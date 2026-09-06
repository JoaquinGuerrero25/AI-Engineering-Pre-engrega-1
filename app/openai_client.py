from openai import AsyncOpenAI
from collections.abc import AsyncIterator
from .base import BaseLLMClient
from .schemas import ChatMessage, ModelConfig, ModelResponse

class OpenAIClient(BaseLLMClient):

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def generate(self, messages: list[ChatMessage], config: ModelConfig) -> ModelResponse:
        response = await self.client.chat.completions.create(
            model = config.model,
            messages = [{"role": message.role, "content": message.content} for message in messages],
            temperature = config.temperature,
            max_tokens = config.max_tokens
        )
        
        return ModelResponse(
            content = response.choices[0].message.content or "",
            model = response.model,
            provider = "OpenAI"
        )
    
    async def stream(self, messages: list[ChatMessage], config: ModelConfig) -> AsyncIterator[str]:
        response = await self.client.chat.completions.create(
            model = config.model,
            messages = [{"role": message.role, "content": message.content} for message in messages],
            temperature = config.temperature,
            max_tokens = config.max_tokens,
            stream = True
        )
        
        async for chunk in response:
            content = chunk.choices[0].delta.get
            
            if content:
                yield content