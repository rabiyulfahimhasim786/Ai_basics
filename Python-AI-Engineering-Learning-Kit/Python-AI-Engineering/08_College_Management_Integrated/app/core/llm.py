from langchain_openai import ChatOpenAI
from app.core.config import settings


def build_chat_model(temperature: float = 0) -> ChatOpenAI:
    """Return a chat model for the provider selected by LLM_PROVIDER."""
    if settings.llm_provider == "openrouter":
        if not settings.openrouter_api_key:
            raise RuntimeError(
                "Set OPENROUTER_API_KEY in .env when LLM_PROVIDER=openrouter"
            )
        return ChatOpenAI(
            model=settings.openrouter_model,
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            temperature=temperature,
        )
    return ChatOpenAI(model=settings.openai_model, temperature=temperature)


def llm_is_configured() -> bool:
    if settings.llm_provider == "openrouter":
        return bool(settings.openrouter_api_key)
    return bool(settings.openai_api_key)
