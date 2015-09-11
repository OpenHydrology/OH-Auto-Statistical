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
    p = argparse.ArgumentParser(prog='autostatistical', description='OH Auto Statistical')
    p.add_argument(
        'catchment_file',
        nargs='?', default=None,
        help='Location of catchment .CD3 or.xml-file.')
    p.add_argument(
        '-v', '--version',
        action='version',
        version='{} {}'.format(p.prog, autostatistical.__version__),
        help='Show the application version number and exit.'
    )
    args = p.parse_args()
    ui = UI(args.catchment_file)
    ui.mainloop()


class UI(tk.Tk):
    APP_NAME = "OH Auto Statistical"

    def __init__(self, catchment_file):
        tk.Tk.__init__(self)
        self.catchment_file = catchment_file
        self.title(self.APP_NAME)
        self.iconbitmap(os.path.join(os.path.dirname(__file__), 'application.ico'))
        self.msg_queue = queue.Queue()
        self.progress = tk.IntVar()
        self.status = tk.StringVar()
        self.listbox = tk.Label(self, textvariable=self.status, anchor='w')
        self.progressbar = ttk.Progressbar(self, orient='horizontal', length=300, mode='determinate',
                                           variable=self.progress)
        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.listbox.pack(fill='x', padx=10, pady=10)
        self.progressbar.pack(padx=10, pady=2)
        self.close_button.pack(anchor='e', ipadx=5, padx=10, pady=10)
        self.protocol('WM_DELETE_WINDOW', self.on_delete)
        #: Analysis thread
        self.analysis = None

        # If no file provided, show file dialog
        if not self.catchment_file:
            self.catchment_file = tkfd.askopenfilename(filetypes=[("Catchment descriptor files", "*.cd3 *.xml")],
                                                       title="Select catchment file")
        if self.catchment_file:
            self.start_analysis(self.catchment_file)
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
        self.analysis = Analysis(catchment_file, self.msg_queue)
        self.analysis.start()
        self.periodiccall()

    def periodiccall(self):
        self.process_msg_queue()
        if self.analysis.is_alive():
            self.after(10, self.periodiccall)
        else:
            self.progress.set(100)
            self.close_button.config(state='active')

    def process_msg_queue(self):
        while self.msg_queue.qsize():
            progress = self.msg_queue.get(0)
            self.status.set(progress.msg)
            self.progress.set(progress.perc)


if __name__ == "__main__":
    main()
