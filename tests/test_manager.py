import pytest

from app.manager import AsyncLLMManager
from app.schemas import ChatMessage, ModelConfig, ModelResponse

def test_manager_selects_openai_client():
    manager = AsyncLLMManager(
        openai_api_key="test-openai-key",
        anthropic_api_key="test-anthropic-key",
    )

    client = manager._get_client("openai")

    assert client.__class__.__name__ == "OpenAIClient"

def test_manager_selects_anthropic_client():
    manager = AsyncLLMManager(
        openai_api_key="test-openai-key",
        anthropic_api_key="test-anthropic-key",
    )

    client = manager._get_client("anthropic")

    assert client.__class__.__name__ == "AnthropicClient"

def test_manager_provider_is_case_insensitive():
    manager = AsyncLLMManager(
        openai_api_key="test-openai-key",
        anthropic_api_key="test-anthropic-key",
    )

    client = manager._get_client("OPENAI")

    assert client.__class__.__name__ == "OpenAIClient"

def test_manager_rejects_unsupported_provider():
    manager = AsyncLLMManager(
        openai_api_key="test-openai-key",
        anthropic_api_key="test-anthropic-key",
    )

    with pytest.raises(ValueError, match="Unsupported provider"):
        manager._get_client("google")