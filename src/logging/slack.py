import requests
from logzero import logger
from src.logging.driver import LogDriver

class SlackLogDriver(LogDriver):
    def __init__(self, name, config):
        self._name = name
        self._level = config.get('level', 'INFO').upper()
        self._webhook_url = config['webhook_url']
        self._prepend = config.get('prepend', None)
        self._prepend_level = config.get('prepend_level', self._level).upper()

    def log(self, message, level):
        if not self._should_log(level, self._level):
            return
        try:
            formatted_message = self._format_message(message, level)
            response = requests.post(
                self._webhook_url, json=formatted_message,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code != 200:
                logger.error(f"Failed to send Slack notification: {response.status_code}, {response.text}")
        except Exception as e:
            logger.error(f"Exception occurred while sending Slack notification: {str(e)}")

    def _format_message(self, message, level):
        unformatted_message = message
        color = self.get_color(level)
        if self._prepend and self._should_log(level, self._prepend_level):
            message = f"{self._prepend}\n{message}"
        message = f"{level.upper()}: {message}"
        if self._name:
            message = f"*{self._name}*\n{message}"
        return {
            "text": unformatted_message,
            "attachments": [
                {
                    "color": color,
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": message,
                            }
                        }
                    ]
                }
            ]
        }

    def get_color(self, level):
        colors = {
            "DEBUG": "#3439FE",    # Blue
            "INFO": "#06a64f",     # Green
            "WARNING": "#FF9F00",  # Orange
            "ERROR": "#DC3545",    # Red
            "CRITICAL": "#8B0000"  # Dark Red
        }
        return colors.get(level.upper(), colors['INFO'])
