from enum import Enum
from typing import Union, Type, Dict, Callable
from functools import wraps
from abc import ABC
import logging

from src.schema import ChatModel, EmbeddingModel

logger = logging.getLogger(__name__)

class Factories(Enum):
    TEMPLATE = "template"
    EMBEDDING = "embedding"
    CHAT = "chat"


class FactoryError(Exception):
    """Custom exception for factory errors."""


class BaseFactory(ABC):
    """Base class for all factories"""
    def __init__(self, model, sync: bool = False, to_db: bool = False):
        self.model = model
        self.sync = sync
        self.to_db = to_db


class FactoryRegistry:
    """Registry to maintain factory mappings."""
    _factories: Dict[str, Dict[Type, Type]] = {}

    @classmethod
    def register(cls, category: str, model_type: Type, factory_cls: Type) -> None:
        """Register an extractor class for a specific model type and category."""
        if not issubclass(factory_cls, BaseFactory):
            raise FactoryError(f"Factory class must inherit from BaseFactories")
        if category not in cls._factories:
            cls._factories[category] = {}
        cls._factories[category][model_type] = factory_cls

    @classmethod
    def get(cls, category: str, model_type: Type) -> Type:
        """Get the registered extractor class."""
        try:
            return cls._factories[category][model_type]
        except KeyError:
            raise FactoryError(f"No extractor registered for category '{category}' and model type '{model_type.__name__}'")


def validate_model(func: Callable) -> Callable:
    """Decorator to validate model type."""
    @wraps(func)
    def wrapper(cls, model: Union[ChatModel, EmbeddingModel], *args, **kwargs):
        if not isinstance(model, (ChatModel, EmbeddingModel)):
            raise FactoryError(f"Expected ChatModel or EmbeddingModel instance, got {type(model).__name__}")
        return func(cls, model, *args, **kwargs)
    return wrapper  # noqa: RET504


class AbstractFactory:
    """Abstract factory base class with registry support."""
    
    @classmethod
    @validate_model
    def build(cls, model: Union[ChatModel, EmbeddingModel], category: str, sync: bool = False, to_db: bool = False) -> BaseFactory:
        """Create a factory instance based on the model type and category."""
        factory_cls = FactoryRegistry.get(category, type(model))
        return factory_cls(model=model, sync=sync, to_db=to_db)
