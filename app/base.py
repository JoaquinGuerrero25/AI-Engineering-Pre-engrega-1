from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from .schemas import ChatMessage, ModelConfig, ModelResponse

class BaseLLMClient(ABC):
    
    @abstractmethod
    async def generate(self, messages: list[ChatMessage], config: ModelConfig) -> ModelResponse:
        """Generate a complete response from the LLM."""
        raise NotImplementedError
    
    @abstractmethod
    async def stream(self, messages: list[ChatMessage], config: ModelConfig) -> AsyncIterator[str]:
        """Stream the response fragments from the LLM."""
        raise NotImplementedError