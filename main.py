import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from models import ChatRequest
from chat_engine import get_response, query_documents
from crises import contains_crisis_keywords, SAFETY_MESSAGE
from logger import log_chat
from fastapi.middleware.cors import CORSMiddleware

# Load environment
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

app = FastAPI(
    title="Mental Health Chatbot API",
    description="A chatbot API for mental health support with document querying capabilities",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the Mental Health Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat - Chat with memory support",
            "doc_query": "/doc_query - Query documents",
            "health": "/health - Health check"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}

@app.post("/chat")
def chat_with_memory(request: ChatRequest):
    """Chat endpoint with session memory and crisis detection."""
    try:
        session_id = request.session_id
        user_query = request.query
        
        # Validate input
        if not session_id or not user_query:
            raise HTTPException(status_code=400, detail="Session ID and query are required")
        
        # Check for crisis keywords
        is_crisis = contains_crisis_keywords(user_query)
        
        if is_crisis:
            response = SAFETY_MESSAGE
        else:
            response = get_response(session_id, user_query)
        
        # Log the conversation
        log_chat(session_id, user_query, response, is_crisis)
        
        return {
            "response": response,
            "session_id": session_id,
            "crisis_detected": is_crisis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@app.post("/doc_query")
def chat_with_documents(request: ChatRequest):
    """Document querying endpoint."""
    try:
        if not request.query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        response = query_documents(request.query)
        
        return {
            "response": response,
            "query": request.query
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)