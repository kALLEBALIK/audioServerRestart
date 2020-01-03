import psutil
import os
from logger import Logger

class Service:
    AUDIOSRV = 'Audiosrv'
    AUDIOENDPOINTBUILDER = 'AudioEndpointBuilder'

    def __init__(self, logger):
        self.logger = logger

    def getService(self, service):
        try:
            serv = psutil.win_service_get(service)
        except (psutil.NoSuchProcess):
            self.logger.writeEntry('Could not find '+service+' process')
            return False
        return serv

    def killService(self, serviceName):
        service = self.getService(serviceName)
        if service:
            proc = psutil.Process(service.pid())
            if proc.is_running():
                self.logger.writeEntry('Terminating ' + service.name())
                proc.kill()
                proc.wait()
                return True
        return False

    def serviceStatus(self, serviceName):
        service = self.getService(serviceName)
        if service:
            proc = psutil.Process(service.pid())
            return proc.status()
        return False

    def netStart(self, toStart):
        self.logger.writeEntry('Starting service: '+ toStart + '...')
        cmd = 'net start ' + toStart
        output = os.popen(cmd).read()
        self.logger.writeEntry(output)

    def isRunning(self, serviceName):
        service = self.getService(serviceName)
        if service:
            proc = psutil.Process(service.pid())
            return proc.is_running()
        return False