from src.infrastructure.factory import Factories, FactoryRegistry, AbstractFactory, BaseFactory
from src.schema import ChatModel, EmbeddingModel


class TemplateFactory(BaseFactory):
    pass


# Register factories
FactoryRegistry.register(Factories.TEMPLATE.value, ChatModel, TemplateFactory)

# Usage
extractor = AbstractFactory.build(
    model=ChatModel(), 
    category=Factories.TEMPLATE.value,
    sync=True, 
    to_db=False
)
