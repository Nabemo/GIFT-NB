import asyncio
from aiogram import Bot, Dispatcher
import requests
from config import *

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class NFTMonitor:
    def __init__(self):
        self.last_prices = {}
        self.market_price = None

    async def get_market_price(self):
        url = f"https://tonapi.io/v2/nfts/collections/{COLLECTION}/stats"
        headers = {"Authorization": f"Bearer {TONAPI_KEY}"}
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            return data.get("floor_price", {}).get("value", 0) / 1e9  # Конвертация в TON
        except Exception as e:
            print(f"Ошибка получения рыночной цены: {e}")
            return None

    async def check_discounts(self):
        while True:
            self.market_price = await self.get_market_price()
            if not self.market_price:
                await asyncio.sleep(300)
                continue

            url = f"https://tonapi.io/v2/nfts/collections/{COLLECTION}/items"
            headers = {"Authorization": f"Bearer {TONAPI_KEY}"}
            
            try:
                response = requests.get(url, headers=headers)
                items = response.json().get("nft_items", [])
                
                for item in items:
                    if not item.get("sale"):
                        continue
                        
                    item_id = item["address"]
                    price = int(item["sale"]["price"]["amount"]) / 1e9
                    threshold = self.market_price * (1 - DISCOUNT)
                    
                    if price < threshold:
                        if item_id not in self.last_prices or price < self.last_prices[item_id]:
                            await self.send_alert(item, price)
                        self.last_prices[item_id] = price
                        
            except Exception as e:
                print(f"Ошибка при проверке NFT: {e}")
            
            await asyncio.sleep(CHECK_INTERVAL)

    async def send_alert(self, item, price):
        name = item["metadata"].get("name", "NFT без названия")
        url = f"https://getgems.io/nft/{item['address']}"
        
        message = (
            f"🎁 Найден подарок со скидкой!\n\n"
            f"📛 Название: {name}\n"
            f"💰 Цена: {price:.2f} TON (Рыночная: {self.market_price:.2f} TON)\n"
            f"🔗 Ссылка: {url}"
        )
        
        await bot.send_message(chat_id=CHAT_ID, text=message)

monitor = NFTMonitor()

async def main():
    await monitor.check_discounts()

if __name__ == "__main__":
    asyncio.run(main())