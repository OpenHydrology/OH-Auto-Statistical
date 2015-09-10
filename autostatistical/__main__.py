# -*- coding: utf-8 -*-

# OH Auto Statistical
# Copyright (C) 2014-2015 Florenz A. P. Hollebrandse
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

import argparse
import tkinter as tk
import tkinter.messagebox as tkmb
import tkinter.filedialog as tkfd
import os.path
from . import Analysis
import autostatistical


def main():
    parser = argparse.ArgumentParser(prog='autostatistical', description='OH Auto Statistical')
    parser.add_argument(
        'catchment_file',
        nargs='?', default=None,
        help='Location of catchment .CD3 or.xml-file.')
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='{} {}'.format(parser.prog, autostatistical.__version__),
        help='Show the application version number and exit.'
    )
    args = parser.parse_args()
    root = tk.Tk()
    root.withdraw()  # Hide main window to show dialogs only
    root.iconbitmap(os.path.join(os.path.dirname(__file__), 'application.ico'))

    # If no file provided, show file dialog
    if not args.catchment_file:
        args.catchment_file = tkfd.askopenfilename(filetypes=[("Catchment descriptor files", "*.cd3 *.xml")],
                                                   title="Select catchment file - {}".format(parser.description))
    if not args.catchment_file:
        return  # User cancelled

    # Run analysis
    try:
        analysis = Analysis(args.catchment_file)
        analysis.run()
    except Exception as e:
        tkmb.showerror(parser.description, 'The following error occurred:\n\n' + str(e))
    else:
        tkmb.showinfo(parser.description, 'OH Auto Statistical report successfully created.')


if __name__ == "__main__":
    main()
