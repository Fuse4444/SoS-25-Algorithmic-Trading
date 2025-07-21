import time
import os
import sqlite3
from datetime import datetime
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

client = TradingClient(
    os.getenv("APCA_API_KEY_ID"),
    os.getenv("APCA_API_SECRET_KEY"),
    paper=True
)

# Set up SQLite database connection
conn = sqlite3.connect("trades.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    qty INTEGER,
    timestamp TEXT
)
""")
conn.commit()

def twap(symbol, qty, duration, interval):
    slices = int(duration / interval)
    slice_qty = qty // slices

    print(f"\nStarting TWAP for {symbol}: {qty} shares over {duration}s ({slices} slices every {interval}s)\n")

    for i in range(slices):
        order = MarketOrderRequest(
            symbol=symbol,
            qty=int(slice_qty),
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY
        )
        response = client.submit_order(order)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Log to console
        print(f"[{timestamp}] Order {i+1}/{slices} placed for {symbol}: {slice_qty} shares")

        # Insert into database
        cursor.execute(
            "INSERT INTO trades (symbol, qty, timestamp) VALUES (?, ?, ?)",
            (symbol, int(slice_qty), timestamp)
        )
        conn.commit()

        time.sleep(interval)

    print("\n✅ TWAP execution completed.\n")

# Run the strategy
if __name__ == "__main__":
    twap("AAPL", 10, duration=60, interval=10)
    conn.close()
