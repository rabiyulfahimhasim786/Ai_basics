from typing import Literal
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()  # Make .env values available to OpenAI/LangChain SDK clients too.


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-5.5"
    llm_provider: Literal["openai", "openrouter"] = "openai"
    openrouter_api_key: str | None = None
    openrouter_model: str = "nvidia/nemotron-3-ultra-550b-a55b:free"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    embedding_model: str = "text-embedding-3-small"
    database_url: str = "sqlite:///./college.db"
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection: str = "college_management_policies"
    mcp_server_url: str = "http://127.0.0.1:8001/mcp"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
