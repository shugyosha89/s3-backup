import tarfile
import os

class BackupDriver:
    def backup(self, date_format, tmp_dir):
        raise NotImplementedError("Backup driver must implement the backup method.")

    def _make_tar(self, dir_path, tar_path):
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(dir_path, arcname=os.path.basename(dir_path))
        self._logger.debug(f"Created tarball of {dir_path} at {tar_path}")
        return tar_path
