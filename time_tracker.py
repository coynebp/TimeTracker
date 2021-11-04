"""

TimeTracker.py

GUI for keeping track of time worked on different projects.

Brian Coyne, 2021

"""
import os
from datetime import datetime
from datetime import timedelta
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkfont
import math
from dataclasses import dataclass

VERSION = "v1.4.1"

# pylint: disable=too-many-instance-attributes
# GUIs often contain many attributes


@dataclass
class Session:
    """
    Class for storing data from a project time session.
    """

    project: str
    start_time: datetime
    stop_time: datetime

    def total_time(self) -> timedelta:
        """Returns total time spent during session"""
        return self.stop_time - self.start_time


class TimerApp:
    """
    Application and GUI for timing work done on projects.
    """

    def __init__(self):
        self.sessions = []
        self.projects = []
        self.project_options =[]
        self.running = False
        self.start_time = None
        self.elapsed_time = timedelta()
        self.elapsed_seconds = 0
        self.recorded_seconds = 0
        self.total_seconds = 0
        # create tk instance
        self.root = tk.Tk()
        # create font
        self.entry_font = tkfont.Font(self.root, weight=tkfont.BOLD)
        # create tk variables
        self.session_frame = tk.Frame(self.root)
        self.session_project_labels = []
        self.session_time_labels = []
        self.total_time_label = tk.Label(
            self.root, text="Total Time:", width=15, anchor="w", font=self.entry_font
        )
        self.total_time_var = tk.StringVar(
            self.root, value=time_string(self.total_seconds)
        )
        self.total_time = tk.Label(
            self.root,
            textvariable=self.total_time_var,
            width=12,
            anchor="w",
            font=self.entry_font,
        )
        self.project_label = tk.Label(self.root, text="Project: ", font=self.entry_font)
        self.project_var = tk.StringVar(self.root)
        self.project_box = ttk.Combobox(
            self.root, textvariable=self.project_var, values=self.project_options
        )
        self.time_var = tk.StringVar(self.root, value=time_string(self.elapsed_seconds))
        self.time_label = tk.Label(
            self.root,
            textvariable=self.time_var,
            width=12,
            anchor="w",
            font=self.entry_font,
        )
        self.start_stop_button = tk.Button(self.root, text="Start", command=self.start)
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        # run app
        self.run_app()

    def start(self, event=None):
        """Starts a new session"""
        del event
        self.start_stop_button.configure(text="Stop", command=self.stop)
        self.root.bind("<Return>", self.stop)
        self.project_box.configure(state=tk.DISABLED)
        self.start_time = datetime.now()
        self.running = True
        self.update()

    def stop(self, event=None):
        """Stops current session"""
        del event
        self.root.bind("<Return>", self.start)
        self.start_stop_button.configure(text="Start", command=self.start)
        self.sessions[:0] = [
            Session(self.project_var.get(), self.start_time, datetime.now())
        ]
        elapsed_seconds = self.sessions[0].total_time().total_seconds()
        self.recorded_seconds += math.floor(self.elapsed_seconds)
        if self.sessions[0].project in self.projects:
            for session in self.sessions[1:]:
                if session.project == self.sessions[0].project:
                    elapsed_seconds += math.floor(session.total_time().total_seconds())
            for (index, label) in enumerate(self.session_time_labels):
                if self.session_project_labels[index]['text'] == self.sessions[0].project:
                    self.session_time_labels[index].configure(text=time_string(elapsed_seconds))
        else:
            self.session_project_labels[:0] = [
                tk.Label(
                    self.session_frame, text=self.project_var.get(), width=22, anchor="w"
                )
            ]
            self.session_time_labels[:0] = [
                tk.Label(
                    self.session_frame,
                    text=time_string(elapsed_seconds),
                    width=17,
                    anchor="w",
                )
            ]
        for (index, label) in enumerate(self.session_project_labels):
            label.grid(row=index, column=0)
        for (index, label) in enumerate(self.session_time_labels):
            label.grid(row=index, column=1)
        self.running = False
        if self.project_var.get() not in self.projects:
            self.projects.append(self.project_var.get())
        if self.project_var.get() not in self.project_options:
            self.project_options.append(self.project_var.get())
        self.project_var.set("")
        self.project_box.configure(state=tk.NORMAL, values=self.project_options)

    def reset(self):
        """Prompts user for confirmation, then resets the GUI"""
        if messagebox.askokcancel("Reset", "Reset all timing data?"):
            self.root.bind("<Return>", self.start)
            self.start_stop_button.configure(text="Start", command=self.start)
            self.running = False
            self.project_var.set("")
            self.project_box.configure(state=tk.NORMAL, values=self.projects)
            self.elapsed_seconds = 0
            self.recorded_seconds = 0
            self.total_seconds = 0
            self.projects = []
            for label in self.session_project_labels:
                label.destroy()
            for label in self.session_time_labels:
                label.destroy()
            del self.session_project_labels[:]
            del self.session_time_labels[:]
            self.session_frame.grid(row=2, column=1, columnspan=2)

    def update(self):
        """Update the running timers"""
        if self.running:
            self.elapsed_time = datetime.now() - self.start_time
        else:
            self.elapsed_time = timedelta()
        self.elapsed_seconds = self.elapsed_time.total_seconds()
        self.time_var.set(time_string(self.elapsed_seconds))
        self.total_seconds = self.recorded_seconds + self.elapsed_seconds
        self.total_time_var.set(time_string(self.total_seconds))
        # schedule the update function
        self.root.after(16, self.update)

    def run_app(self):
        """Builds application window and runs app"""
        # set window size
        self.root.geometry("430x400")
        # set title, icon
        self.root.title("TimeTracker " + VERSION)
        directory = os.path.dirname(__file__)
        iconpath = os.path.join(directory, "time_icon.ico")
        self.root.iconbitmap(iconpath)
        # arrange window
        self.root.grid()
        self.total_time_label.grid(row=0, column=1, pady=4)
        self.total_time.grid(row=0, column=2, pady=4)
        self.project_label.grid(row=1, column=0, pady=4)
        self.project_box.grid(row=1, column=1, pady=4)
        self.time_label.grid(row=1, column=2, pady=4)
        self.start_stop_button.grid(row=1, column=3, pady=4)
        self.reset_button.grid(row=1, column=4, pady=4)
        self.session_frame.grid(row=2, column=1, columnspan=2)
        # bind enter key
        self.root.bind("<Return>", self.start)
        # run app
        self.root.mainloop()


def time_string(total_seconds: int) -> str:
    '''Formats the number of seconds given into "xxh xxm xxs"'''
    seconds = int(total_seconds % 60)
    minutes = int((total_seconds // 60) % 60)
    hours = int(total_seconds // 3600)
    return f"{hours:02d}h {minutes:02d}m {seconds:02d}s"


def main():
    """Runs the timer application"""
    TimerApp()


if __name__ == "__main__":
    main()
