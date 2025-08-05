import requests
import os

async def send_telegram_alert(deal, chat_id):
    message = (
        f"🎁 **Срочно! Выгодная покупка**\n\n"
        f"Подарок: {deal['name']}\n"
        f"💵 Цена: {deal['price']} TON\n"
        f"🔗 [Купить сейчас]({deal['url']})"
    )
    
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    })