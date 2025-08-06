from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os

bot = Bot(token="7833462753:AAHFvHWIT18D8CzSYA5Vqg1IBbPllcsV6gE")
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("✅ Бот активирован! Вот что я умею:\n\n"
                        "/help - Показать справку\n"
                        "/check - Проверить статус")

async def handle_webhook(request):
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != os.getenv("TG_SECRET"):
        return {"statusCode": 403}
    
    update = types.Update(**request.json)
    await dp.feed_update(bot, update)
    return {"statusCode": 200}