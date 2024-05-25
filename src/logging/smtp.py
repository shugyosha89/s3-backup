import smtplib
from logzero import logger
from src.logging.driver import LogDriver
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SmtpLogDriver(LogDriver):
    def __init__(self, name, config):
        self._name = name
        self._host = config['host']
        self._port = config['port']
        self._to_email = config['to_email']
        self._from_email = config['from_email']
        self._to_name = config['to_name'] if 'to_name' in config else None
        self._from_name = config['from_name'] if 'from_name' in config else None
        self._username = config['username'] if 'username' in config else None
        self._password = config['password'] if 'password' in config else None
        self._encryption = config['encryption'] if 'encryption' in config else None
        self._level = config.get('level', 'INFO').upper()

    def _get_mailbox(self, name, email):
        return f'"{name}" <{email}>' if name else email

    def _get_email(self, message, level):
        msg = MIMEMultipart()
        msg['To'] = self._get_mailbox(self._to_name, self._to_email)
        msg['From'] = self._get_mailbox(self._from_name, self._from_email)
        msg['Subject'] = f"S3 Backup ({level.lower()})"
        msg.attach(MIMEText(message, 'plain'))
        return msg

    def _handle_auth(self, server):
        if self._encryption and self._encryption.lower() == 'tls':
            server.starttls()
        if self._username and self._password:
            server.login(self._username, self._password)

    def _send_mail(self, message, level):
        if self._name:
            message = f"{self._name}: {message}"
        msg = self._get_email(message, level)
        server = smtplib.SMTP(self._host, self._port)
        self._handle_auth(server)
        server.sendmail(self._from_email, self._to_email, msg.as_string())
        server.quit()
        logger.debug(f"Email sent to {self._to_email} with message: {message}")

    def log(self, message, level):
        if not self._should_log(level, self._level):
            return
        try:
            self._send_mail(message, level)
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
