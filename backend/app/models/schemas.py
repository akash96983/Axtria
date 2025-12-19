from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    text: str
    session_id: str = "default_session"

class ChatResponse(BaseModel):
    text: str
    source: str | None
    count: int
    status: str = "success"
