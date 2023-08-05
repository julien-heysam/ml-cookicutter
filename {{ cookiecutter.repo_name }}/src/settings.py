import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings
from rich.logging import RichHandler

load_dotenv(override=True)

logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True, tracebacks_suppress=[])],
)
logger = logging.getLogger("gorgas-ai")


class ModelVar(BaseSettings):
    TEMPERATURE: float = 0.2
    PRICE_PER_TOKENS_INPUT: float = 0.0015 / 1000
    PRICE_PER_TOKENS_OUTPUT: float = 0.002 / 1000
    LLM_MODEl: str = "gpt-4"  # "gpt-3.5-turbo-16k-0613"
    USE_EVALUATION_LAYER: bool = True


class ApiKeys(BaseSettings):
    API_KEY: str = os.environ.get("API_KEY", "")
    PINECONE_ENV: str = os.environ.get("PINECONE_ENV", "")
    COMET_API_KEY: str = os.environ.get("COMET_API_KEY", "")
    NOTION_API_KEY: str = os.environ.get("NOTION_API_KEY", "")
    PINECONE_INDEX: str = os.environ.get("PINECONE_INDEX", "")
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
    APIFY_API_TOKEN: str = os.environ.get("APIFY_API_TOKEN", "")
    PINECONE_API_KEY: str = os.environ.get("PINECONE_API_KEY", "")
    PROMPTLAYER_API_KEY: str = os.environ.get("PROMPTLAYER_API_KEY", "")
    OPENAI_ORGANIZATION: str = os.environ.get("OPENAI_ORGANIZATION", "Gorgias - Sandbox")


class ProjectPaths(BaseSettings):
    ROOT_PATH: Path = Path(__file__).parent.parent

    PROJECT_PATH: Path = ROOT_PATH / "src"
    QUERIES_PATH: Path = PROJECT_PATH / "queries"

    DATA_PATH: Path = ROOT_PATH / "data"
    LOGS_DATA: Path = DATA_PATH / "logs"
    RAW_DATA: Path = DATA_PATH / "raw"
    INTERIM_DATA: Path = DATA_PATH / "interim"
    EXTERNAL_DATA: Path = DATA_PATH / "external"
    PROCESSED_DATA: Path = DATA_PATH / "processed"
    EVALUATION_DATA: Path = DATA_PATH / "evaluation"

    MODEL_DATA: Path = ROOT_PATH / "models"


class ProjectEnvs(BaseSettings):
    PROJECT_BUCKET: str = os.environ.get("PROJECT_BUCKET", "gs://gorgias-ml-production-{{ cookiecutter.project_name }}")
    PROJECT_ID: str = os.environ.get("GCP_PROJECT_ID", "gorgias-ml-production")
    ENV_STATE: str = os.environ.get("ENV_STATE", "production")


class ProcessingVar(BaseSettings):
    MIN_NUMBER_WORDS: int = 4
    MAX_NUMBER_WORDS: int = 512


class GorgiasMLApi(BaseSettings):
    ENV_STATE: str = os.environ.get("ENV_STATE", "production")
    ROOT_URL: str = (
        f"https://intent.production.gorgias.ai/"
        if ENV_STATE == "production"
        else f"https://us-central1.incoming.staging.gorgias.ai/"
    )
    HELP_CENTER_SEARCH_ENDPOINT: str = "article-recommendation/search"
    QUESTION_EXTRACTION_ENDPOINT: str = "faq-questions/prediction"
    PRODUCTS_SEARCH_ENDPOINT: str = "products/search"
    WEB_DATA_SEARCH_ENDPOINT: str = "web-data/search"
    MACRO_SEARCH_ENDPOINT: str = "macro/search"
    USE_WEB_DATA: bool = False
    USE_MACRO_DATA: bool = True
    USE_PRODUCTS_DATA: bool = False
    USE_HELP_CENTER_DATA: bool = True


MODEL_VAR = ModelVar()
GORGIAS_ML_API = GorgiasMLApi()
PROCESSING_VAR = ProcessingVar()
PROJECT_ENV = ProjectEnvs()
PROJECT_PATHS = ProjectPaths()
API_KEYS = ApiKeys()
