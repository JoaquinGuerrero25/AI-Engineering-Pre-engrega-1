import asyncio
import os

from dotenv import load_dotenv
from app.manager import AsyncLLMManager
from app.schemas import ChatMessage, ModelConfig

load_dotenv()

async def main():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    openai_model = os.getenv("OPENAI_MODEL")
    anthropic_model = os.getenv("ANTHROPIC_MODEL")

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set in the environment variables.")
    
    if not openai_model:
        raise ValueError("OPENAI_MODEL is not set in the environment variables.")
    
    if not anthropic_model:
        raise ValueError("ANTHROPIC_MODEL is not set in the environment variables.")
    
    manager = AsyncLLMManager(openai_api_key=openai_api_key, anthropic_api_key=anthropic_api_key)
    
    messages = [ChatMessage(role="user", content="¿Qué es la entropía? Explícalo de forma sencilla.")]
    
    openai_config = ModelConfig(model=openai_model, max_tokens=100, temperature=0.7)
    anthropic_config = ModelConfig(model=anthropic_model, max_tokens=100, temperature=0.7)
    
    response = await manager.generate(provider="openai", messages=messages, config=openai_config)
    
    print("\n--- RESPUESTA OPENAI ---")
    print(response.content)

if __name__ == "__main__":
    asyncio.run(main())