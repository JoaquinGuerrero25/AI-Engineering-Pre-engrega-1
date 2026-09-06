from collections.abc import AsyncIterator
from .anthropic_client import AnthropicClient
from .base import BaseLLMClient
from .openai_client import OpenAIClient
from .schemas import ChatMessage, ModelConfig, ModelResponse

class AsyncLLMManager:
    def __init__(self, openai_api_key: str, anthropic_api_key: str):
        self.clients: dict[str, BaseLLMClient] = {
            "openai": OpenAIClient(api_key=openai_api_key),
            "anthropic": AnthropicClient(api_key=anthropic_api_key)
        }
        
    def _get_client(self, provider: str) -> BaseLLMClient:
        client = self.clients.get(provider.lower())
        
        if client is None:
            raise ValueError(f"Unsupported provider: {provider}")
        
        return client
    
    async def generate(self, provider: str, messages: list[ChatMessage], config: ModelConfig) -> ModelResponse:
        client = self._get_client(provider.lower())

        return await client.generate(messages=messages, config=config)
    
    async def stream(self, provider: str, messages: list[ChatMessage], config: ModelConfig) -> AsyncIterator[str]:
        client = self._get_client(provider.lower())

        async for chunk in client.stream(messages=messages, config=config):
            yield chunk