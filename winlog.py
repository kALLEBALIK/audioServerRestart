from datetime import datetime, date
import win32evtlog

class Winlog:
    """ Looking at windows event logs """
    server = 'localhost'
    logtype = 'System'
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ

    latestWakeupAction = datetime(1970, 1, 1)
    def __init__(self, logger):
        self.logr = logger

    def didWakeup(self, timeDiff):
        """ Check if computer wokeup in the latest x amount of seconds """
        hand = win32evtlog.OpenEventLog(self.server, self.logtype)
        # total = win32evtlog.GetNumberOfEventLogRecords(hand)
        while True:
            events = win32evtlog.ReadEventLog(hand, self.flags, 0)
            if events:
                for event in events:
                    if event.EventID == 42:
                        duration = datetime.now() - event.TimeGenerated
                        passed = duration.total_seconds()
                        if self.latestWakeupAction < event.TimeGenerated and passed < timeDiff:
                            self.logr.writeEntry('Found wakeup TimeGenerated: ' + str(event.TimeGenerated))
                            self.latestWakeupAction = event.TimeGenerated
                            return True
            else:
                return False

# event.EventCategory
# event.TimeGenerated
# event.SourceName
# event.EventID
# event.EventType
# data = event.StringInserts
