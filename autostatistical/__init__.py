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

import os.path
import threading
from datetime import date
from floodestimation import loaders
from floodestimation import db
from floodestimation import fehdata
from floodestimation.collections import CatchmentCollections
from floodestimation.analysis import QmedAnalysis, GrowthCurveAnalysis
from .template import TemplateEnvironment


class Analysis(threading.Thread):
    def __init__(self, cd3_file_path, msg_queue):
        threading.Thread.__init__(self)
        self.cd3_file_path = cd3_file_path
        self.msg_queue = msg_queue
        self.name = os.path.basename(os.path.splitext(cd3_file_path)[0])
        self.folder = os.path.dirname(cd3_file_path)
        self.catchment = None
        self.db_session = None
        self.gauged_catchments = None
        self.results = {}
        self.qmed = None

    def _load_data(self):
        self.results['report_date'] = date.today()
        self.catchment = loaders.from_file(self.cd3_file_path)
        self.results['catchment'] = self.catchment
        self.db_session = db.Session()
        # Add subject catchment to db if gauged
        if self.catchment.record_length > 0:
            loaders.to_db(self.catchment, self.db_session, method='update', autocommit=True)
        # Add additional catchment data
        loaders.userdata_to_db(self.db_session, autocommit=True)

        self.gauged_catchments = CatchmentCollections(self.db_session)
        self.results['nrfa'] = fehdata.nrfa_metadata()

    def finish(self):
        self.db_session.close()

    def run(self):
        try:
            self.msg_queue.put("Loading data.")
            self._load_data()
            self.msg_queue.put("Running median annual flood analysis.")
            self._run_qmed_analysis()
            self.msg_queue.put("Running growth curve analysis.")
            self._run_growthcurve()
            self.msg_queue.put("Creating results report.")
            self._create_report()
            self.msg_queue.put("Results report completed.")
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
        rep.save(self.folder)


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
