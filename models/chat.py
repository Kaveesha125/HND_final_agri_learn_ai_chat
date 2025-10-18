from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    role: str
    conversation_id: str | None = None
