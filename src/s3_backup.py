import os
import yaml
import shutil
import time

from src.backup.manager import BackupManager
from src.logging.manager import LoggingManager
from src.s3 import S3Manager

class S3Backup:
    def __init__(self, config_path):
        self._config = self.load_config(config_path)
        self._tmp_dir = self._config.get('settings').get('tmp_dir', 'tmp')
        name = self._config.get('settings').get('name')
        date_format = self._config.get('settings').get('date_format', '%Y-%m-%d')
        self._logger = LoggingManager(name, self._config['loggers'])
        self._backup = BackupManager(date_format, self._tmp_dir, self._config['backups'], self._logger)
        self._s3 = S3Manager(self._config['s3'], self._logger)
        self._logger.debug(f"Running with config:\n{yaml.dump(self._config)}")
        os.makedirs(self._tmp_dir, exist_ok=True)

    def load_config(self, path):
        with open(path, 'r') as config_file:
            return yaml.safe_load(config_file)

    def _clean_up(self):
        if os.path.exists(self._tmp_dir):
            self._logger.debug(f"Deleting temporary directory {self._tmp_dir}")
            shutil.rmtree(self._tmp_dir)

    def run(self):
        try:
            start_time = time.time()
            self._logger.debug("Starting S3 backup process")
            uploaded_keys = self._s3.upload_all(self._backup.backup())
            self._clean_up()
            end_time = time.time()
            time_taken = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))
            self._logger.info(f"Uploaded backups to S3:\n{yaml.dump(uploaded_keys)}\nTime taken: {time_taken}")
        except Exception as e:
            self._logger.critical(f"Backup failed: {str(e)}")
