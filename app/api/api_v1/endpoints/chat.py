from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.schemas.chat import SessionCreate, Session, Message, MessageResponse

router = APIRouter()

# In-memory storage
session_store: List[dict] = []
chat_store: dict = {}

@router.post("/sessions", response_model=Session)
async def create_session(session: SessionCreate):
    normalized_user = session.session_user.strip().lower()
    if not normalized_user:
        raise HTTPException(status_code=400, detail="Username cannot be empty")
    
    # Create new session
    session_id = len(session_store) + 1
    new_session = {
        "session_id": session_id,
        "session_user": normalized_user,
        "created_at": datetime.utcnow()
    }
    
    # Store session
    session_store.append(new_session)
    chat_store[session_id] = []
    
    return new_session

@router.post("/sessions/{session_id}/messages", response_model=Message)
async def add_message(session_id: int, message: Message):
    if session_id not in chat_store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if message.role not in ["user", "assistant"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    chat_store[session_id].append(message.dict())
    return message

@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    session_id: int,
    role: Optional[str] = Query(None, pattern="^(user|assistant)$")
):
    if session_id not in chat_store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = chat_store[session_id]
    if role:
        messages = [msg for msg in messages if msg["role"] == role]
    
    return messages
