from pathlib import Path
from datetime import datetime

class Logger:
    def __init__(self, name='log'):
        self.LOGPATH = Path.cwd()
        self.LOGFILENAME = Path(name + '.txt')
        self.LOGFILE = self.LOGPATH / self.LOGFILENAME

        self.log = {
            "print": True,
            "write": True,
        }

        self.sessionIsActive = False
        self.LogFileObject = {}
    
    def __writeLine(self, line):
        self.LogFileObject.write(str(line) + '\n')
        self.LogFileObject.flush()

    def __del__(self):
        if (self.sessionIsActive):
            self.endSession()

    def timeString(self):
        return datetime.now().strftime("%H:%M:%S")

    def dateString(self):
        return str(datetime.now().date())

    def beginSession(self):
        string = '------ Beginning session '+ self.dateString() + ' ' + self.timeString() +' ------'
        if self.log['write']:
            self.LogFileObject = open(self.LOGFILE, "a+")
            self.sessionIsActive = True
            self.__writeLine(string)

        if self.log['print']:
            print(string)

    def writeEntry(self, entry): 
        current_time = self.timeString()
        string = current_time + ': ' + str(entry).replace('\n', '\n\t  ')
        if self.sessionIsActive:
            self.__writeLine(string)

        if self.log['print']:
            print(string)

    def endSession(self):
        string = '------ Ending session -----------------------------'
        if self.sessionIsActive:
            self.__writeLine(string)
            self.LogFileObject.close()
        self.sessionIsActive = False

        if self.log['print']:
            print(string)