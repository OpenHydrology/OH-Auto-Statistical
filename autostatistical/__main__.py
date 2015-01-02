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

import sys
from . import Analysis


def main(argv):
    try:
        cd3_file_path = argv[0]
    except IndexError:
        print("A CD3-file must be specified.")
        sys.exit()

    analysis = Analysis(cd3_file_path)
    analysis.run()
    analysis.create_report()


if __name__ == "__main__":
    main(sys.argv[1:])