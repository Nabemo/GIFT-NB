from fastapi import FastAPI, Request, HTTPException
import os

app = FastAPI()
TONCONSOLE_TOKEN = "68d1d2e5c4734ed3bb788343320071b2"

@app.post("/tonconsole-webhook")
async def handle_webhook(request: Request):
    # Проверка авторизации
    if request.headers.get("Authorization") != f"Bearer {TONCONSOLE_TOKEN}":
        raise HTTPException(status_code=403)
    
    data = await request.json()
    event_type = data.get("event")
    
    # Обработка событий
    if event_type == "nft_purchase":
        return {"status": "ok", "message": "NFT purchase processed"}
    elif event_type == "transaction":
        return {"status": "ok", "message": "Transaction processed"}
    
    return {"status": "ok"}