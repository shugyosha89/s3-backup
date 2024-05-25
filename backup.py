import os
import subprocess
import tarfile
import boto3
import yaml
import shutil
from datetime import datetime
import logzero
from logzero import logger

class S3Backup:
    def __init__(self, config_path='config.yml'):
        self.config = self.load_config(config_path)
        self.settings = self.config['settings']
        self.tmp_dir = self.settings['tmp_dir']
        self.log_file = self.settings['log_file']
        self.s3_bucket = self.settings['s3_bucket']
        self.s3_path_prefix = self.settings.get('s3_path_prefix', '')
        self.storage_class = self.settings.get('storage_class', 'STANDARD')
        self.date_format = self.settings['date_format']
        self.local_dirs = self.config['local_dirs']
        self.remote_dirs = self.config['remote_dirs']
        self.s3_client = boto3.client('s3')
        os.makedirs(self.tmp_dir, exist_ok=True)
        self.setup_logging()

    def load_config(self, path):
        with open(path, 'r') as config_file:
            return yaml.safe_load(config_file)

    def setup_logging(self):
        log_level = self.settings.get('log_level', 'INFO').upper()
        logzero.loglevel(getattr(logzero.logging, log_level, logzero.logging.INFO))
        logzero.logfile(self.log_file, maxBytes=1e6, backupCount=3)

    def backup(self, dir_path, tar_file_path):
        with tarfile.open(tar_file_path, "w:gz") as tar:
            tar.add(dir_path, arcname=os.path.basename(dir_path))
        logger.debug(f"Created tarball of {dir_path} at {tar_file_path}")

    def upload(self, tar_file_path):
        try:
            current_date = datetime.now().strftime(self.date_format)
            s3_key = f"{self.s3_path_prefix}{current_date}/{os.path.basename(tar_file_path)}-{current_date}.tar.gz"
            logger.debug(f"Uploading {tar_file_path} to S3 bucket {self.s3_bucket} with key {s3_key} and storage class {self.storage_class}")
            self.s3_client.upload_file(
                tar_file_path, self.s3_bucket, s3_key,
                ExtraArgs={'StorageClass': self.storage_class}
            )
            logger.info(f"{tar_file_path} uploaded successfully.")
            os.remove(tar_file_path)
        except Exception as e:
            logger.error(f"Upload of {tar_file_path} to S3 failed: {str(e)}")

    def backup_local_dirs(self):
        for name, dir_path in self.local_dirs.items():
            tar_file_path = os.path.join(self.tmp_dir, f"{name}-{datetime.now().strftime(self.date_format)}.tar.gz")
            logger.debug(f"Starting backup of local directory {dir_path}")
            self.backup(dir_path, tar_file_path)
            self.upload(tar_file_path)

    def backup_remote_dirs(self):
        for name, remote in self.remote_dirs.items():
            remote_host, remote_path = remote.split(':')
            local_copy_path = os.path.join(self.tmp_dir, f"{name}-{datetime.now().strftime(self.date_format)}")

            logger.debug(f"Starting backup of remote directory {remote}")
            scp_command = ["scp", "-r", f"{remote_host}:{remote_path}", local_copy_path]
            result = subprocess.run(scp_command, capture_output=True, text=True)

            if result.returncode == 0:
                tar_file_path = os.path.join(self.tmp_dir, f"{name}-{datetime.now().strftime(self.date_format)}.tar.gz")
                self.backup(local_copy_path, tar_file_path)
                self.upload(tar_file_path)
                shutil.rmtree(local_copy_path)
            else:
                logger.error(f"Failed to copy {remote}: {result.stderr}")

    def clean_up(self):
        if os.path.exists(self.tmp_dir):
            logger.debug(f"Cleaning up temporary directory {self.tmp_dir}")
            shutil.rmtree(self.tmp_dir)

    def run(self):
        logger.info("Starting S3 backup process")
        self.backup_local_dirs()
        self.backup_remote_dirs()
        self.clean_up()
        logger.info("S3 backup process completed")

if __name__ == "__main__":
    backup_script = S3Backup()
    backup_script.run()
