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
import tkinter.messagebox as tkmb
import tkinter.filedialog as tkfd
import subprocess
import queue
import os.path
import sys
from . import Analysis
import autostatistical


on_win = sys.platform == 'win32'


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
        self.progressbar = ttk.Progressbar(self, orient='horizontal', length=300, mode='determinate',
                                           variable=self.progress)
        self.status = tk.StringVar()
        self.open_report = tk.IntVar()
        self.listbox = tk.Label(self, textvariable=self.status, anchor='w')
        self.open_report_ceck = tk.Checkbutton(self, text="Open report when closing application", variable=self.open_report)
        if on_win:
            self.open_report.set(1)
        else:
            self.open_report_ceck.config(state=tk.DISABLED)
        self.close_button = tk.Button(self, text="Close", command=self.quit, default='active')
        self.listbox.pack(fill='x', padx=10, pady=10)
        self.progressbar.pack(padx=10, pady=2)
        self.close_button.pack(anchor='e', side='right', ipadx=5, padx=10, pady=10)
        self.open_report_ceck.pack(anchor='w', padx=10, pady=10)
        self.bind('<Return>', lambda e: self.quit())
        self.protocol('WM_DELETE_WINDOW', self.quit)
        #: Analysis thread
        self.analysis = None
        #: Results report file path
        self.report_file = None

        # If no file provided, show file dialog
        if not self.catchment_file:
            self.catchment_file = tkfd.askopenfilename(filetypes=[("Catchment descriptor files", "*.cd3 *.xml")],
                                                       title="Select catchment file")
        if self.catchment_file:
            self.start_analysis(self.catchment_file)
        else:
            self.status.set("No catchment file selected.")

    def quit(self):
        """Intercept exit if analysis is running."""
        if self.analysis:
            if self.analysis.is_alive():
                return
        if self.open_report.get() and self.report_file:
            subprocess.Popen(['notepad', self.report_file],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) # Don't wait
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
            self.after(50, self.periodiccall)
        else:
            self.finish_analysis()

    def process_msg_queue(self):
        while 1:
            try:
                progress = self.msg_queue.get(0)
                self.status.set(progress.msg)
                self.progress.set(progress.perc)
            except queue.Empty:
                return

    def finish_analysis(self):
        try:
            self.report_file = self.analysis.join()
            self.progress.set(100)
        except Exception as e:
            self.status.set("An error occurred.")
            tkmb.showerror(title=self.APP_NAME, message="The following error occurred:\n\n{}".format(repr(e)))
        self.close_button.config(state='active')


if __name__ == "__main__":
    main()
