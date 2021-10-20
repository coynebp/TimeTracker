import os
from datetime import datetime
from datetime import timedelta
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont

VERSION = 'v1.0.0'

class Session:
    def __init__(self, project: str, startTime: datetime, stopTime: datetime):
        self.project = project
        self.startTime = startTime
        self.stopTime = stopTime
        self.totalTime = self.stopTime - self.startTime

class TimerApp:
    def __init__(self):
        self.sessions = []
        self.running = False
        self.startTime = None
        self.elapsedTime = timedelta()
        self.total_seconds = 0
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        #create tk instance
        self.root = tk.Tk()
        #create font
        self.entryFont = tkfont.Font(self.root, weight=tkfont.BOLD)
        #create tk variables
        self.sessionFrame = tk.Frame(self.root)
        self.sessionProjectLabels = []
        self.sessionTimeLabels = []
        self.projectLabel = tk.Label(self.root, text='Project: ', font=self.entryFont)
        self.projectVar = tk.StringVar(self.root)
        self.projectEntry = tk.Entry(self.root, textvariable=self.projectVar)
        self.timeString = tk.StringVar(self.root, value='{:02d}h {:02d}m {:02d}s'.format(self.hours, self.minutes, self.seconds))
        self.timeLabel = tk.Label(self.root, textvariable=self.timeString, width=12, anchor='w', font=self.entryFont)
        self.startStopButton = tk.Button(self.root, text="Start", command=self.start)
        #bind enter key
        self.root.bind('<Return>', self.start)
        #run app
        self.runApp()
    def start(self, event=None):
        self.startStopButton.configure(text="Stop", command=self.stop)
        self.root.bind('<Return>', self.stop)
        self.projectEntry.configure(state=tk.DISABLED)
        self.startTime = datetime.now()
        self.running = True
        self.update()
    def stop(self, event=None):
        self.root.bind('<Return>', self.start)
        self.startStopButton.configure(text="Start", command=self.start)
        self.sessions[:0] = [Session(self.projectVar.get(), self.startTime, datetime.now())]
        self.sessionProjectLabels[:0] = [tk.Label(self.sessionFrame, 
                                                 text=self.projectVar.get(), 
                                                 width=17, 
                                                 anchor='w'
                                                 )]
        total_seconds = self.sessions[0].totalTime.total_seconds()
        self.sessionTimeLabels[:0] = [tk.Label(self.sessionFrame, 
                                              text=timeString(total_seconds), 
                                              width=17, 
                                              anchor='w'
                                              )]
        for index in range(len(self.sessionProjectLabels)):
            self.sessionProjectLabels[index].grid(row=index, column=0)
            self.sessionTimeLabels[index].grid(row=index, column=1)
        self.running = False
        self.projectEntry.configure(state=tk.NORMAL)
    def update(self):
        if self.running:
            self.elapsedTime = datetime.now() - self.startTime
        else:
            self.elapsedTime = timedelta()
        self.total_seconds = self.elapsedTime.total_seconds()
        self.timeString.set(timeString(self.total_seconds))
        #schedule the update function
        self.root.after(16, self.update)
    def runApp(self):
        #set title, icon
        self.root.title("TimeTracker " + VERSION)
        directory = os.path.dirname(__file__)
        iconpath = os.path.join(directory, 'time_icon.ico')
        self.root.iconbitmap(iconpath)
        #arrange window
        self.root.grid()
        self.projectLabel.grid(row=0, column=0, pady=4)
        self.projectEntry.grid(row=0, column=1, pady=4)
        self.timeLabel.grid(row=0, column=2, pady=4)
        self.startStopButton.grid(row=0, column=3, pady=4)
        self.sessionFrame.grid(row=1, column=1, columnspan=2)
        #run app
        self.root.mainloop()
def main():
    TimerApp()

def timeString(total_seconds: int) -> str:
    seconds = int(total_seconds % 60)
    minutes = int((total_seconds // 60) % 60)
    hours = int(total_seconds // 3600)
    return "{:02d}h {:02d}m {:02d}s".format(hours, minutes, seconds)

if __name__ == "__main__":
    main()