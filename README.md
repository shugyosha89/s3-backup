# S3 Backup

A Python script for backing up local and remote directories to Amazon S3. The script reads configuration from a YAML file, creates tarball backups of specified directories, uploads them to an S3 bucket, and logs all operations.

## Features

- Configurable directories for local and remote backups
- Supports different S3 storage classes
- Organizes backups with date-based prefixes in S3
- Logs operations using `logzero` for easy debugging and monitoring

## Prerequisites

- Python 3.x
- AWS CLI configured with appropriate credentials

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/shuygyosha89/s3-glacier-backup.git
   ```

2. **Install requirements**

   ```sh
   pip install -r requirements.txt
   ```

3. **Set your configuration**

    Create a `config.yml` file with your chosen settings.

    See `config.yml.example` for an example with a description of the settings.

4. **Run the script**

   ```sh
   python backup.py
   ```

   Make sure to run it as a user with the privileges to write to the log file location and temp directory.


## Tips
* Add the script to your `crontab` to automate backups.
* Edit your bucket settings in AWS Console to control how long backup files are kept for.
