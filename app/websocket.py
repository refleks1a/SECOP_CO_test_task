import json
import httpx
import asyncio
from fastapi import WebSocket, WebSocketDisconnect


COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
COIN_SYMBOLS = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "ltc": "litecoin",
}

# Retrieve coin prices
async def fetch_coin_price(symbol: str):
    coin_id = COIN_SYMBOLS.get(symbol.lower())
    
    if not coin_id:
        return None
    
    params = {"ids": coin_id, "vs_currencies": "usd"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(COINGECKO_API_URL, params=params)
        if resp.status_code == 200:
            data = resp.json()
            price = data.get(coin_id, {}).get("usd")
            if price is not None:
                return {"symbol": symbol.upper(), "price": price, "currency": "USD"}

    return None


async def coin_track_ws(websocket: WebSocket):
    await websocket.accept()
    
    current_symbol = None
    update_task = None
    stop_event = asyncio.Event()

    async def send_price_updates():
        while not stop_event.is_set():
            if current_symbol:
                price_data = await fetch_coin_price(current_symbol)
                if price_data:
                    await websocket.send_json(price_data)
                else:
                    await websocket.send_json({"error": "Invalid symbol or price not found"})
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=5)
            except asyncio.TimeoutError:
                continue

    try:
        while True:
            data = await websocket.receive_text()
            try:
                req = json.loads(data)
                symbol = req.get("symbol")
                if not symbol:
                    await websocket.send_json({"error": "Missing symbol"})
                    continue
                if symbol != current_symbol:
                    current_symbol = symbol
                    if update_task:
                        stop_event.set()
                        await update_task
                        stop_event.clear()
                    # Send price immediately
                    price_data = await fetch_coin_price(current_symbol)
                    if price_data:
                        await websocket.send_json(price_data)
                    else:
                        await websocket.send_json({"error": "Invalid symbol or price not found"})
                    # Start background update task
                    update_task = asyncio.create_task(send_price_updates())
            except Exception as e:
                await websocket.send_json({"error": str(e)})
    except WebSocketDisconnect:
        if update_task:
            stop_event.set()
            await update_task
        pass
