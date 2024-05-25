# S3 Backup

A Python script for backing up local and remote directories to Amazon S3. The script reads configuration from a YAML file, creates tarball backups of specified directories, uploads them to an S3 bucket, and logs all operations.

## Features

- Back up both local and remote files to S3
- Supports different S3 storage classes
- Receive notifications by email and Slack

## Prerequisites

- Python 3.x
- AWS CLI configured profile

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/shugyosha89/s3-backup.git
   ```

2. **Install requirements**

   ```sh
   pip install -r requirements.txt
   ```

3. **Set your configuration**

    Create a `config.yml` file with your chosen settings.

4. **Run the script**

   ```sh
   python main.py
   ```

   Make sure to run it as a user with the privileges to read and write from the configured locations.

## Configuration

See [config.yml.example](config.yml.example) for a complete example configuration.

### Settings

General script settings.

* `name`: Prepended to log output. Useful if you run the script on more than one machine. Optional.
* `tmp_dir`: Location to archive files before uploading them. Default: `tmp`. Optional.
* `date_format`: Date format to use in archive file names. Default: `%Y-%m-%d`. Optional.

#### Example
```
settings:
  name: S3 Backup
  tmp_dir: tmp
  date_format: "%Y-%m-%d"
```
### S3

S3 upload destination settings.

* `bucket`: Name of the bucket to upload to. Required.
* `path_prefix`: Prefix to append to S3 keys when uploading files. Default: None. Optional.
* `storage_class`: Storage class to use when uploading to S3. Default: `STANDARD`. Optional.
* `aws_profile`: Name of the AWS profile to use when uploading to S3. Default: uses your default profile. Optional.

  Available values: `STANDARD`, `INTELLIGENT_TIERING`, `STANDARD_IA`, `ONEZONE_IA`, `GLACIER`, `DEEP_ARCHIVE`, `REDUCED_REDUNDANCY`.

#### Example
```
s3:
  bucket: my-bucket
  path_prefix: backups/
  storage_class: STANDARD
  aws_profile: default
```

### Backups

List of target directories or files to backup.

#### Common settings

* `name`: File name of the archive file to create. Required.
* `driver`: How to access the files to back up. Required.

  Available values: `local`, `ssh`

* `path`: Path to the file or directory to back up. Required.

#### SSH driver settings
* `key`: Path to identity key file to use. Optional.
* `port`: Port to connect to remote machine on. Optional.


#### Example
```
backups:
  - name: documents
    driver: local
    path: /home/user/Documents

  - name: work
    driver: ssh
    path: user@machine:~/Documents/Work
    key: /home/user/.ssh/id_rsa
    port: 22
```

### Loggers
Loggers allow logging the output of the script to different services.

#### Common settings

* `driver`: How to log program output. Required.

  Available values: `file`, `slack`, `email`

* `level`: Minimum log level to output. Default value: `INFO`. Optional.

#### File driver settings
* `path`: Path to the log file. Required.

#### Slack driver settings
* `webhook_url`: Your Slack webhook URL. Required.
* `prepend`: Prepend text to log messages. Useful for tagging people. Optional.
* `prepend_level`: Minimum log level to prepend the `prepend` text to. Optional. Default: `INFO`.

#### Email driver settings
* `host`: SMTP host address. Required.
* `port`: SMTP host port. Required.
* `username`: Account username. Optional.
* `password`: Account password. Optional.
* `from_name`: Name of the sender. Optional.
* `from_email`: Email address of the sender. Required.
* `to_name`: Name of the recipient. Optional.
* `to_email`: Email address of the recipient. Required.
* `encryption`: Encryption method to use. Optional. Default: None.

  Available values: `tls` for STARTTLS.

#### Example
```
loggers:
  - driver: file
    path: s3-backup.log
    level: DEBUG

  - driver: slack
    webhook_url: https://hooks.slack.com/services/my-webhook
    level: INFO
    prepend: "@here"
    prepend_level: ERROR

  - driver: email
    host: smtp.example.com
    port: 587
    username: smtp-user
    password: smtp-password
    from_name: S3 Backup
    from_email: s3-backup@example.com
    to_name: My Name
    to_email: my-email@example.com
    encryption: "tls"
    level: "ERROR"
```

## Tips
* Add the script to your `crontab` to automate backups.
* Edit your bucket settings in AWS Console to control how long backup files are kept for.
