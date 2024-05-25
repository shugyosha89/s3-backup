class LogDriver:

    def _should_log(self, level, driver_level):
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        return levels.index(level.upper()) >= levels.index(driver_level)

    def log(self, message, severity):
        raise NotImplementedError("Log driver must implement the log method.")

    def debug(self, message):
        raise self.log(message, "DEBUG")

    def info(self, message):
        raise self.log(message, "INFO")

    def warning(self, message):
        raise self.log(message, "WARNING")

    def error(self, message):
        raise self.log(message, "ERROR")

    def critical(self, message):
        raise self.log(message, "CRITICAL")
