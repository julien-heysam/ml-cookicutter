import logging
 
import requests
from requests.exceptions import RequestException

from src import PROJECT_ENVS
from src.infrastructure.email.base import EmailManager, EmailMessage

logger = logging.getLogger(__name__)


class EmailMailgun(EmailManager):

    def __init__(self, api_key: str, domain: str):
        self.api_key = api_key
        self.domain = domain
        self.base_url = f"https://api.mailgun.net/v3/{domain}"

    def send_email(self, message: EmailMessage) -> bool:
        try:
            files = None
            if message.attachment_path:
                if not message.attachment_path.exists():
                    logger.warning(f"Attachment not found: {message.attachment_path}")
                else:
                    with open(message.attachment_path, "rb") as f:
                        files = [("attachment", f)]

            response = requests.post(
                f"{self.base_url}/messages",
                auth=("api", self.api_key),
                data=message.to_dict(),
                files=files,
            )
            response.raise_for_status()
            logger.info("Email sent successfully", extra={"message": message.to_dict()})
            return True

        except RequestException as e:
            logger.error("Failed to send email", extra={"error": str(e), "message": message.to_dict()}, exc_info=PROJECT_ENVS.DEBUG)
            return False
