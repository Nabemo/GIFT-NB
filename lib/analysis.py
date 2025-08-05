async def analyze_market(orders):
    if not orders:
        return {"floor_price": 0, "avg_price": 0}
    
    prices = [order["price"] for order in orders]
    floor_price = min(prices)
    avg_price = sum(prices) / len(prices)
    
    return {"floor_price": floor_price, "avg_price": round(avg_price, 2)}

def find_undervalued(orders, market_data, discount=0.1):
    return [order for order in orders if order["price"] < market_data["floor_price"] * (1 - discount)]