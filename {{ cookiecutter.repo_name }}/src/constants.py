from enum import Enum

class RagFusionAlgos(Enum):
    RECIPROCAL = "reciprocal"


class SlackApps(Enum):
    WEB = "web"


class Conversations(Enum):
    WEB = "web"


class OriginRequests(Enum):
    WEB = "web"
    MACHINE = "machine"


class Envs(Enum):
    DEV = "DEV"
    PROD = "PROD"
    LOCAL = "LOCAL"
    STAGING = "STAGING"


class TextReductions(Enum):
    ABSTRACTIVE_SUMMARIZATION = "abstractive_summarization"
    EXTRACTIVE_SUMMARIZATION = "extractive_summarization"


class TasksComplexity(Enum):
    LVL1 = 1
    LVL2 = 2
    LVL3 = 3
    LVL4 = 4
    LVL5 = 5
    LVL6 = 6


class QueryTypes(Enum):
    EXPAND = "expand"
    REFINE = "refine"
    DECOMPOSE = "decompose"


class Providers(Enum):
    ABLY = "ably"
    PRINT = "print"
    NOMIC = "nomic"
    LOGGER = "logger"
    RECALL = "recall"
    COHERE = "cohere"
    GOOGLE = "google"
    OPENAI = "openai"
    OPENCV = "opencv"
    PYGAME = "pygame"
    ALGOLIA = "algolia"
    SKLEARN = "sklearn"
    MOVIEPY = "moviepy"
    PINECONE = "pinecone"
    ANTHROPIC = "anthropic"
    MIXEDNREAD = "mixedbread"
    TRANSFORMERS = "transformers"
    HTTP_PINECONE = "http_pinecone"


class Clusterings(Enum):
    BIRCH = "birch"
    HIERARCHICAL = "hierarchical"


class ClusterTitles(Enum):
    CENTROID = "centroid"
    LLM = "llm"


class Instances(Enum):
    JSON = "json"
    LIST = "list"
    STRING = "string"


class Schedulers(Enum):
    MP = "mp"
    ASYNC = "async"
    THREAD = "thread"
    APSCHEDULER = "apscheduler"


class Splitters(Enum):
    NLTK = "nltk"
    REGEX = "regex"


class Roles(Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class Creators(Enum):
    USER = "user"


class Statues(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Contents(Enum):
    TEXT = "text"
    IMAGE = "image"
