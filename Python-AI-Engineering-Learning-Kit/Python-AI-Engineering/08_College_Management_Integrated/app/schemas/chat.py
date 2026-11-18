from pydantic import BaseModel, Field, ConfigDict


class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    question: str = Field(min_length=3, max_length=2000, description="Question for the college assistant")


class ChatResponse(BaseModel):
    answer: str
    request_id: str
