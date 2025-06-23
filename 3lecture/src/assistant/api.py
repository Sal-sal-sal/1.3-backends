from fastapi import APIRouter, Body, HTTPException
from .google_agent import GoogleSearchAgent
from .openai_agent import run_agent_with_search
from .models import GoogleSearchRequest, GoogleSearchResponse, GoogleSearchResultItem, OpenAIRequest, OpenAIResponse
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CX_ID = "00d92e72f2da44f8b"

router = APIRouter()

@router.post("/google_search", response_model=GoogleSearchResponse)
def google_search(request: GoogleSearchRequest = Body(...)):
    agent = GoogleSearchAgent(api_key=GOOGLE_API_KEY, cx_id=GOOGLE_CX_ID)
    results = agent.search(request.query)
    items = [
        GoogleSearchResultItem(
            title=item.get("title", ""),
            link=item.get("link", ""),
            snippet=item.get("snippet", "")
        ) for item in results
    ]
    return GoogleSearchResponse(results=items)

@router.post("/openai_search", response_model=OpenAIResponse)
def openai_search(request: OpenAIRequest = Body(...)):
    try:
        result = run_agent_with_search(request.messages)
        return OpenAIResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
