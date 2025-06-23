from pydantic import BaseModel
from typing import List, Optional

class GoogleSearchRequest(BaseModel):
    query: str

class GoogleSearchResultItem(BaseModel):
    title: str
    link: str
    snippet: Optional[str] = None

class GoogleSearchResponse(BaseModel):
    results: List[GoogleSearchResultItem]

# New model for chat messages
class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class OpenAIRequest(BaseModel):
    messages: List[ChatMessage]

class OpenAIResponse(BaseModel):
    response: str
