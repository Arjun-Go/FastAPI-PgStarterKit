from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SessionCreate(BaseModel):
    session_user: str = Field(..., min_length=1)

class Session(BaseModel):
    session_id: int
    session_user: str
    created_at: datetime

class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1)

class MessageResponse(BaseModel):
    role: str
    content: str
