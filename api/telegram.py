from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import os

bot = Bot(token="7833462753:AAHFvHWIT18D8CzSYA5Vqg1IBbPllcsV6gE")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🛠️ Бот для работы с TonConsole\n\n"
        "Доступные команды:\n"
        "/balance - Проверить баланс\n"
        "/help - Помощь"
    )

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Техподдержка: @ваш_аккаунт")

async def handle_webhook(request):
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != os.getenv("TG_SECRET"):
        return {"statusCode": 403}
    
    update = types.Update(**request.json)
    await dp.feed_update(bot, update)
    return {"statusCode": 200}

if __name__ == "__main__":
    from fastapi import FastAPI
    app = FastAPI()
    app.post("/telegram-webhook")(handle_webhook)