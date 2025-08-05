from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

bot = Bot(token=os.getenv("7833462753:AAHFvHWIT18D8CzSYA5Vqg1IBbPllcsV6gE"))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("🔍 Бот активен! Мониторим NFT-подарки в Tonnel...")

async def on_startup(dp):
    await bot.set_webhook("https://gift-nb-nabemo53s-projects.vercel.app/webhook")

if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path='/webhook',
        on_startup=on_startup,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )