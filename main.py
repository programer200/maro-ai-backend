from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-669e06f654ec4d46878adfca7887c718")
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": request.message}],
        }
        response = requests.post(DEEPSEEK_URL, headers=headers, json=payload)
        response.raise_for_status()
        return {"response": response.json()["choices"][0]["message"]["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))