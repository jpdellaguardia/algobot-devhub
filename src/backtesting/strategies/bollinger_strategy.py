import pandas as pd
import numpy as np

def bollinger_bands_strategy(df, current_index, period=20, std_dev=2):
    """
    Estratégia Bollinger Bands
    - Compra: Preço toca banda inferior
    - Venda: Preço toca banda superior
    """
    if current_index < period:
        return 0
    
    closes = df['close'].iloc[current_index-period:current_index+1]
    sma = closes.mean()
    std = closes.std()
    
    upper_band = sma + (std_dev * std)
    lower_band = sma - (std_dev * std)
    current_price = df['close'].iloc[current_index]
    
    # Sinais nas bandas
    if current_price <= lower_band:
        return 1  # Compra na banda inferior
    elif current_price >= upper_band:
        return -1  # Venda na banda superior
    
    return 0

def bollinger_squeeze_strategy(df, current_index, period=20):
    """
    Estratégia Bollinger Squeeze
    - Identifica períodos de baixa volatilidade seguidos de breakout
    """
    if current_index < period + 10:
        return 0
    
    # Calcula Bollinger Bands atual
    closes = df['close'].iloc[current_index-period:current_index+1]
    sma = closes.mean()
    std = closes.std()
    band_width = (std * 4) / sma * 100  # Largura das bandas em %
    
    # Calcula largura média das últimas 10 períodos
    avg_width = 0
    for i in range(10):
        past_closes = df['close'].iloc[current_index-period-i:current_index-i+1]
        past_std = past_closes.std()
        past_sma = past_closes.mean()
        past_width = (past_std * 4) / past_sma * 100
        avg_width += past_width
    avg_width /= 10
    
    current_price = df['close'].iloc[current_index]
    prev_price = df['close'].iloc[current_index-1]
    
    # Squeeze: largura atual menor que média E breakout
    if band_width < avg_width * 0.8:
        if current_price > prev_price * 1.005:  # Breakout para cima
            return 1
        elif current_price < prev_price * 0.995:  # Breakout para baixo
            return -1
    
    return 0

def bollinger_mean_reversion_strategy(df, current_index, period=20):
    """
    Estratégia Bollinger de reversão à média
    - Compra quando preço volta da banda inferior para a média
    - Venda quando preço volta da banda superior para a média
    """
    if current_index < period + 2:
        return 0
    
    # Bandas atuais
    closes = df['close'].iloc[current_index-period:current_index+1]
    sma = closes.mean()
    std = closes.std()
    upper_band = sma + (2 * std)
    lower_band = sma - (2 * std)
    
    current_price = df['close'].iloc[current_index]
    prev_price = df['close'].iloc[current_index-1]
    prev2_price = df['close'].iloc[current_index-2]
    
    # Reversão da banda inferior
    if (prev2_price <= lower_band and 
        prev_price > lower_band and 
        current_price > prev_price):
        return 1
    
    # Reversão da banda superior
    if (prev2_price >= upper_band and 
        prev_price < upper_band and 
        current_price < prev_price):
        return -1
    
    return 0

def bollinger_trend_strategy(df, current_index, period=20):
    """
    Estratégia Bollinger de tendência
    - Compra: Preço consistentemente acima da média móvel
    - Venda: Preço consistentemente abaixo da média móvel
    """
    if current_index < period + 5:
        return 0
    
    closes = df['close'].iloc[current_index-period:current_index+1]
    sma = closes.mean()
    current_price = df['close'].iloc[current_index]
    
    # Verifica se preço está acima/abaixo da média nos últimos 5 períodos
    recent_prices = df['close'].iloc[current_index-4:current_index+1]
    above_sma = all(price > sma for price in recent_prices)
    below_sma = all(price < sma for price in recent_prices)
    
    if above_sma and current_price > sma * 1.01:
        return 1  # Tendência de alta
    elif below_sma and current_price < sma * 0.99:
        return -1  # Tendência de baixa
    
    return 0