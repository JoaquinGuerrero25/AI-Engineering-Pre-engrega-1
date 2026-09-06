from openai import (APIConnectionError, AsyncOpenAI, RateLimitError)
from collections.abc import AsyncIterator

from .base import BaseLLMClient
from .exceptions import LLMConnectionError, LLMRateLimitError
from .schemas import ChatMessage, ModelConfig, ModelResponse

class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def generate(self, messages: list[ChatMessage], config: ModelConfig) -> ModelResponse:
        try:
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

        except RateLimitError as error:
            raise LLMRateLimitError("OpenAI rate limit or quota exceeded.") from error
        
        except APIConnectionError as error:
            raise LLMConnectionError("Could not connect to OpenAI.") from error
    
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