import pytest

from app.anthropic_client import AnthropicClient
from app.manager import AsyncLLMManager
from app.openai_client import OpenAIClient


def test_manager_selects_openai_client():
    manager = AsyncLLMManager(
        provider="openai",
        api_key="test-openai-key",
    )

    assert isinstance(manager.client, OpenAIClient)


def test_manager_selects_anthropic_client():
    manager = AsyncLLMManager(
        provider="anthropic",
        api_key="test-anthropic-key",
    )

    assert isinstance(manager.client, AnthropicClient)


def test_manager_provider_is_case_insensitive():
    manager = AsyncLLMManager(
        provider="OpenAI",
        api_key="test-openai-key",
    )

    assert manager.provider == "openai"
    assert isinstance(manager.client, OpenAIClient)


def test_manager_rejects_unsupported_provider():
    with pytest.raises(ValueError, match="Unsupported provider"):
        AsyncLLMManager(
            provider="unsupported",
            api_key="test-key",
        )