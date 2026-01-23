from fastapi import FastAPI
from pydantic import BaseModel
from llm import get_ai_response

app = FastAPI(title="Advanced AI Chatbot API")

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.post("/chat")
def chat(req: ChatRequest):
    messages = [
        {"role": "system", "content": "You are an advanced AI chatbot."}
    ]

    # add chat history
    messages.extend(req.history)

    # add current user message
    messages.append({"role": "user", "content": req.message})

    # get AI response
    reply = get_ai_response(messages)

    return {
        "reply": reply
    }
