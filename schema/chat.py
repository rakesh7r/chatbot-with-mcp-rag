from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# ----------------------------
# Types
# ----------------------------
class HistoryItem(BaseModel):
    role: str
    parts: List[Dict[str, str]]

class ChatType(BaseModel):
    prompt: str
    response: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    prompt: str
    history: List[ChatType] = []

class ResponseSchema(BaseModel):
    status: str
    prompt: str
    message: str
    data: Dict[str, Any]

