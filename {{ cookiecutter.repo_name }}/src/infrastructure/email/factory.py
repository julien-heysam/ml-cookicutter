from enum import Enum
from typing import Optional

from src.infrastructure.factory import FactoryError
from src.infrastructure.email.base import EmailManager
from src.infrastructure.email._smtp import EmailSMTP
from src.infrastructure.email._mailgun import EmailMailgun


class EmailProviderType(Enum):
    SMTP = "smtp"
    MAILGUN = "mailgun"


class EmailFactory:
    REQUIRED_PARAMS: dict[EmailProviderType, set[str]] = {
        EmailProviderType.SMTP: {"smtp_host", "smtp_port", "username", "password"},
        EmailProviderType.MAILGUN: {"api_key", "domain"}
    }

    @classmethod
    def validate_params(cls, provider_type: EmailProviderType, params: dict) -> None:
        required_params = cls.REQUIRED_PARAMS[provider_type]
        missing_params = required_params - set(params.keys())
        
        if missing_params:
            raise ValueError(
                f"Missing required parameters for {provider_type.value}: {', '.join(missing_params)}"
            )
        
    @classmethod
    def create(cls, provider_type: EmailProviderType, **kwargs) -> Optional[EmailManager]:
        if not isinstance(provider_type, EmailProviderType):
            raise ValueError(f"Invalid provider type. Must be one of: {[t.value for t in EmailProviderType]}")

        cls.validate_params(provider_type, kwargs)
        if provider_type == EmailProviderType.MAILGUN:
            return EmailMailgun(api_key=kwargs["api_key"], domain=kwargs["domain"])
        elif provider_type == EmailProviderType.SMTP:
            return EmailSMTP(
                smtp_host=kwargs["smtp_host"],
                smtp_port=kwargs["smtp_port"],
                username=kwargs["username"],
                password=kwargs["password"]
            )
        raise FactoryError(f"No factory registered for provider type '{provider_type}'")
