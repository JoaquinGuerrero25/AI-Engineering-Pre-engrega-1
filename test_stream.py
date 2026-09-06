import asyncio

from app.schemas import ChatMessage, ModelConfig


class FakeLLMClient:

    async def stream(self, messages, config):
        chunks = [
            "La ",
            "entropía ",
            "es una medida ",
            "del desorden ",
            "o incertidumbre.",
        ]

        for chunk in chunks:
            await asyncio.sleep(0.2)
            yield chunk


async def main():
    client = FakeLLMClient()

    messages = [
        ChatMessage(
            role="user",
            content="¿Qué es la entropía?",
        )
    ]

    config = ModelConfig(
        model="fake-model",
        temperature=0.7,
        max_tokens=500,
    )

    print("--- STREAMING LOCAL ---")

    async for chunk in client.stream(
        messages=messages,
        config=config,
    ):
        print(chunk, end="", flush=True)

    print("\n")
    print("Streaming finalizado correctamente.")


if __name__ == "__main__":
    asyncio.run(main())