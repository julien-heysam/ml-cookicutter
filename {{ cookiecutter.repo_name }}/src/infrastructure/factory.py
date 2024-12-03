from typing import Type, Dict
import logging

logger = logging.getLogger(__name__)


class FactoryError(Exception):
    """Custom exception for factory errors."""


class FactoryRegistry:
    """Registry to maintain factory mappings."""
    _factories: Dict[str, Dict[Type, Type]] = {}

    @classmethod
    def register(cls, category: str, model_type: Type, factory_cls: Type) -> None:
        """Register an extractor class for a specific model type and category."""
        if category not in cls._factories:
            cls._factories[category] = {}
        cls._factories[category][model_type] = factory_cls

    @classmethod
    def get(cls, category: str, model_type: Type) -> Type:
        """Get the registered extractor class."""
        try:
            return cls._factories[category][model_type]
        except KeyError:
            raise FactoryError(f"No factory registered for category '{category}' and model type '{model_type.__name__}'")


factories = FactoryRegistry()
