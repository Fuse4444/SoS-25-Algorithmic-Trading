import asyncio
from alpaca.data.live import StockDataStream
from dotenv import load_dotenv
import os

load_dotenv()

KEY = os.getenv("APCA_API_KEY_ID")
SECRET = os.getenv("APCA_API_SECRET_KEY")

stream = StockDataStream(KEY, SECRET)

async def handle_trade(data):
    print("Trade:", data)

async def main():
    stream.subscribe_trades(handle_trade, "AAPL")
    await stream._run_forever()

asyncio.run(main())