import time
import json
from logger import Logger
from settingsHandler import SettingsHandler
from service import Service
from winlog import Winlog
from defaultSettings import SETTINGS

def restartAudio(logr, srvc):
    if not srvc.isRunning(srvc.AUDIOSRV) or not srvc.isRunning(srvc.AUDIOENDPOINTBUILDER):
        logr.writeEntry('Audio Services not running, starting them...')
        srvc.netStart(srvc.AUDIOSRV)

    AudiosrvProcessKilled = srvc.killService(srvc.AUDIOSRV)
    AudioEndpointBuilderProcessKilled = srvc.killService(srvc.AUDIOENDPOINTBUILDER)

    if AudiosrvProcessKilled:
        srvc.netStart(srvc.AUDIOSRV)
    elif AudioEndpointBuilderProcessKilled:
        srvc.netStart(srvc.AUDIOENDPOINTBUILDER)


def main():
    sets = SettingsHandler(SETTINGS)
    sets.match('settings')

    logr = Logger('audioServerRestart_log')
    logr.log = sets.settings['log']
    logr.beginSession()

    sets.attatchLogger(logr)

    srvc = Service(logr)
    wnlg = Winlog(logr)

    logr.writeEntry('"settings:" \n' + str(json.dumps(sets.settings, indent=4)))

    running = False
    if sets.settings['run-style'] == 'continuously':
        logr.writeEntry('Starting. Running continuously...')
        running = True
    else:
        restartAudio(logr, srvc)

    runs = 0
    if running:
        logr.writeEntry('Checking Windows logs...')
    while running:
        if runs % 10 == 0:
            logr.writeEntry('Still checking Windows logs...')
        if wnlg.didWakeup(sets.settings['event-time-diff']):
            restartAudio(logr, srvc)
        time.sleep(sets.settings['event-timeout'])
        runs += 1

    logr.endSession()

if __name__ == '__main__':
    main()
