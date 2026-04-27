from pydantic import BaseModel
from typing import List, Dict


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    messages: List[Dict[str, str]]
    escalated: bool


class HistoryResponse(BaseModel):
    conversation_id: str
    history: List[Dict[str, str]]
