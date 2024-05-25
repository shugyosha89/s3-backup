from src.logging.file import FileLogDriver
from src.logging.slack import SlackLogDriver
from src.logging.smtp import SmtpLogDriver

class LoggingManager:
    _DRIVERS = {
        'file': FileLogDriver,
        'slack': SlackLogDriver,
        'email': SmtpLogDriver,
    }

    def __init__(self, name, loggers):
        self._name = name
        self._drivers = []
        if not loggers:
            return
        for logger_config in loggers:
            driver = logger_config['driver']
            if driver not in self._DRIVERS:
                raise ValueError(f"Unsupported logging driver: {driver}")
            driver_class = self._DRIVERS[driver]
            self._drivers.append(driver_class(name, logger_config))

    def log(self, message, level):
        for driver in self._drivers:
            driver.log(message, level)

    def debug(self, message):
        self.log(message, 'DEBUG')

    def info(self, message):
        self.log(message, 'INFO')

    def warning(self, message):
        self.log(message, 'WARNING')

    def error(self, message):
        self.log(message, 'ERROR')

    def critical(self, message):
        self.log(message, 'CRITICAL')
