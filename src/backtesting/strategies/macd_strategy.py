import pandas as pd
import numpy as np

def macd_strategy(df, current_index, fast_period=12, slow_period=26, signal_period=9):
    """
    Estratégia MACD (Moving Average Convergence Divergence)
    - Compra: MACD cruza acima da linha de sinal
    - Venda: MACD cruza abaixo da linha de sinal
    """
    if current_index < slow_period + signal_period:
        return 0
    
    # Calcula MACD
    closes = df['close'].iloc[:current_index+1]
    ema_fast = closes.ewm(span=fast_period).mean()
    ema_slow = closes.ewm(span=slow_period).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal_period).mean()
    
    # Valores atuais e anteriores
    current_macd = macd_line.iloc[-1]
    current_signal = signal_line.iloc[-1]
    prev_macd = macd_line.iloc[-2]
    prev_signal = signal_line.iloc[-2]
    
    # Sinais de cruzamento
    if current_macd > current_signal and prev_macd <= prev_signal:
        return 1  # Compra
    elif current_macd < current_signal and prev_macd >= prev_signal:
        return -1  # Venda
    
    return 0

def macd_histogram_strategy(df, current_index):
    """
    Estratégia MACD com histograma
    - Compra: Histograma muda de negativo para positivo
    - Venda: Histograma muda de positivo para negativo
    """
    if current_index < 35:
        return 0
    
    closes = df['close'].iloc[:current_index+1]
    ema_12 = closes.ewm(span=12).mean()
    ema_26 = closes.ewm(span=26).mean()
    macd_line = ema_12 - ema_26
    signal_line = macd_line.ewm(span=9).mean()
    histogram = macd_line - signal_line
    
    current_hist = histogram.iloc[-1]
    prev_hist = histogram.iloc[-2]
    
    # Mudança de sinal no histograma
    if current_hist > 0 and prev_hist <= 0:
        return 1  # Compra
    elif current_hist < 0 and prev_hist >= 0:
        return -1  # Venda
    
    return 0