import os
from datetime import datetime
import shutil
import subprocess
import tarfile

from src.backup.driver import BackupDriver

class SshBackupDriver(BackupDriver):
    def __init__(self, config, logger):
        self._name = config['name']
        self._path = config['path']
        self._port = config['port'] if 'port' in config else 22
        self._key = config['key'] if 'key' in config else None
        self._exclude = config['exclude'] if 'exclude' in config else None
        self._logger = logger

    def _get_command(self, local_copy_path):
        ssh = f"ssh -p {self._port}"
        if self._key is not None:
            ssh += f" -i {self._key}"
        command = ["rsync", "-a"]
        if self._exclude is not None:
            for exclude in self._exclude:
                command.extend(["--exclude", exclude])
        command.extend(["-e", ssh, self._path, local_copy_path])
        return command

    def backup(self, date_format, tmp_dir):
        self._logger.debug(f"Starting backup of remote directory {self._path}")
        backup_name = f"{self._name}-{datetime.now().strftime(date_format)}"
        local_copy_path = os.path.join(tmp_dir, backup_name)

        command = self._get_command(local_copy_path)
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            self._logger.error(f"Failed to execute command : {result.stderr}\nUsing rsync command: {' '.join(command)}")
            return None

        tar_path = os.path.join(tmp_dir, f"{backup_name}.tar.gz")
        self._make_tar(local_copy_path, tar_path)
        shutil.rmtree(local_copy_path)
        return tar_path
