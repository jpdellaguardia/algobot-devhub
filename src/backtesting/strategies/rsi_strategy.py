import pandas as pd
import numpy as np

def rsi_strategy(df, current_index, period=14, oversold=30, overbought=70):
    """
    Estratégia RSI (Relative Strength Index)
    - Compra: RSI < oversold (sobrevenda)
    - Venda: RSI > overbought (sobrecompra)
    """
    if current_index < period:
        return 0
    
    closes = df['close'].iloc[current_index-period:current_index+1]
    delta = closes.diff()
    gain = (delta.where(delta > 0, 0)).mean()
    loss = (-delta.where(delta < 0, 0)).mean()
    
    if loss == 0:
        return 0
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    if rsi < oversold:
        return 1  # Compra
    elif rsi > overbought:
        return -1  # Venda
    
    return 0

def rsi_divergence_strategy(df, current_index, period=14):
    """
    Estratégia RSI com divergência
    - Identifica divergências entre preço e RSI
    """
    if current_index < period + 10:
        return 0
    
    # Calcula RSI para os últimos pontos
    rsi_values = []
    for i in range(current_index-10, current_index+1):
        closes = df['close'].iloc[i-period:i+1]
        delta = closes.diff()
        gain = (delta.where(delta > 0, 0)).mean()
        loss = (-delta.where(delta < 0, 0)).mean()
        
        if loss == 0:
            rsi_values.append(50)
        else:
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)
    
    current_rsi = rsi_values[-1]
    current_price = df['close'].iloc[current_index]
    
    # Verifica divergência bullish (preço baixo, RSI alto)
    if (current_rsi > 40 and current_rsi < 60 and 
        current_price < df['close'].iloc[current_index-5:current_index].mean()):
        return 1
    
    # Verifica divergência bearish (preço alto, RSI baixo)
    if (current_rsi > 40 and current_rsi < 60 and 
        current_price > df['close'].iloc[current_index-5:current_index].mean()):
        return -1
    
    return 0

def rsi_mean_reversion_strategy(df, current_index, period=14):
    """
    Estratégia RSI de reversão à média
    - Compra em RSI muito baixo
    - Venda em RSI muito alto
    """
    if current_index < period:
        return 0
    
    closes = df['close'].iloc[current_index-period:current_index+1]
    delta = closes.diff()
    gain = (delta.where(delta > 0, 0)).mean()
    loss = (-delta.where(delta < 0, 0)).mean()
    
    if loss == 0:
        return 0
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Níveis mais extremos para reversão
    if rsi < 20:
        return 1  # Compra forte
    elif rsi > 80:
        return -1  # Venda forte
    
    return 0