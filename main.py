import asyncio
import os

from dotenv import load_dotenv
from app.manager import AsyncLLMManager
from app.schemas import ChatMessage, ModelConfig
from app.exceptions import LLMRateLimitError, LLMConnectionError

load_dotenv()

async def main():
    provider = os.getenv("LLM_PROVIDER")
    if not provider:
        raise ValueError("LLM_PROVIDER is not configured")
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set in the environment variables.")
    
    openai_model = os.getenv("OPENAI_MODEL")
    anthropic_model = os.getenv("ANTHROPIC_MODEL")
    
    if not openai_model:
        raise ValueError("OPENAI_MODEL is not set in the environment variables.")
    
    if not anthropic_model:
        raise ValueError("ANTHROPIC_MODEL is not set in the environment variables.")
    
    manager = AsyncLLMManager(openai_api_key=openai_api_key, anthropic_api_key=anthropic_api_key)
    
    messages = [ChatMessage(role="user", content="¿Qué es la entropía? Explícalo de forma sencilla.")]
    
    openai_config = ModelConfig(model=openai_model, max_tokens=100, temperature=0.7)
    anthropic_config = ModelConfig(model=anthropic_model, max_tokens=100, temperature=0.7)
    
    print("\n--- RESPUESTA OPENAI ---")
    try:
        response = await manager.generate(provider=provider, messages=messages, config=openai_config)
        print(response.content)
    
    except LLMRateLimitError as error:
        print(f"\nRate limit / quota error: {error}")

    except LLMConnectionError as error:
        print(f"\nConnection error: {error}")
        
    print("\n--- STREAMING OPENAI ---")

    try:
        async for chunk in manager.stream(provider="openai", messages=messages, config=openai_config):
            print(chunk, end="", flush=True)

        print()

    except LLMRateLimitError as error:
        print(f"\nRate limit / quota error: {error}")

    except LLMConnectionError as error:
        print(f"\nConnection error: {error}")
        
if __name__ == "__main__":
    asyncio.run(main())