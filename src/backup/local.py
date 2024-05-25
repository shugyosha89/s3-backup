import os
from datetime import datetime

from src.backup.driver import BackupDriver

class LocalBackupDriver(BackupDriver):
    def __init__(self, config, logger):
        self._name = config['name']
        self._path = config['path']
        self._logger = logger

    def backup(self, date_format, tmp_dir):
        tar_name = f"{self._name}-{datetime.now().strftime(date_format)}.tar.gz"
        tar_path = os.path.join(tmp_dir, tar_name)
        self._make_tar(self._path, tar_path)
        self._logger.debug(f"Created tarball of {self._path} at {tar_path}")
        return tar_path
