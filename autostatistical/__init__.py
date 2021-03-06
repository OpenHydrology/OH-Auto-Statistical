# -*- coding: utf-8 -*-

# OH Auto Statistical
# Copyright (C) 2014-2015  Florenz A. P. Hollebrandse
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import configparser
import os.path
import threading
import queue
import json
from urllib import request
import urllib.error
from appdirs import AppDirs
from collections import namedtuple
from distutils.version import LooseVersion
from datetime import date
from floodestimation import loaders
from floodestimation import db
from floodestimation import fehdata
from floodestimation import entities
from floodestimation.collections import CatchmentCollections
from floodestimation.analysis import QmedAnalysis, GrowthCurveAnalysis
from .template import TemplateEnvironment


#: Named tuple for passing messages and percentage completion through thread queue
Progress = namedtuple('Progress', ['msg', 'perc'])


class Analysis(threading.Thread):
    """
    Analysis and report creation object.

    Start thread as ``Analysis(...).start()``
    """
    def __init__(self, catchment_file, msg_queue=None):
        threading.Thread.__init__(self)
        #: Path to catchment file
        self.catchment_file = catchment_file
        #: Settings from ini file
        self.config = Config()
        #: Queue for passing messages to UI
        self.msg_queue = msg_queue if msg_queue is not None else queue.Queue()
        #: Name of analysis/catchment based on file name
        self.name = os.path.basename(os.path.splitext(catchment_file)[0])
        #: Working folder
        self.folder = os.path.dirname(catchment_file)
        #: :class:`floodestimation.entities.Catchment` object
        self.catchment = None
        #: Database session
        self.db_session = None
        #: Gauged catchments collection
        self.gauged_catchments = None
        #: Big dict holding all results, to be passed as context to Jinja2
        self.results = {}
        #: QMED result value
        self.qmed = None
        #: Report file path
        self.report_file = None
        #: Any exceptions occurring during analysis
        self.exc = None

    def _load_data(self):
        self.results['report_date'] = date.today()
        self.results['version'] = __version__
        self.catchment = loaders.from_file(self.catchment_file)
        self.results['catchment'] = self.catchment
        self.db_session = db.Session()

        if self.db_session.query(entities.Catchment).count() == 0:
            self.msg_queue.put(Progress("Downloading and storing NRFA data.", 10))
            loaders.nrfa_to_db(self.db_session, autocommit=True, incl_pot=False)
        if self.config.getboolean('application', 'check_nrfa_updates', fallback=True):
            if fehdata.update_available():
                self.msg_queue.put(Progress("Downloading and storing NRFA data update.", 10))
                db.empty_db_tables()
                loaders.nrfa_to_db(self.db_session, autocommit=True, incl_pot=False)

        # Add subject catchment to db if gauged
        if self.catchment.record_length > 0:
            loaders.to_db(self.catchment, self.db_session, method='update', autocommit=True)

        self.msg_queue.put(Progress("Loading additional data.", 20))
        loaders.userdata_to_db(self.db_session, autocommit=True)

        self.gauged_catchments = CatchmentCollections(self.db_session, load_data='manual')
        self.results['nrfa'] = fehdata.nrfa_metadata()

    def finish(self):
        if self.db_session:
            self.db_session.close()

    def join(self):
        """Return report file path when completed and thread joined."""
        threading.Thread.join(self)
        if self.exc:
            raise self.exc

        return self.report_file

    def run(self):
        try:
            self.msg_queue.put(Progress("Loading data.", 5))
            self._load_data()
            self.msg_queue.put(Progress("Running median annual flood analysis.", 25))
            self._run_qmed_analysis()
            self.msg_queue.put(Progress("Running growth curve analysis.", 50))
            self._run_growthcurve()
            self.msg_queue.put(Progress("Creating results report.", 75))
            self.report_file = self._create_report()
            self.msg_queue.put(Progress("Results report completed.", 95))
        except BaseException as e:
            self.exc = e
        finally:
            self.finish()

    def _run_qmed_analysis(self):
        results = {}

        analysis = QmedAnalysis(self.catchment, self.gauged_catchments, results_log=results)
        self.qmed = analysis.qmed()

        results['qmed'] = self.qmed
        self.results['qmed'] = results

    def _run_growthcurve(self):
        results = {}

        analysis = GrowthCurveAnalysis(self.catchment, self.gauged_catchments, results_log=results)
        gc = analysis.growth_curve()

        aeps = [0.5, 0.2, 0.1, 0.05, 0.03333, 0.02, 0.01333, 0.01, 0.005, 0.002, 0.001]
        growth_factors = gc(aeps)
        flows = growth_factors * self.qmed

        results['aeps'] = aeps
        results['growth_factors'] = growth_factors
        results['flows'] = flows
        self.results['gc'] = results

    def _create_report(self):
        rep = Report(self.name, self.results, template_name='normal.md')
        return rep.save(self.folder)


class Report(object):
    def __init__(self, name, context, template_name):
        self.name = name
        self.context = context
        self.template_name = template_name
        self.template_extension = os.path.splitext(template_name)[1]
        self.template = self._get_template()

    def _get_template(self):
        env = TemplateEnvironment()
        return env.get_template(self.template_name)

    def _get_content(self):
        return self.template.render(self.context)

    def save(self, to_folder):
        date_str = date.today().isoformat()
        file_path = os.path.join(to_folder, '{}.Flood estimation report.{}{}'.
                                 format(self.name, date_str, self.template_extension))
        content = self._get_content()
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except FileNotFoundError:
            raise FileNotFoundError("Destination folder `{}` does not exist.".format(to_folder))
        except PermissionError:
            raise PermissionError("No write access to destination folder {}".format_map(to_folder))
        except:
            raise
        return file_path


#: Update information. `version` key is :class:`distutils.version.Version` object
Update = namedtuple('Update', ['version', 'url'])


class UpdateChecker(threading.Thread):
    """
    Checks for application updates based on GitHub repo published releases
    """
    API_URL = 'https://api.github.com/repos/openhydrology/oh-auto-statistical/releases/latest'
    TAG_PREFIX = 'v'

    def __init__(self):
        threading.Thread.__init__(self)
        self.update = None

    def run(self):
        try:
            with request.urlopen(self.API_URL, timeout=5) as f:
                data = json.loads(f.read().decode('utf-8'))
                repo_version = LooseVersion(data['tag_name'].lstrip(self.TAG_PREFIX))
                url = data['html_url']
        except BaseException:  # Anything going wrong: we don't care
            return
        current_version = LooseVersion(__version__)
        if repo_version > current_version:
            self.update = Update(version=repo_version, url=url)

    def join(self):
        threading.Thread.join(self)
        return self.update


class Config(configparser.ConfigParser):
    """
    Configuration/settings object.

    Settings are read from a `config.ini` file within the python package (default values) or from the user's appdata
    folder. Data is read immediately when object initiated. Data are only written to user file.
    """
    FILE_NAME = 'config.ini'
    APP_NAME = 'autostatistical'
    APP_ORG = 'Open Hydrology'

    def __init__(self):
        configparser.ConfigParser.__init__(self)

        here = os.path.abspath(os.path.dirname(__file__))
        self._app_folders = AppDirs(self.APP_NAME, self.APP_ORG)
        self._default_config_file = os.path.join(here, self.FILE_NAME)

        os.makedirs(self._app_folders.user_config_dir, exist_ok=True)  # Create folder in advance if necessary
        self._user_config_file = os.path.join(self._app_folders.user_config_dir, self.FILE_NAME)

        self.read_file(open(self._default_config_file, encoding='utf-8'))
        self.read()

    def read(self):
        """
        Read config data from user config file.
        """
        configparser.ConfigParser.read(self, self._user_config_file, encoding='utf-8')

    def save(self):
        """
        Write data to user config file.
        """
        with open(self._user_config_file, 'w', encoding='utf-8') as f:
            self.write(f)
