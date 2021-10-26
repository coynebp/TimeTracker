import os
from datetime import datetime
from datetime import timedelta
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont
import math

VERSION = 'v1.3.0'

class Session:
    def __init__(self, project: str, startTime: datetime, stopTime: datetime):
        self.project = project
        self.startTime = startTime
        self.stopTime = stopTime
        self.totalTime = self.stopTime - self.startTime

class TimerApp:
    def __init__(self):
        self.sessions = []
        self.projects = []
        self.running = False
        self.startTime = None
        self.elapsedTime = timedelta()
        self.elapsedSeconds = 0
        self.recordedSeconds = 0
        self.totalSeconds = 0
        #create tk instance
        self.root = tk.Tk()
        #create font
        self.entryFont = tkfont.Font(self.root, weight=tkfont.BOLD)
        #create tk variables
        self.sessionFrame = tk.Frame(self.root)
        self.sessionProjectLabels = []
        self.sessionTimeLabels = []
        self.totalTimeLabel = tk.Label(self.root, text='Total Time:', width=15, anchor='w', font=self.entryFont)
        self.totalTimeVar = tk.StringVar(self.root, value=time_string(self.totalSeconds))
        self.totalTime = tk.Label(self.root, textvariable=self.totalTimeVar, width=12, anchor='w', font=self.entryFont)
        self.projectLabel = tk.Label(self.root, text='Project: ', font=self.entryFont)
        self.projectVar = tk.StringVar(self.root)
        self.projectBox = ttk.Combobox(self.root, textvariable=self.projectVar, values=self.projects)
        self.timeVar = tk.StringVar(self.root, value=time_string(self.elapsedSeconds))
        self.timeLabel = tk.Label(self.root, textvariable=self.timeVar, width=12, anchor='w', font=self.entryFont)
        self.startStopButton = tk.Button(self.root, text="Start", command=self.start)
        self.resetButton = tk.Button(self.root, text="Reset", command=self.reset)
        #run app
        self.runApp()
    def start(self, event=None):
        self.startStopButton.configure(text="Stop", command=self.stop)
        self.root.bind('<Return>', self.stop)
        self.projectBox.configure(state=tk.DISABLED)
        self.startTime = datetime.now()
        self.running = True
        self.update()
    def stop(self, event=None):
        self.root.bind('<Return>', self.start)
        self.startStopButton.configure(text="Start", command=self.start)
        self.sessions[:0] = [Session(self.projectVar.get(), self.startTime, datetime.now())]
        self.sessionProjectLabels[:0] = [tk.Label(self.sessionFrame, 
                                                 text=self.projectVar.get(), 
                                                 width=22, 
                                                 anchor='w'
                                                 )]
        elapsedSeconds = self.sessions[0].totalTime.total_seconds()
        self.sessionTimeLabels[:0] = [tk.Label(self.sessionFrame, 
                                              text=time_string(elapsedSeconds), 
                                              width=17, 
                                              anchor='w'
                                              )]
        for index in range(len(self.sessionProjectLabels)):
            self.sessionProjectLabels[index].grid(row=index, column=0)
            self.sessionTimeLabels[index].grid(row=index, column=1)
        self.running = False
        self.recordedSeconds += math.floor(self.elapsedSeconds)
        if self.projectVar.get() not in self.projects:
            self.projects.append(self.projectVar.get())
        self.projectVar.set('')
        self.projectBox.configure(state=tk.NORMAL, values=self.projects)
    def reset(self):
        self.root.bind('<Return>', self.start)
        self.startStopButton.configure(text="Start", command=self.start)
        self.running = False
        self.projectVar.set('')
        self.projectBox.configure(state=tk.NORMAL, values=self.projects)
        self.elapsedSeconds = 0
        self.recordedSeconds = 0
        self.totalSeconds = 0
        for label in self.sessionProjectLabels:
            label.destroy()
        for label in self.sessionTimeLabels:
            label.destroy()
        del self.sessionProjectLabels[:]
        del self.sessionTimeLabels[:]
        self.sessionFrame.grid(row=2, column=1, columnspan=2)
    def update(self):
        if self.running:
            self.elapsedTime = datetime.now() - self.startTime
        else:
            self.elapsedTime = timedelta()
        self.elapsedSeconds = self.elapsedTime.total_seconds()
        self.timeVar.set(time_string(self.elapsedSeconds))
        self.totalSeconds = self.recordedSeconds + self.elapsedSeconds
        self.totalTimeVar.set(time_string(self.totalSeconds))
        #schedule the update function
        self.root.after(16, self.update)
    def runApp(self):
        #set window size
        self.root.geometry("430x400")
        #set title, icon
        self.root.title("TimeTracker " + VERSION)
        directory = os.path.dirname(__file__)
        iconpath = os.path.join(directory, 'time_icon.ico')
        self.root.iconbitmap(iconpath)
        #arrange window
        self.root.grid()
        self.totalTimeLabel.grid(row=0, column=1, pady=4)
        self.totalTime.grid(row=0, column=2, pady=4)
        self.projectLabel.grid(row=1, column=0, pady=4)
        self.projectBox.grid(row=1, column=1, pady=4)
        self.timeLabel.grid(row=1, column=2, pady=4)
        self.startStopButton.grid(row=1, column=3, pady=4)
        self.resetButton.grid(row=1, column=4, pady=4)
        self.sessionFrame.grid(row=2, column=1, columnspan=2)
        #bind enter key
        self.root.bind('<Return>', self.start)
        #run app
        self.root.mainloop()

def time_string(totalSeconds: int) -> str:
    seconds = int(totalSeconds % 60)
    minutes = int((totalSeconds // 60) % 60)
    hours = int(totalSeconds // 3600)
    return "{:02d}h {:02d}m {:02d}s".format(hours, minutes, seconds)


def main():
    TimerApp()


if __name__ == "__main__":
    main()