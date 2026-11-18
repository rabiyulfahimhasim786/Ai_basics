import logging
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Request
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/v1", tags=["AI Assistant"])


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, request: Request) -> ChatResponse:
    assistant = request.app.state.assistant
    try:
        answer = await assistant.ask(payload.question)
        return ChatResponse(answer=answer, request_id=str(uuid4()))
    except Exception as exc:
        # Log the full exception server-side; do not expose secrets/internal details to clients.
        logging.getLogger(__name__).exception("AI chat request failed")
        raise HTTPException(status_code=502, detail="The AI assistant could not complete the request") from exc
