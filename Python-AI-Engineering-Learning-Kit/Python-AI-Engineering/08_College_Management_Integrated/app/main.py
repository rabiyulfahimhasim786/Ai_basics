from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes.chat import router as chat_router
from app.core.config import settings  # validates required environment configuration
from app.core.llm import llm_is_configured
from app.db.database import Base, engine
from app.models import Student, Attendance, Fee  # register ORM metadata
from app.services.agent_service import CollegeAssistant


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    assistant = CollegeAssistant()
    await assistant.initialize()
    app.state.assistant = assistant
    yield


app = FastAPI(
    title="College Management AI Assistant",
    version="1.0.0",
    description="Learning project: LLM + Agent + MCP + LangChain + RAG + Qdrant",
    lifespan=lifespan,
)
app.include_router(chat_router)


@app.get("/health", tags=["Health"])
async def health() -> dict:
    return {
        "status": "ok",
        "llm_provider": settings.llm_provider,
        "model_configured": llm_is_configured(),
    }
