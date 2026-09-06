from collections.abc import AsyncIterator
from anthropic import AsyncAnthropic, APIConnectionError, RateLimitError

from .exceptions import LLMConnectionError, LLMRateLimitError
from .base import BaseLLMClient
from .schemas import ChatMessage, ModelConfig, ModelResponse

class AnthropicClient(BaseLLMClient):

    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
    
    async def generate(self, messages: list[ChatMessage], config: ModelConfig) -> ModelResponse:
        system_message = [
            message.content for message in messages if message.role == "system"
        ]
        
        conversation_messages = [
            {"role": message.role, "content": message.content}
            for message in messages if message.role != "system"
        ]
        
        try: 
            response = await self.client.chat.completions.create(
                model = config.model,
                max_tokens = config.max_tokens,
                temperature = config.temperature,
                system="\n".join(system_message) if system_message else None,
                messages = conversation_messages
            )
            
            content = "".join(block.text for block in response.completion if block.type == "text")
            
            return ModelResponse(content = content, model = response.model, provider = "Anthropic")
        
        except RateLimitError as error:
            raise LLMRateLimitError("Anthropic rate limit or quota exceeded.") from error
        
        except APIConnectionError as error:
            raise LLMConnectionError("Could not connect to Anthropic.") from error
    
    async def stream(self, messages: list[ChatMessage], config: ModelConfig) -> AsyncIterator[str]:
        system_message = [message.content for message in messages if message.role == "system"]
        
        conversation_messages = [
            {"role": message.role, "content": message.content}
            for message in messages if message.role != "system"
        ]
        
        async with self.client.messages.stream(
            model = config.model,
            max_tokens = config.max_tokens,
            temperature = config.temperature,
            system="\n".join(system_message) if system_message else None,
            messages = conversation_messages
        ) as stream:
            async for text in stream.text_stream:
                yield text
        
        
        