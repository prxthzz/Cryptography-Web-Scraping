from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import datetime
import os

cg = CoinGeckoAPI()
coins = cg.get_coins_markets('usd', per_page=10, page=1)

data = []
for coin in coins:
    data.append({
        "Timestamp": f"2025-12-05 {datetime.now().strftime('%H:%M:%S')}",  # Static format
        "Coin": coin['name'],
        "Price": str(coin['current_price']) + " USD",
        "24h_Change": str(round(coin['price_change_percentage_24h'], 2)) + "%" if coin['price_change_percentage_24h'] else "0%",
        "Market_Cap": str(int(coin['market_cap'])) if coin['market_cap'] else "0"
    })

df = pd.DataFrame(data)

# FIX: Force text format for CSV (no # symbols)
df['Timestamp'] = "'" + df['Timestamp']  # Excel text prefix
df['Price'] = "'" + df['Price']          # Prevent number formatting

csv_file = 'crypto_prices.csv'
if os.path.exists(csv_file):
    existing = pd.read_csv(csv_file)
    df = pd.concat([existing, df], ignore_index=True)

df.to_csv(csv_file, index=False, encoding='utf-8-sig')  # BOM for Excel
print("✅ PERFECT CSV SAVED - No # symbols!")
print(df)
