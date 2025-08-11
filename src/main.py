import pandas as pd
from backtesting.strategies import sma_cross
from backtesting.engine_example import backtest

# Load dados limpos
df = pd.read_csv("data/processed/BTCUSDT_1m_clean.csv", parse_dates=['open_time'])

# Gerar sinais
df = sma_cross.generate_signals(df)

# Rodar o backtest
final_balance, operations = backtest(df)

print(f"💰 Resultado final: ${final_balance:.2f}")

#yolo