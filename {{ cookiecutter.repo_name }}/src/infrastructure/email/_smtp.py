import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from src import PROJECT_ENVS
from src.infrastructure.email.base import EmailManager, EmailMessage

logger = logging.getLogger(__name__)


class EmailSMTP(EmailManager):
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, message: EmailMessage) -> bool:
        try:
            # Create MIME message
            mime_message = MIMEMultipart()
            mime_message["From"] = message.from_email
            mime_message["To"] = message.to_email
            mime_message["Subject"] = message.subject

            # Attach body
            mime_message.attach(MIMEText(message.body, "html" if message.html else "plain"))

            # Attach file if provided
            if message.attachment_path and message.attachment_path.exists():
                with open(message.attachment_path, "rb") as f:
                    attachment = MIMEApplication(f.read())
                    attachment.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=message.attachment_path.name
                    )
                    mime_message.attach(attachment)
            elif message.attachment_path:
                logger.warning(f"Attachment not found: {message.attachment_path}")

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(mime_message)

            logger.info("Email sent successfully", extra={"message": message.to_dict()})
            return True

        except Exception as e:
            logger.error(
                "Failed to send email",
                extra={"error": str(e), "message": message.to_dict()},
                exc_info=PROJECT_ENVS.DEBUG
            )
            return False
