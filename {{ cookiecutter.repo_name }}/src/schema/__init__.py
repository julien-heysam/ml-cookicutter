from typing import Literal, Optional

from pydantic import BaseModel


class ChatModel(BaseModel):
    name: str
    max_output: int
    context_size: int
    cost_prompt_token: float
    provider: str
    stop: Optional[str] = None
    cost_completion_token: float
    temperature: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0


class EmbeddingModel(BaseModel):
    context_size: int
    cost_token: float
    dimension: int
    metric: str
    name: str
    provider: str


class TTSModel(BaseModel):
    cost_char: float
    name: str
    provider: str
    voice: str = Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


class RerankModel(BaseModel):
    name: str
    provider: str
    cost_search: Optional[float] = 0.0
    cost_token: Optional[float] = 0.0


class STTModel(BaseModel):
    cost_char: float
    provider: str
    name: str


__ALL__ = []
