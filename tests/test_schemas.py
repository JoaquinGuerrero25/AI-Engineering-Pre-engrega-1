import pytest

from pydantic import ValidationError

from app.schemas import ChatMessage, ModelConfig

def test_chat_message_valid():
    message = ChatMessage(role="user", content="Hola!")
    
    assert message.role == "user"
    assert message.content == "Hola!"
    
def test_chat_message_invalid_role():
    with pytest.raises(ValidationError):
        ChatMessage(role="Invalid", content="Hola!")
        
def test_model_config_valid():
    config = ModelConfig(model="gpt-4o-mini", temperature=0.7, max_tokens=500)
    
    assert config.model == "gpt-4o-mini"
    assert config.temperature == 0.7
    assert config.max_tokens == 500
    
def test_model_config_invalid_temperature():
    with pytest.raises(ValidationError):
        ModelConfig(model="gpt-4o-mini", temperature=3.0, max_tokens=500)