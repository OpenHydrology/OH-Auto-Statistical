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

import jinja2 as jj
import jinja2.exceptions
import os.path
import math
from datetime import date
from floodestimation.loaders import load_catchment
from floodestimation import db
from floodestimation.collections import CatchmentCollections
from floodestimation.analysis import QmedAnalysis, GrowthCurveAnalysis


class Analysis(object):
    def __init__(self, cd3_file_path):
        self.cd3_file_path = cd3_file_path
        self.name = os.path.basename(os.path.splitext(cd3_file_path)[0])
        self.folder = os.path.dirname(cd3_file_path)
        self.results = {'report_date': date.today()}
        self.catchment = load_catchment(cd3_file_path)
        self.results['catchment'] = self.catchment
        self.db_session = db.Session()
        self.gauged_catchments = CatchmentCollections(self.db_session)
        self.qmed = None

    def finish(self):
        self.db_session.close()

    def run(self):
        try:
            self.run_qmed_analysis()
            self.run_growthcurve()
        finally:
            self.finish()

    def run_qmed_analysis(self):
        results = {}

        analysis = QmedAnalysis(self.catchment, self.gauged_catchments, results_log=results)
        self.qmed = analysis.qmed(method='descriptors')

        results['qmed'] = self.qmed
        self.results['qmed'] = results

    def run_growthcurve(self):
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

    def create_report(self):
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
            raise PermissionError("No wright access to destination folder {}".format_map(to_folder))
        except:
            raise


class TemplateEnvironment(jj.Environment):
    """
    A jinja2 template environment with loader and filters setup.
    """
    def __init__(self):
        jj.Environment.__init__(self)
        self.trim_blocks = True

        # Load templates from within the package
        self.loader = jj.PackageLoader('autostatistical', 'templates')

        # Custom formatting filters
        self.filters['dateformat'] = self.dateformat
        self.filters['round'] = self.round
        self.filters['signif'] = self.signif
        self.filters['floatcolumn'] = self.floatcolumn
        self.filters['signifcolumn'] = self.signifcolumn
        self.filters['intcolumn'] = self.intcolumn
        self.filters['strcolumn'] = self.strcolumn

    @staticmethod
    def dateformat(value, format='%d/%m/%Y'):
        """
        Format a date
        """
        try:
            return value.strftime(format)
        except (ValueError, TypeError, AttributeError):
            return ""

    @staticmethod
    def round(value, decimals=2):
        """
        Override the default jinja round filter as it drops decimals.
        """
        try:
            return "{value:.{decimals:d}f}".format(value=value, decimals=decimals)
        except (ValueError, TypeError):
            return ""

    @staticmethod
    def floatcolumn(value, decimals=3, width=12, sep_pos=None):
        """
        Format number within a fixed-width column and specified number of decimal places.

        The formatter assumes columns are right-aligned: padding to the left of the value are ordinary spaces (which may
        collapse in HTML) and padding to the right are figure spaces (they have the same width as numerals in non
        fixed-width fonts, they don't collapse in HTML). Some fixed-width fonts actually adjust the width of figure
        spaces and punctuation spaces, which is silly.

        :param value: Value to be formatted
        :param decimals: Number of decimal places, default: 3
        :param width: Column width, default: 12 characters
        :param sep_pos: Position of the decimal point within the column
        :return: Formatted string
        """
        if not sep_pos:
            sep_pos = width - decimals
        number_width = sep_pos + decimals
        if decimals == 0:
            number_width -= 1
            padding = ' ' + ' ' * (width - number_width - 1)  # punctuation space followed by figure spaces
        else:
            padding = ' ' * (width - number_width)  # figure spaces
        try:
            return "{value:>{width:d}.{decimals:d}f}{padding:s}". \
                format(value=value, width=number_width, decimals=decimals, padding=padding)
        except (ValueError, TypeError):
            return ""

    @staticmethod
    def signif(value, significance=2):
        """
        Format a float with a certain number of significant figures.

        E.g.:

            signif(1.234) == '1.23'
            signif(123.4) == '120'

        :param value: Value to be formatted
        :param significance: Number of significant figures
        :return: Formatted string
        """
        try:
            order = math.floor(math.log10(value))
            decimals = max(0, significance - order - 1)
            rounded_value = round(value, significance - order - 1)
            return "{value:.{decimals:d}f}".format(value=rounded_value, decimals=decimals)
        except (ValueError, TypeError, jinja2.exceptions.UndefinedError):
            return ""

    @staticmethod
    def signifcolumn(value, significance=2, width=12, sep_pos=None):
        order = math.floor(math.log10(value))
        decimals = max(0, significance - order - 1)
        rounded_value = round(value, significance - order - 1)
        return TemplateEnvironment.floatcolumn(rounded_value, decimals, width, sep_pos)

    @staticmethod
    def intcolumn(value, width=12):
        try:
            return "{value:>{width:d}.0f}".format(value=value, width=width)
        except (ValueError, TypeError):
            return ""

    @staticmethod
    def strcolumn(value, width=25):
        try:
            return "{value:<{width:d}s}".format(value=value, width=width)
        except (ValueError, TypeError):
            return ""