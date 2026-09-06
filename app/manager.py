from collections.abc import AsyncIterator
from .anthropic_client import AnthropicClient
from .base import BaseLLMClient
from .openai_client import OpenAIClient
from .schemas import ChatMessage, ModelConfig, ModelResponse

class AsyncLLMManager:
    def __init__(self, provider: str, api_key:str):
        self.provider = provider.lower()

        if self.provider == "openai":
            self.client: BaseLLMClient = OpenAIClient(api_key)

        elif self.provider == "anthropic":
            self.client = AnthropicClient(api_key)
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
    def _get_client(self, provider: str) -> BaseLLMClient:
        client = self.clients.get(provider.lower())
        
        if client is None:
            raise ValueError(f"Unsupported provider: {provider}")
        
        return client
    
    async def generate(self, messages: list[ChatMessage], config: ModelConfig) -> ModelResponse:
        return await self.client.generate(messages=messages, config=config)
    
    async def stream(self, messages: list[ChatMessage], config: ModelConfig) -> AsyncIterator[str]:
        async for chunk in self.client.stream(messages=messages, config=config):
            yield chunk