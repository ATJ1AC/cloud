from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx
import os

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = "default-model"

class ChatResponse(BaseModel):
    response: str
    model: str

class NewsRequest(BaseModel):
    query: str = "latest news"
    max_results: Optional[int] = 5

class NewsItem(BaseModel):
    title: str
    description: str
    url: str
    published_at: Optional[str] = None

class NewsResponse(BaseModel):
    articles: list[NewsItem]

# Using NewsAPI - you can get a free key at https://newsapi.org/
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "public-api-key")
NEWS_API_URL = "https://newsapi.org/v2/everything"

@router.post("/chat")
async def chat_with_ai(request: ChatRequest):
    # This is a placeholder implementation
    # In a real application, this would connect to an AI service like Ollama
    mock_responses = {
        "hello": "Hello! I'm your AI assistant. How can I help you today?",
        "how are you": "I'm just a program, but I'm functioning optimally! How can I assist you?",
        "what is sh7omylab": "Sh7omyLab is a personal cloud portal with storage, notes, calendar, and AI assistance features.",
        "news": "For real-time news, please use the /news endpoint. Or ask me specific questions about recent events!",
        "default": f"I received your message: '{request.message}'. In a real implementation, I would connect to an AI model like Ollama for processing."
    }
    
    response_text = mock_responses.get(request.message.lower(), mock_responses["default"])
    return ChatResponse(response=response_text, model=request.model)

@router.post("/news", response_model=NewsResponse)
async def get_news(request: NewsRequest):
    """
    Fetch real news based on the query.
    This endpoint connects to a news API to fetch real-time news.
    """
    try:
        # Using NewsAPI to fetch real news
        params = {
            'q': request.query,
            'sortBy': 'publishedAt',
            'pageSize': request.max_results,
            'apiKey': NEWS_API_KEY
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(NEWS_API_URL, params=params)
            
        if response.status_code != 200:
            # Return empty results if API key is invalid or other error occurs
            return NewsResponse(articles=[])
        
        data = response.json()
        
        # Convert API response to our NewsItem format
        articles = []
        for item in data.get('articles', [])[:request.max_results]:
            articles.append(NewsItem(
                title=item['title'],
                description=item['description'],
                url=item['url'],
                published_at=item['publishedAt']
            ))
        
        return NewsResponse(articles=articles)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@router.get("/models")
async def get_available_models():
    # This would connect to Ollama or another AI service to list available models
    # Returning mock data for now
    return {
        "models": [
            {"name": "llama2", "size": "7B", "description": "Llama 2 7B model"},
            {"name": "mistral", "size": "7B", "description": "Mistral 7B model"},
            {"name": "gemma", "size": "2B", "description": "Gemma 2B model"}
        ]
    }