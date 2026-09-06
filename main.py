import asyncio
import os

from dotenv import load_dotenv
from app.manager import AsyncLLMManager
from app.schemas import ChatMessage, ModelConfig
from app.exceptions import LLMRateLimitError, LLMConnectionError

load_dotenv()

def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(
            f"{name} is not configured in the environment variables."
        )

    return value

def get_float_env(name: str, default: float) -> float:
    value = os.getenv(name, str(default))

    try:
        return float(value)
    except ValueError as error:
        raise ValueError(
            f"{name} must be a valid number."
        ) from error

def get_int_env(name: str, default: int) -> int:
    value = os.getenv(name, str(default))

    try:
        return int(value)
    except ValueError as error:
        raise ValueError(
            f"{name} must be a valid integer."
        ) from error

async def main():
    provider = get_required_env("LLM_PROVIDER").lower()

    if provider == "openai":
        api_key = get_required_env("OPENAI_API_KEY")
        model = get_required_env("OPENAI_MODEL")

    elif provider == "anthropic":
        api_key = get_required_env("ANTHROPIC_API_KEY")
        model = get_required_env("ANTHROPIC_MODEL")

    else:
        raise ValueError(f"Unsupported provider: {provider}")

    temperature = get_float_env("LLM_TEMPERATURE", 0.7)
    max_tokens = get_int_env("LLM_MAX_TOKENS", 100)
    
    manager = AsyncLLMManager(provider=provider, api_key=api_key)
    
    messages = [ChatMessage(role="user", content="¿Qué es la entropía? Explícalo de forma sencilla.")]
    
    config = ModelConfig(model=model, temperature=temperature, max_tokens=max_tokens)
    
    print(f"\n--- RESPUESTA {provider.upper()} ---")
    
    try:
        response = await manager.generate(messages=messages, config=config)
        print(response.content)
    
    except LLMRateLimitError as error:
        print(f"\nRate limit / quota error: {error}")
    
    except LLMAuthenticationError as error:
        print(f"\nAuthentication error: {error}")

    except LLMConnectionError as error:
        print(f"\nConnection error: {error}")
        
    print(f"\n--- STREAMING {provider.upper()} ---")

    try:
        async for chunk in manager.stream(messages=messages, config=config):
            print(chunk, end="", flush=True)

        print()

    except LLMRateLimitError as error:
        print(f"\nRate limit / quota error: {error}")

    except LLMConnectionError as error:
        print(f"\nConnection error: {error}")
        
    except LLMAuthenticationError as error:
        print(f"\nAuthentication error: {error}")
        
if __name__ == "__main__":
    asyncio.run(main())