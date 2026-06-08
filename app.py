import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI()

# Разрешаем запросы от твоего HTML-сайта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Твои данные (токен уже внутри, ID обновили)
TELEGRAM_TOKEN = "8873438917:AAGvBRBoSc-9KLlfV2eYCWtMVP_YvWs_syo"
CHAT_ID = "6156911952" 

class ReplyModel(BaseModel):
    answer: str

@app.post("/api/reply")
async def handle_reply(data: ReplyModel):
    tg_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(tg_url, json={
            "chat_id": CHAT_ID,
            "text": data.answer
        })
        
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Ошибка отправки в Telegram")
        
    return {"status": "success"}
