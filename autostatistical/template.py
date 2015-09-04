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

import math
import jinja2 as jj
import jinja2.exceptions
import jinja2.utils
from appdirs import AppDirs
import os

APP_NAME = 'OH Auto Statistical'
APP_AUTHOR = 'Open Hydrology'


class TemplateEnvironment(jj.Environment):
    """
    A jinja2 template environment with loader and filters setup.
    """
    def __init__(self):
        jj.Environment.__init__(self)
        self.trim_blocks = True

        # Load templates from within the package
        self.loader = jj.ChoiceLoader([
            jj.FileSystemLoader(self.user_template_folder()),
            jj.PackageLoader('autostatistical', 'templates')
        ])

        # Custom formatting filters
        self.filters['dateformat'] = self.dateformat
        self.filters['round'] = self.round
        self.filters['signif'] = self.signif
        self.filters['floatcolumn'] = self.floatcolumn
        self.filters['signifcolumn'] = self.signifcolumn
        self.filters['intcolumn'] = self.intcolumn
        self.filters['strcolumn'] = self.strcolumn
        self.filters['default'] = self.default

    def user_template_folder(self):
        template_folder = os.path.join(AppDirs(APP_NAME, APP_AUTHOR).user_data_dir, 'templates')
        return template_folder

    @staticmethod
    def dateformat(value, format='%d/%m/%Y'):
        """
        Format a date
        """
        try:
            return value.strftime(format)
        except (ValueError, TypeError, AttributeError, jinja2.exceptions.UndefinedError):
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
            return ' ' * (sep_pos - 1) + ' ' + ' ' * (width - sep_pos)

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
            return ' ' * width

    @staticmethod
    def strcolumn(value, width=25):
        try:
            return "{value:<{width:d}s}".format(value=value, width=width)
        except (ValueError, TypeError):
            return ' ' * width

    @staticmethod
    def default(value, default=''):
        if value is None or jinja2.utils.is_undefined(value):
            return default
        else:
            return value