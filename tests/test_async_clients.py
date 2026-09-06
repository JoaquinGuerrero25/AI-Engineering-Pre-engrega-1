import pytest

from openai import APIConnectionError, RateLimitError
from anthropic import RateLimitError as AnthropicRateLimitError
from anthropic import APIConnectionError as AnthropicAPIConnectionError

from app.openai_client import OpenAIClient
from app.schemas import ChatMessage, ModelConfig
from app.anthropic_client import AnthropicClient
from app.exceptions import LLMConnectionError, LLMRateLimitError

class FakeOpenAIResponse:

    class Choice:
        class Message:
            content = "Respuesta de prueba"

        message = Message()

    choices = [Choice()]
    model = "fake-model"

class FakeOpenAICompletions:

    async def create(self, **kwargs):
        return FakeOpenAIResponse()


class FakeOpenAIClient:

    class Chat:
        completions = FakeOpenAICompletions()

    chat = Chat()


@pytest.mark.asyncio
async def test_openai_generate():
    client = OpenAIClient(api_key="test-key")

    client.client = FakeOpenAIClient()

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

    response = await client.generate(
        messages=messages,
        config=config,
    )

    assert response.content == "Respuesta de prueba"
    assert response.model == "fake-model"
    assert response.provider.lower() == "openai"
    
class FakeAnthropicResponse:

    class TextBlock:
        type = "text"
        text = "Respuesta de prueba"

    content = [TextBlock()]
    model = "fake-claude-model"


class FakeAnthropicMessages:

    async def create(self, **kwargs):
        return FakeAnthropicResponse()


class FakeAnthropicClient:

    messages = FakeAnthropicMessages()


@pytest.mark.asyncio
async def test_anthropic_generate():
    client = AnthropicClient(api_key="test-key")

    client.client = FakeAnthropicClient()

    messages = [
        ChatMessage(
            role="user",
            content="¿Qué es la entropía?",
        )
    ]

    config = ModelConfig(
        model="fake-claude-model",
        temperature=0.7,
        max_tokens=500,
    )

    response = await client.generate(
        messages=messages,
        config=config,
    )

    assert response.content == "Respuesta de prueba"
    assert response.model == "fake-claude-model"
    assert response.provider.lower() == "anthropic"
    
class FakeAnthropicStream:

    def __init__(self):
        self.text_stream = self._generate_chunks()

    async def _generate_chunks(self):
        for chunk in ["Hola ", "mundo", "!"]:
            yield chunk


class FakeAnthropicMessagesStreaming:

    def stream(self, **kwargs):
        return FakeAnthropicStreamContext()


class FakeAnthropicStreamContext:

    async def __aenter__(self):
        return FakeAnthropicStream()

    async def __aexit__(self, exc_type, exc, tb):
        pass


class FakeAnthropicStreamingClient:

    messages = FakeAnthropicMessagesStreaming()


@pytest.mark.asyncio
async def test_anthropic_stream():
    client = AnthropicClient(api_key="test-key")

    client.client = FakeAnthropicStreamingClient()

    messages = [
        ChatMessage(
            role="user",
            content="Hola",
        )
    ]

    config = ModelConfig(
        model="fake-claude-model",
        temperature=0.7,
        max_tokens=100,
    )

    chunks = []

    async for chunk in client.stream(
        messages=messages,
        config=config,
    ):
        chunks.append(chunk)

    assert chunks == [
        "Hola ",
        "mundo",
        "!",
    ]
    
class FakeRateLimitError(RateLimitError):
    def __init__(self):
        pass  
    
@pytest.mark.asyncio
async def test_openai_generate_handles_rate_limit_error():
    client = OpenAIClient(api_key="test-key")

    class FakeCompletions:
        async def create(self, **kwargs):
            raise FakeRateLimitError()
        
    class FakeChat:
        completions = FakeCompletions()

    class FakeClient:
        chat = FakeChat()

    client.client = FakeClient()

    messages = [
        ChatMessage(
            role="user",
            content="Hola",
        )
    ]

    config = ModelConfig(
        model="fake-model",
        temperature=0.7,
        max_tokens=100,
    )

    with pytest.raises(LLMRateLimitError):
        await client.generate(
            messages=messages,
            config=config,
        )
        
@pytest.mark.asyncio
async def test_openai_generate_handles_connection_error():
    client = OpenAIClient(api_key="test-key")

    class FakeAPIConnectionError(APIConnectionError):
        def __init__(self):
            pass

    class FakeCompletions:

        async def create(self, **kwargs):
            raise FakeAPIConnectionError()

    class FakeChat:
        completions = FakeCompletions()

    class FakeClient:
        chat = FakeChat()

    client.client = FakeClient()

    messages = [
        ChatMessage(
            role="user",
            content="Hola",
        )
    ]

    config = ModelConfig(
        model="fake-model",
        temperature=0.7,
        max_tokens=100,
    )

    with pytest.raises(LLMConnectionError):
        await client.generate(
            messages=messages,
            config=config,
        )

@pytest.mark.asyncio
async def test_anthropic_generate_handles_rate_limit_error():
    client = AnthropicClient(api_key="test-key")

    class FakeRateLimitError(AnthropicRateLimitError):
        def __init__(self):
            pass

    class FakeMessages:

        async def create(self, **kwargs):
            raise FakeRateLimitError()

    class FakeClient:
        messages = FakeMessages()

    client.client = FakeClient()

    messages = [
        ChatMessage(
            role="user",
            content="Hola",
        )
    ]

    config = ModelConfig(
        model="fake-model",
        temperature=0.7,
        max_tokens=100,
    )

    with pytest.raises(LLMRateLimitError):
        await client.generate(
            messages=messages,
            config=config,
        )
        
@pytest.mark.asyncio
async def test_anthropic_generate_handles_connection_error():
    client = AnthropicClient(api_key="test-key")

    class FakeAPIConnectionError(AnthropicAPIConnectionError):
        def __init__(self):
            pass

    class FakeMessages:

        async def create(self, **kwargs):
            raise FakeAPIConnectionError()

    class FakeClient:
        messages = FakeMessages()

    client.client = FakeClient()

    messages = [
        ChatMessage(
            role="user",
            content="Hola",
        )
    ]

    config = ModelConfig(
        model="fake-model",
        temperature=0.7,
        max_tokens=100,
    )

    with pytest.raises(LLMConnectionError):
        await client.generate(
            messages=messages,
            config=config,
        )