import json
import logging

import requests

from src import PROJECT_ENVS
from src.constants import Envs

logger = logging.getLogger(__name__)


class SlackNotifier:
    def __init__(self, webhook_url: str, default_metadata: dict = None):
        """
        Initialize a generic Slack notifier.
        
        Args:
            webhook_url: Slack webhook URL for sending messages
            default_metadata: Optional default metadata to include in all messages
        """
        self.webhook_url = webhook_url
        self.default_metadata = default_metadata or {}

    def _send_to_slack(self, payload: dict):
        if PROJECT_ENVS.ENV_STATE == Envs.PROD.value:
            headers = {"Content-Type": "application/json"}
            response = requests.post(self.webhook_url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                logger.debug("Message sent to Slack successfully.")
            else:
                logger.warning(
                    f"Failed to send message to Slack. Status code: {response.status_code}, Response: {response.text}"
                )
        else:
            logger.info(payload)

    def post_message(self, message: str, metadata: dict = None):
        """Post a normal progress message to Slack."""
        combined_metadata = {**self.default_metadata, **(metadata or {})}
        metadata_text = "\n".join(f"*{k}:* {v}" for k, v in combined_metadata.items())
        
        payload = {
            "text": message,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{metadata_text}\n\n{message} :gear:" if metadata_text else f"{message} :gear:",
                    },
                }
            ],
        }
        self._send_to_slack(payload)

    def post_warning(self, message: str, metadata: dict = None):
        """Post a warning message to Slack."""
        combined_metadata = {**self.default_metadata, **(metadata or {})}
        metadata_text = "\n".join(f"*{k}:* {v}" for k, v in combined_metadata.items())
        
        payload = {
            "text": message,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": metadata_text,
                    },
                },
                {
                    "type": "section",
                    "block_id": "section_warning",
                    "fields": [{"type": "mrkdwn", "text": f":warning: ```{message}```"}],
                },
            ],
        }
        self._send_to_slack(payload)

    def post_error(self, error: str, metadata: dict = None, help_link: str = None):
        """Post an error message to Slack."""
        combined_metadata = {**self.default_metadata, **(metadata or {})}
        metadata_text = "\n".join(f"*{k}:* {v}" for k, v in combined_metadata.items())
        
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": metadata_text,
                },
            },
            {
                "type": "section",
                "block_id": "section_error",
                "fields": [{"type": "mrkdwn", "text": f":boom: *Error Occurred:*\n```{error}```"}],
            },
        ]

        if help_link:
            blocks.append({
                "type": "section",
                "block_id": "section_help",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<{help_link}|Click here> for more details or troubleshooting.",
                },
            })

        payload = {
            "text": error,
            "blocks": blocks,
        }
        self._send_to_slack(payload)


if __name__ == "__main__":
    notifier = SlackNotifier("bot_id_123", "data_processing_task", "https://hooks.slack.com/services/...")
    notifier.post_message("Data processing started successfully. Monitoring the task.")
    notifier.post_error("Bot ID not found during execution.")
