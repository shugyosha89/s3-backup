from src.s3_backup import S3Backup

if __name__ == "__main__":
    backup_script = S3Backup('config.yml')
    backup_script.run()
