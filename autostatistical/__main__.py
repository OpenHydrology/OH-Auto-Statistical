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
from . import Analysis


def main():
    parser = argparse.ArgumentParser(description='Create OH Auto Statistical flood estimation report.')
    parser.add_argument('file_path', nargs='?', default=None, help='Location of catchment CD3-file.')
    args = parser.parse_args()

    if not args.file_path:
        import tkinter as tk
        import tkinter.filedialog as tkfd
        root = tk.Tk()
        root.withdraw()  # No main window, just the file dialog
        args.file_path = tkfd.askopenfilename(filetypes=[
            ("Catchment descriptor files", "*.cd3 *.xml"),
            ("All files", "*.*")
        ])
    if not args.file_path:
        return  # User cancelled

    try:
        analysis = Analysis(args.file_path)
        analysis.run()
        analysis.create_report()
    except Exception as e:
        print(e)
        input("Press Enter to close this window.")


if __name__ == "__main__":
    main()
