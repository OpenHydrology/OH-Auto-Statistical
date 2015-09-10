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
from tkinter import ttk
import tkinter.filedialog as tkfd
import queue
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
    ui = UI(parser)
    ui.mainloop()


class UI(tk.Tk):
    def __init__(self, arg_parser):
        tk.Tk.__init__(self)
        self.args = arg_parser.parse_args()
        self.title(arg_parser.description)
        self.iconbitmap(os.path.join(os.path.dirname(__file__), 'application.ico'))
        self.queue = queue.Queue()
        self.status = tk.StringVar()
        self.listbox = tk.Label(self, textvariable=self.status, anchor='w')
        self.progressbar = ttk.Progressbar(self, orient='horizontal', length=300, mode='determinate')
        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.listbox.pack(fill='x', padx=10, pady=10)
        self.progressbar.pack(padx=10, pady=2)
        self.close_button.pack(anchor='e', ipadx=5, padx=10, pady=10)
        self.protocol('WM_DELETE_WINDOW', self.on_delete)
        self.analysis = None

        # If no file provided, show file dialog
        if not self.args.catchment_file:
            self.args.catchment_file = tkfd.askopenfilename(filetypes=[("Catchment descriptor files", "*.cd3 *.xml")],
                                                            title="Select catchment file")
        if self.args.catchment_file:
            self.start_analysis(self.args.catchment_file)
        else:
            self.status.set("No catchment file selected.")

    def on_delete(self):
        """Intercept exit if analysis is running."""
        if self.analysis:
            if self.analysis.is_alive():
                return
        self.destroy()

    def start_analysis(self, catchment_file):
        """Run analysis is separate thread."""
        self.close_button.config(state='disabled')
        self.analysis = Analysis(catchment_file, self.queue)
        self.analysis.start()
        self.periodiccall()

    def periodiccall(self):
        self.process_msg_queue()
        if self.analysis.is_alive():
            self.after(100, self.periodiccall)
        else:
            self.close_button.config(state='active')

    def process_msg_queue(self):
        while self.queue.qsize():
            msg = self.queue.get(0)
            self.status.set(msg)
            self.progressbar.step(19.95)


if __name__ == "__main__":
    main()
