import logging
from pathlib import Path
from typing import List, Optional
from abc import ABC, abstractmethod

from pydantic import BaseModel, EmailStr, validator

logger = logging.getLogger(__name__)


class EmailMessage(BaseModel):
    subject: str
    from_email: EmailStr
    to_emails: List[EmailStr]
    html: str
    text: Optional[str] = None
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None
    attachment_path: Optional[Path] = None

    @validator('from_email')
    def validate_from_email(cls, email):
        if '@' not in email:
            raise ValueError("From email must contain '@' symbol")
        return email

    @validator('to_emails')
    def validate_to_emails(cls, emails):
        if not emails:
            raise ValueError("At least one recipient email is required")
        if any('@' not in email for email in emails):
            raise ValueError("All recipient emails must contain '@' symbol")
        return emails

    @validator('html')
    def validate_html_content(cls, html):
        if not html.strip():
            raise ValueError("HTML content cannot be empty")
        return html

    @validator('attachment_path')
    def validate_attachment_path(cls, path):
        if path and not path.exists():
            raise ValueError(f"Attachment file does not exist: {path}")
        return path

    def to_dict(self) -> dict:
        data = {
            "from": self.from_email,
            "to": ",".join(self.to_emails),
            "subject": self.subject,
            "html": self.html,
        }
        if self.text:
            data["text"] = self.text
        if self.cc:
            data["cc"] = ",".join(self.cc)
        if self.bcc:
            data["bcc"] = ",".join(self.bcc)
        return data


class EmailManager(ABC):

    @abstractmethod
    def send_email(self, message: EmailMessage) -> bool:
        ...
