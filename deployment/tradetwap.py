import time
import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from dotenv import load_dotenv

load_dotenv()

client = TradingClient(os.getenv("APCA_API_KEY_ID"), os.getenv("APCA_API_SECRET_KEY"), paper=True)

def twap(symbol, qty, duration, interval):
    slices = int(duration / interval)
    slice_qty = qty // slices

    for i in range(slices):
        order = MarketOrderRequest(symbol=symbol, qty=slice_qty, side=OrderSide.BUY, time_in_force=TimeInForce.DAY)
        client.submit_order(order)
        print(f"TWAP Order {i+1}/{slices} placed.")
        time.sleep(interval)

twap("AAPL", 10, duration=60, interval=10)