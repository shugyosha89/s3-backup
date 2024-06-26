import boto3
import os
from datetime import datetime

class S3Manager:
    def __init__(self, name, date_format, config, logger):
        self._name = name
        self._date_format = date_format
        self._logger = logger
        self._bucket = config['bucket']
        self._path_prefix = config.get('path_prefix', '')
        self._storage_class = config.get('storage_class', 'STANDARD')
        session = boto3.Session(profile_name=config.get('profile', 'default'))
        self._client = session.client('s3')

    def upload_all(self, files):
        all_keys = []
        for file_path in files:
            s3_key = f"{self._path_prefix}{os.path.basename(file_path)}"
            s3_key = s3_key.replace('{date}', datetime.now().strftime(self._date_format))
            s3_key = s3_key.replace('{name}', self._name or '')
            if self.try_upload(file_path, s3_key):
                all_keys.append(s3_key)
        return all_keys

    def try_upload(self, tar_path, s3_key):
        try:
            self.upload(tar_path, s3_key)
        except Exception as e:
            self._logger.error(f"Upload of {tar_path} to S3 failed: {str(e)}")
            return False
        return True

    def upload(self, file_path, s3_key):
        self._logger.debug(f"Uploading {file_path} to S3 bucket {self._bucket} with key {s3_key} and storage class {self._storage_class}")
        self._client.upload_file(
            file_path, self._bucket, s3_key,
            ExtraArgs={'StorageClass': self._storage_class}
        )
        self._logger.debug(f"Uploaded {s3_key}")
