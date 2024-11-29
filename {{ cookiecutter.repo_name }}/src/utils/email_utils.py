import logging

import requests

from src import API_KEYS, PROJECT_ENVS

logger = logging.getLogger(__name__)


def send_html_email_with_attachment(
    html: str,
    subject: str,
    from_email: str,
    to_emails: list[str],
    text: str = None,
    cc: str = None,
    bcc: str = None,
    file_path: str = None,
) -> bool:
    """
    Send an HTML email with an optional attachment using Mailgun.

    Parameters:
    - html (str): HTML content of the email.
    - subject (str): Subject of the email.
    - from_email (str): Sender's email address.
    - to_email (str): Recipient's email address.
    - text (str, optional): Plain text content of the email.
    - cc (str, optional): CC recipient email addresses.
    - bcc (str, optional): BCC recipient email addresses.
    - file_path (str, optional): Path to the file to attach.
    """
    data = {
        "from": from_email,
        "to": to_emails,
        "subject": subject,
        "html": html,
    }
    if text:
        data["text"] = text
    if cc:
        data["cc"] = cc
    if bcc:
        data["bcc"] = bcc

    files = None
    if file_path:
        try:
            files = [("attachment", open(file_path, "rb"))]
        except FileNotFoundError:
            logger.warning(f"Error: The file at {file_path} was not found.")

    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{API_KEYS.MAILGUN_DOMAIN}/messages",
            auth=("api", API_KEYS.MAILGUN_API_KEY),
            data=data,
            files=files,
        )
        response.raise_for_status()
        logger.info("Email sent successfully!")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send email. Error: {e}", extra={"error": e}, exc_info=PROJECT_ENVS.DEBUG)
        return False
