class LLMClientError(Exception):
    """Base exception for LLM client errors."""

class LLMRateLimitError(LLMClientError):
    """Raised when the provider rate limit or quota is exceeded."""

class LLMConnectionError(LLMClientError):
    """Raised when there is a connection problem with the provider."""
    
class LLMAuthenticationError(LLMClientError):
    """Raised when the provider credentials are invalid."""