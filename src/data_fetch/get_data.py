import pandas as pd
import os
from binance.client import Client
from datetime import datetime, timedelta


interval_map = {
    "1m": Client.KLINE_INTERVAL_1MINUTE,
    "5m": Client.KLINE_INTERVAL_5MINUTE,
    "15m": Client.KLINE_INTERVAL_15MINUTE,
    "30m": Client.KLINE_INTERVAL_30MINUTE,
    "1h": Client.KLINE_INTERVAL_1HOUR,
    "4h": Client.KLINE_INTERVAL_4HOUR,
    "1d": Client.KLINE_INTERVAL_1DAY
}

# Inputs from user
print("=== COLETA DE DADOS HISTÓRICOS DA BINANCE ===")
print(f"Intervalos disponíveis: {', '.join(interval_map.keys())}")

while True:
    interval_input = input("Digite o intervalo desejado (ex: 1m, 5m, 1h): ").strip()
    if interval_input in interval_map:
        interval = interval_map[interval_input]
        break
    print(f"❌ Intervalo inválido. Use: {', '.join(interval_map.keys())}")

days = int(input("Quantos dias de dados deseja coletar? "))

symbols_input = input("Digite os símbolos separados por vírgula (ex: BTCUSDT,ETHUSDT,BNBUSDT): ")
symbols = [s.strip().upper() for s in symbols_input.split(",")]

# Colect Period
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=days)

start_str = start_date.strftime("%d %b %Y %H:%M:%S")
end_str = end_date.strftime("%d %b %Y %H:%M:%S")

# Create destin folder (out of src)
data_path = os.path.join("..", "..", "data", "raw")
os.makedirs(data_path, exist_ok=True)

# Conect API from Binance
client = Client()

# Funtion to formate klines
def format_klines_to_df(klines):
    df = pd.DataFrame(klines, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    df = df[["open_time", "open", "high", "low", "close", "volume"]]
    return df

# Loop
for symbol in symbols:
    print(f"🔄 Coletando {days} dias de {symbol} em candles de {interval_input}...")
    klines = client.get_historical_klines(symbol, interval, start_str, end_str)
    df = format_klines_to_df(klines)

    filename = f"{symbol}_{interval_input}_{days}d.csv"
    filepath = os.path.join(data_path, filename)
    df.to_csv(filepath, index=False)
    print(f"✅ {symbol} salvo: {filepath} ({len(df)} candles)")
