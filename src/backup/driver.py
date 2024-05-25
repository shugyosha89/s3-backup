import subprocess

class BackupDriver:
    def backup(self, date_format, tmp_dir):
        raise NotImplementedError("Backup driver must implement the backup method.")

    def _make_tar(self, dir_path, tar_path, exclude=None):
        exclude_args = []
        if exclude:
            exclude_args.extend(f"--exclude={pattern}" for pattern in exclude)
        tar_command = ["tar", *exclude_args, *["-czf", tar_path, "-C", dir_path, "."]]
        try:
            result = subprocess.run(tar_command, capture_output=True, text=True, check=True)
            self._logger.debug(result.stdout)
            if result.stderr:
                self._logger.warning(result.stderr)
            return tar_path
        except subprocess.CalledProcessError as e:
            self._logger.error(f"Tar command failed with return code {e.returncode}")
            self._logger.error(e.stderr)
            raise
