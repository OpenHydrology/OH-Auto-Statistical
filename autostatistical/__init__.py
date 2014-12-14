# -*- coding: utf-8 -*-

# OH Auto Statistical
# Copyright (C) 2014  Florenz A. P. Hollebrandse
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

import floodestimation as fe
from floodestimation.loaders import load_catchment
import jinja2 as jj
import jinja2.exceptions
import os.path
from datetime import date


class Analysis(object):
    def __init__(self, cd3_file_path):
        self.cd3_file_path = cd3_file_path
        self.name = os.path.basename(os.path.splitext(cd3_file_path)[0])
        self.folder = os.path.dirname(cd3_file_path)
        self.results = {'report_date': date.today()}
        self.catchment = load_catchment(cd3_file_path)
        self.results['catchment'] = self.catchment

    def run(self):
        self.run_qmed_analysis()

    def run_qmed_analysis(self):
        self.results['qmed_adjusted'] = '1.2'

    def create_report(self):
        rep = Report(self.name, self.results, template_name='plain.md')
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
        file_path = os.path.join(to_folder, '{}.{}{}'.format(self.name, date_str, self.template_extension))
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
    def __init__(self):
        jj.Environment.__init__(self)
        self.loader = jj.PackageLoader('autostatistical', 'templates')
        self.filters['dateformat'] = self.dateformat
        self.filters['floatformat'] = self.floatformat

    @staticmethod
    def dateformat(value, format='%d/%m/%Y'):
        try:
            return value.strftime(format)
        except AttributeError:
            return ""

    @staticmethod
    def floatformat(value, decimals=3):
        width = 7 + decimals
        if decimals == 0:
            width -= 1
        padding = ' ' * (12 - width)  # right-hand padding: non-breaking space
        return "{value:>{width}.{decimals}f}{padding}". \
            format(value=value, width=width, decimals=decimals, padding=padding)