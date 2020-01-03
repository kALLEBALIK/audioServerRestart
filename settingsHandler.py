import json

class SettingsHandler:
    """ Manages settings """
    def __init__(self, settings, logr=False):
        self.cachedError = []
        self.logr = logr
        if isinstance(settings, str):
            self.settings = self._readJson(settings)
        else:
            self.settings = settings

    def attatchLogger(self, logr):
        self.logr = logr
        for err in self.cachedError:
            logr.writeEntry(err)

    def match(self, _settings):
        """ match custom settings and default settings using merge """
        source = self._readJson(_settings)
        if source == FileNotFoundError:
            self.log("No settings file provided, using default.")
            source = {}
        if source == json.decoder.JSONDecodeError:
            self.log("Can't decode settings file, using default.")
            source = {}
        destination = self.settings
        self.settings = SettingsHandler.merge(source, destination)

    @staticmethod
    def merge(source, destination):
        """ deep merge of dicts """
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                SettingsHandler.merge(value, node)
            else:
                destination[key] = value
        return destination

    def log(self, str):
        if self.logr:
            self.logr.writeEntry(str)
        else:
            self.cacheError(str)

    def cacheError(self, str):
        self.cachedError.append(str)

    def _readJson(self, file):
        """ read json file """
        try:
            with open(file + '.json', 'r') as jfile:
                return json.loads(jfile.read())
        except FileNotFoundError:
            return FileNotFoundError
        except json.decoder.JSONDecodeError:
            return json.decoder.JSONDecodeError
