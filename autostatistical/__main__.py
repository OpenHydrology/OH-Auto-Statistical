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
import webbrowser
from . import Analysis, UpdateChecker
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
        #: Input catchment file path
        self.catchment_file = catchment_file
        #: Analysis thread
        self.analysis = None
        #: Results report file path
        self.report_file = None
        #: Application update checker
        self.update_checker = None
        #: Holds update info
        self.update = None

        self.title(self.APP_NAME)
        self.iconbitmap(os.path.join(os.path.dirname(__file__), 'application.ico'))

        # Queues and variables
        self.msg_queue = queue.Queue()
        self.progress = tk.IntVar()
        self.status = tk.StringVar()
        self.open_report = tk.IntVar()

        # Widgets
        self.columnconfigure(0, weight=1)
        self.frame = ttk.Frame(self)
        self.frame.grid(column=0, row=0, sticky=('n', 'e', 's', 'w'))
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        content = ttk.Frame(self.frame, padding=(10, 10, 10, 10))
        content.grid(column=0, row=1, sticky=('n', 'e', 's', 'w'))
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, pad=10)
        content.rowconfigure(1, pad=10)
        content.rowconfigure(2, pad=10)
        ttk.Label(content, textvariable=self.status, anchor='w').grid(column=0, row=0, columnspan=2, sticky=('e', 'w'))
        ttk.Progressbar(content, variable=self.progress).grid(column=0, row=1, columnspan=2, sticky=('e', 'w'))
        open_report_chk = ttk.Checkbutton(content, text="Open report when closing application",
                                          variable=self.open_report)
        open_report_chk.grid(column=0, row=2, sticky='w', padx=(0, 20))
        ttk.Button(content, text="Close", command=self.quit, default='active').grid(column=1, row=2)

        if on_win:
            self.open_report.set(1)
        else:
            open_report_chk.config(state=tk.DISABLED)

        self.bind('<Return>', lambda e: self.quit())
        self.protocol('WM_DELETE_WINDOW', self.quit)

        # If no file provided, show file dialog
        if not self.catchment_file:
            self.catchment_file = tkfd.askopenfilename(filetypes=[("Catchment descriptor files", "*.cd3 *.xml")],
                                                       title="Select catchment file")
        if self.catchment_file:
            self.start_analysis(self.catchment_file)
        else:
            self.status.set("No catchment file selected.")

        self.after(2000, self.start_update_check)  # Delay start with 2 seconds

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

    def start_update_check(self):
        """Run update check in separate thread"""
        self.update_checker = UpdateChecker()
        self.update_checker.start()
        self.periodiccall_update_check()

    def periodiccall_update_check(self):
        if self.update_checker.is_alive():
            self.after(1000, self.periodiccall_update_check)
        else:
            self.finish_update_check()

    def finish_update_check(self):
        self.update = self.update_checker.join()
        if self.update:
            bar = MessageBar(self.frame, text="OH Auto Statistical version {} is available.".format(self.update.version),
                             actiontext="Download", command=self.open_update_url)
            bar.grid(column=0, row=0, columnspan=2, sticky=('e', 'w'))

    def open_update_url(self):
        if self.update:
            webbrowser.open(self.update.url)
            self.quit()  # Close application as well


class MessageBar(ttk.Frame):
    """
    A message bar with action button to be placed at the top of the application window.
    """
    bg_colour = '#d9edf7'
    text_colour = '#31708f'

    def __init__(self, parent, text, actiontext=None, command=None):
        """
        :param parent: Parent window/Tkinter frame
        :param text: Text to display in message bar
        :param actiontext: Text on action button
        :param command: Callback function for action button
        :return: Message bar
        :rtype: :class:`ttk.Frame`
        """
        ttk.Frame.__init__(self, parent, padding=(10, 5, 10, 5), style='MB.TFrame')
        style = ttk.Style()
        style.configure('MB.TFrame', background=self.bg_colour)
        style.configure('MB.TFrame', relief=tk.GROOVE)
        style.configure('MB.TLabel', background=self.bg_colour)
        style.configure('MB.TLabel', foreground=self.text_colour)
        self.grid(column=0, row=0)
        self.columnconfigure(0, weight=1)
        ttk.Label(self, text=text, anchor='w', style='MB.TLabel').grid(column=0, row=0, sticky=('e', 'w'))
        if actiontext and command:
            ttk.Button(self, text=actiontext, command=command).grid(column=1, row=0, sticky='e')


if __name__ == "__main__":
    main()
