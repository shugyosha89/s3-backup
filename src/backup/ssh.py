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
        self._logger = logger

    def _get_scp_command(self, remote_host, remote_path, local_copy_path):
        scp_command = ["scp", "-r"]
        if self._key is not None:
            scp_command.extend(["-i", self._key])
        scp_command.extend(
            [
                "-P",
                str(self._port),
                f"{remote_host}:{remote_path}",
                local_copy_path,
            ]
        )
        return scp_command

    def backup(self, date_format, tmp_dir):
        self._logger.debug(f"Starting backup of remote directory {self._path}")
        remote_host, remote_path = self._path.split(':')
        backup_name = f"{self._name}-{datetime.now().strftime(date_format)}"
        local_copy_path = os.path.join(tmp_dir, backup_name)

        scp_command = self._get_scp_command(remote_host, remote_path, local_copy_path)
        result = subprocess.run(scp_command, capture_output=True, text=True)
        if result.returncode != 0:
            self._logger.error(f"Failed to copy {self._path}: {result.stderr}")
            return None

        tar_path = os.path.join(tmp_dir, f"{backup_name}.tar.gz")
        self._make_tar(local_copy_path, tar_path)
        shutil.rmtree(local_copy_path)
        return tar_path
