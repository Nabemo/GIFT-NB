import requests
import os

TONAPI_KEY = os.getenv("TONAPI_KEY")

async def fetch_orders(collection_address: str):
    url = f"https://tonapi.io/v2/nfts/collections/{collection_address}/items?on_sale=true"
    headers = {"Authorization": f"Bearer {AEBP3JJVEO56ZCAAAAACZI7HVAFNW7II3RRQBOTGNGCYH4YYSBQSQ2XVQELRX4RBBWEODSI}"}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    return [
        {
            "address": item["address"],
            "price": int(item["sale"]["price"]["amount"]) / 1e9,
            "url": f"https://getgems.io/nft/{item['address']}",
            "name": item["metadata"]["name"]
        }
        for item in data.get("nft_items", []) if item.get("sale")
    ]