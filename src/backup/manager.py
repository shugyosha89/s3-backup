from src.backup.local import LocalBackupDriver
from src.backup.ssh import SshBackupDriver

class BackupManager:
    _DRIVERS = {
        'local': LocalBackupDriver,
        'ssh': SshBackupDriver,
    }

    def __init__(self, date_format, tmp_dir, backups, logger):
        self._date_format = date_format
        self._tmp_dir = tmp_dir
        self._logger = logger
        self._drivers = []
        if not backups:
            return
        for backup_config in backups:
            driver = backup_config['driver']
            if driver not in self._DRIVERS:
                raise ValueError(f"Unsupported backup driver: {driver}")
            driver_class = self._DRIVERS[driver]
            self._drivers.append(driver_class(backup_config, logger))

    def backup(self):
        return [
            driver.backup(self._date_format, self._tmp_dir)
            for driver in self._drivers
        ]
