import logging
import logging.config
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pythonjsonlogger.jsonlogger import JsonFormatter
from rich.console import Console
from rich.logging import RichHandler

from src.constants import Envs

load_dotenv(override=True)
console = Console()
FAKE_API_KEY: str = "FAKE_API_KEY"


class ApiKeys(BaseSettings):
    ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", FAKE_API_KEY)
    COHERE_API_KEY: str = os.environ.get("COHERE_API_KEY", FAKE_API_KEY)
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", FAKE_API_KEY)
    VOYAGE_API_KEY: str = os.environ.get("VOYAGE_API_KEY", FAKE_API_KEY)
    MIXEDBREAD_API_KEY: str = os.environ.get("MIXEDBREAD_API_KEY", FAKE_API_KEY)
    GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", FAKE_API_KEY)

    PINECONE_API_KEY: str = os.environ.get("PINECONE_API_KEY", FAKE_API_KEY)
    PINECONE_ENV: str = os.environ.get("PINECONE_ENV", None)
    PINECONE_INDEX: str = os.environ.get("PINECONE_INDEX", None)
    PINECONE_INDEX_URL: str = os.environ.get("PINECONE_INDEX_URL", None)

    ALGOLIA_APP_ID: str = os.environ.get("ALGOLIA_APP_ID", None)
    ALGOLIA_SEARCH_API_KEY: str = os.environ.get("ALGOLIA_SEARCH_API_KEY", FAKE_API_KEY)
    ALGOLIA_WRITE_API_KEY: str = os.environ.get("ALGOLIA_WRITE_API_KEY", FAKE_API_KEY)
    ALGOLIA_INDEX: str = os.environ.get("ALGOLIA_INDEX", None)

    APIFY_API_TOKEN: str = os.environ.get("APIFY_API_TOKEN", FAKE_API_KEY)
    BRAVE_API_KEY: str = os.environ.get("BRAVE_API_KEY", FAKE_API_KEY)
    SERPER_API_KEY: str = os.environ.get("SERPER_API_KEY", FAKE_API_KEY)
    GOOGLE_SERPER_API_KEY: str = os.environ.get("GOOGLE_SERPER_API_KEY", FAKE_API_KEY)

    GOOGLE_API_KEY: str = os.environ.get("GOOGLE_API_KEY", FAKE_API_KEY)
    COMET_API_KEY: str = os.environ.get("COMET_API_KEY", FAKE_API_KEY)
    NOTION_API_KEY: str = os.environ.get("NOTION_API_KEY", FAKE_API_KEY)
    OPENWEATHERMAP_API_KEY: str = os.environ.get("OPENWEATHERMAP_API_KEY", FAKE_API_KEY)
    PROMPTLAYER_API_KEY: str = os.environ.get("PROMPTLAYER_API_KEY", FAKE_API_KEY)

    POSTGRES_DATABASE_USERNAME: str = os.environ.get("POSTGRES_DATABASE_USERNAME", "postgres")
    POSTGRES_DATABASE_PASSWORD: str = os.environ.get("POSTGRES_DATABASE_PASSWORD", "postgres")
    POSTGRES_DATABASE_URL: str = os.environ.get("POSTGRES_DATABASE_URL", "127.0.0.1:5432")
    POSTGRES_DATABASE_NAME: str = os.environ.get("POSTGRES_DATABASE_NAME", "postgres")

    RECALLAI_WEBHOOK_TOKEN: str = os.environ.get("RECALLAI_WEBHOOK_TOKEN", FAKE_API_KEY)
    RECALLAI_API_KEY: str = os.environ.get("RECALLAI_API_KEY", FAKE_API_KEY)
    RECALLAI_TRANSCRIPTION_TOKEN: str = os.environ.get("RECALLAI_TRANSCRIPTION_TOKEN", FAKE_API_KEY)

    MAILGUN_API_KEY: str = os.environ.get("MAILGUN_API_KEY", FAKE_API_KEY)
    MAILGUN_DOMAIN: str = os.environ.get("MAILGUN_DOMAIN", None)

    ABLY_API_KEY: str = os.environ.get("ABLY_API_KEY", FAKE_API_KEY)


class ProjectPaths(BaseSettings):
    ROOT_PATH: Path = Path(__file__).parent.parent

    DATA_PATH: Path = ROOT_PATH / "data"
    PROJECT_PATH: Path = ROOT_PATH / "src"
    SPHINX_PATH: Path = ROOT_PATH / "docs"

    RAW_DATA: Path = DATA_PATH / "raw"
    PPTX_DATA: Path = DATA_PATH / "pptx"
    LOGS_DATA: Path = DATA_PATH / "logs"
    INTERIM_DATA: Path = DATA_PATH / "interim"
    EXTERNAL_DATA: Path = DATA_PATH / "external"
    PROCESSED_DATA: Path = DATA_PATH / "processed"


class ProjectEnvs(BaseSettings):
    DD_ENV: str = os.environ.get("DD_ENV", "dev")
    LOG_LVL: str = os.environ.get("LOG_LVL", "DEBUG")
    DEBUG: bool = os.environ.get("DEBUG", "False") == "True"
    ENV_STATE: str = os.environ.get("ENV_STATE", "LOCAL").upper()
    DD_AGENT_HOST: str = os.environ.get("DD_AGENT_HOST", "127.0.0.1")
    DD_TRACE_AGENT_PORT: int = os.environ.get("DD_TRACE_AGENT_PORT", 8126)
    GCP_SERVICE_ACCOUNT_JSON: str = os.environ.get("GCP_SERVICE_ACCOUNT_JSON", "")
    DD_LOGS_INJECTION: bool = os.environ.get("DD_LOGS_INJECTION", "False") == "True"


PROJECT_PATHS = ProjectPaths()
PROJECT_ENVS = ProjectEnvs()
API_KEYS = ApiKeys()
DATABASE_URI = f"postgresql://{API_KEYS.POSTGRES_DATABASE_USERNAME}:{API_KEYS.POSTGRES_DATABASE_PASSWORD}@{API_KEYS.POSTGRES_DATABASE_URL}/{API_KEYS.POSTGRES_DATABASE_NAME}{'?sslmode=require' if PROJECT_ENVS.ENV_STATE not in [Envs.LOCAL.value, Envs.DEV.value] else ''}"


def get_handler():
    return ["datadog"] if PROJECT_ENVS.ENV_STATE not in [Envs.LOCAL.value, Envs.DEV.value] else ["console"]


def get_level():
    return "INFO" if PROJECT_ENVS.ENV_STATE not in [Envs.LOCAL.value, Envs.DEV.value] else PROJECT_ENVS.LOG_LVL


local_env_loggers = {
    "sentence_transformers": {
        "handlers": get_handler(),
        "level": get_level(),
        "propagate": False,
    },
    "uvicorn": {
        "handlers": get_handler(),
        "level": get_level(),
        "propagate": False,
    },
    "openai": {
        "handlers": get_handler(),
        "level": get_level(),
        "propagate": False,
    },
    "git": {
        "handlers": get_handler(),
        "level": get_level(),
        "propagate": False,
    },
    "ably": {
        "handlers": get_handler(),
        "level": get_level(),
        "propagate": False,
    },
    "sqlalchemy.engine": {
        "handlers": get_handler(),
        "level": get_level(),
        "propagate": False,
    },
}


def get_local_env_logger():
    return {} if PROJECT_ENVS.ENV_STATE != Envs.LOCAL else local_env_loggers


class RichCustomFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rich_handler = RichHandler(rich_tracebacks=True, tracebacks_suppress=[], tracebacks_show_locals=True)

    def format(self, record):
        return super().format(record)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "console": {
            "()": RichCustomFormatter,
            "format": "%(message)s",
            "datefmt": "<%d %b %Y | %H:%M:%S>",
        },
        "json_datadog": {
            "()": JsonFormatter,
            "format": "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
            "[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s "
            "dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] - %(message)s",
            "datefmt": "<%d %b %Y | %H:%M:%S>",
        },
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "level": PROJECT_ENVS.LOG_LVL,
            "formatter": "console",
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
        },
        "datadog": {
            "class": "logging.StreamHandler",
            "formatter": "json_datadog",
        },
    },
    "loggers": {
        "": {
            "handlers": get_handler(),
            "level": PROJECT_ENVS.LOG_LVL,
            "propagate": True,
        }
        | get_local_env_logger(),
    },
}

logging.captureWarnings(True)
logging.config.dictConfig(LOGGING_CONFIG)
