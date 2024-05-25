import logzero
from logzero import logger
from src.logging.driver import LogDriver

class FileLogDriver(LogDriver):
    def __init__(self, name, config):
        self._name = name
        self._level = config.get('level', 'INFO').upper()
        logzero.loglevel(getattr(logzero.logging, self._level, logzero.logging.INFO))
        logzero.logfile(config['path'], maxBytes=1e6, backupCount=3)

    def log(self, message, level):
        if not self._should_log(level, self._level):
            return
        if self._name:
            message = f"{self._name}: {message}"
        getattr(logger, level.lower())(message)
