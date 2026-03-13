import os
from typing import Optional, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from agent import process_message, clear_session
from training_agent import process_training_message

load_dotenv()

app = FastAPI(title="AI Coding Assistant")

# CORS middleware (for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request / Response Models
# -----------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    error: Optional[str] = None
    tools_used: List[str] = []

class TrainingChatRequest(BaseModel):
    message: str
    session_id: str = "training_default"

class TrainingProgressResponse(BaseModel):
    week: int
    topic: Optional[str]
    active_task: Optional[dict]
    metrics: dict

class TrainingChatResponse(BaseModel):
    response: str
    state: Optional[TrainingProgressResponse] = None
    error: Optional[str] = None

class ClearRequest(BaseModel):
    session_id: str = "default"

# -----------------------------
# Training Endpoints
# -----------------------------

@app.post("/api/training/chat", response_model=TrainingChatResponse)
async def training_chat(request: TrainingChatRequest):
    try:
        result = process_training_message(
            request.message,
            session_id=request.session_id
        )
        return TrainingChatResponse(
            response=result["response"],
            state=result["state"],
            error=result["error"]
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return TrainingChatResponse(response="", error=str(e))


# -----------------------------
# Chat Endpoint
# -----------------------------

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = process_message(
            request.message,
            session_id=request.session_id
        )

        response_text = result.get("response", "")

        # If response is a list (LangGraph format), extract text parts
        if isinstance(response_text, list):
            parts = []
            for item in response_text:
                if isinstance(item, dict) and "text" in item:
                    parts.append(item["text"])
                elif isinstance(item, str):
                    parts.append(item)
                else:
                    parts.append(str(item))
            response_text = " ".join(parts)

        # Ensure response_text is always a string
        if not isinstance(response_text, str):
            response_text = str(response_text)

        # Build response — only include error if it's a non-None string
        error_val = result.get("error")
        
        return ChatResponse(
            response=response_text or "No response generated.",
            error=error_val if isinstance(error_val, str) else None,
            tools_used=result.get("tools_used", []),
        )

    except Exception as e:
        import traceback
        traceback.print_exc()

        return ChatResponse(
            response="",
            error=str(e),
            tools_used=[]
        )

# -----------------------------
# Clear Session Endpoint
# -----------------------------

@app.post("/api/clear")
async def clear(request: ClearRequest):
    cleared = clear_session(request.session_id)

    return {
        "cleared": cleared,
        "session_id": request.session_id
    }


# -----------------------------
# Run Server
# -----------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )