import pandas as pd
import numpy as np

def rulebased_strategy(df, current_index):
    """
    Multiple rules-based strategy:
    - RSI to identify overbought/oversold conditions
    - Moving averages for trend
    - Volume for confirmation
    """
    if current_index < 50:  # Need sufficient history
        return 0
    
    # Current data
    current_data = df.iloc[current_index]
    recent_data = df.iloc[current_index-20:current_index]
    
    # Rule 1: RSI
    rsi = calculate_rsi(df, current_index, period=14)
    
    # Rule 2: Moving averages
    sma_short = df['close'].iloc[current_index-10:current_index].mean()
    sma_long = df['close'].iloc[current_index-30:current_index].mean()
    
    # Rule 3: Volume
    avg_volume = recent_data['volume'].mean()
    current_volume = current_data['volume']
    
    # Rule 4: Momentum
    price_change = (current_data['close'] - df['close'].iloc[current_index-5]) / df['close'].iloc[current_index-5] * 100
    
    # BUY conditions
    buy_conditions = [
        rsi < 35,                           # RSI oversold
        sma_short > sma_long,               # Uptrend
        current_volume > avg_volume * 1.2,  # Volume above average
        price_change > -2                   # Not falling too much
    ]
    
    # SELL conditions
    sell_conditions = [
        rsi > 65,                           # RSI overbought
        sma_short < sma_long,               # Downtrend
        current_volume > avg_volume * 1.1,  # Volume confirming
        price_change < 1                    # Weak momentum
    ]
    
    # Decision based on rules
    buy_score = sum(buy_conditions)
    sell_score = sum(sell_conditions)
    
    # Need at least 3 conditions to trade
    if buy_score >= 3:
        return 1  # Buy
    elif sell_score >= 3:
        return -1  # Sell
    
    return 0  # Hold

def calculate_rsi(df, current_index, period=14):
    """Calculates RSI for current index"""
    if current_index < period:
        return 50
    
    closes = df['close'].iloc[current_index-period:current_index]
    delta = closes.diff()
    gain = (delta.where(delta > 0, 0)).mean()
    loss = (-delta.where(delta < 0, 0)).mean()
    
    if loss == 0:
        return 100
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def advanced_rulebased_strategy(df, current_index):
    """
    Estratégia avançada com mais regras:
    - Bollinger Bands
    - MACD
    - Support/Resistance
    """
    if current_index < 50:
        return 0
    
    current_price = df['close'].iloc[current_index]
    
    # Bollinger Bands
    sma_20 = df['close'].iloc[current_index-20:current_index].mean()
    std_20 = df['close'].iloc[current_index-20:current_index].std()
    bb_upper = sma_20 + (2 * std_20)
    bb_lower = sma_20 - (2 * std_20)
    
    # MACD
    ema_12 = df['close'].iloc[current_index-12:current_index].ewm(span=12).mean().iloc[-1]
    ema_26 = df['close'].iloc[current_index-26:current_index].ewm(span=26).mean().iloc[-1]
    macd = ema_12 - ema_26
    
    # Support/Resistance (mínimos e máximos locais)
    recent_highs = df['high'].iloc[current_index-10:current_index]
    recent_lows = df['low'].iloc[current_index-10:current_index]
    resistance = recent_highs.max()
    support = recent_lows.min()
    
    # RSI
    rsi = calculate_rsi(df, current_index)
    
    # Regras de COMPRA
    buy_rules = [
        current_price <= bb_lower,          # Preço na banda inferior
        macd > 0,                          # MACD positivo
        current_price > support * 1.01,    # Acima do suporte
        rsi < 40,                          # RSI oversold
        df['volume'].iloc[current_index] > df['volume'].iloc[current_index-10:current_index].mean()
    ]
    
    # Regras de VENDA
    sell_rules = [
        current_price >= bb_upper,          # Preço na banda superior
        macd < 0,                          # MACD negativo
        current_price < resistance * 0.99,  # Abaixo da resistência
        rsi > 60,                          # RSI overbought
        df['volume'].iloc[current_index] > df['volume'].iloc[current_index-5:current_index].mean()
    ]
    
    # Decisão
    if sum(buy_rules) >= 4:
        return 1
    elif sum(sell_rules) >= 4:
        return -1
    
    return 0

def conservative_rulebased_strategy(df, current_index):
    """
    Estratégia conservadora com regras rígidas
    """
    if current_index < 30:
        return 0
    
    # Apenas regras muito conservadoras
    rsi = calculate_rsi(df, current_index)
    sma_10 = df['close'].iloc[current_index-10:current_index].mean()
    sma_20 = df['close'].iloc[current_index-20:current_index].mean()
    current_price = df['close'].iloc[current_index]
    
    # Compra apenas em condições muito favoráveis
    if (rsi < 25 and 
        sma_10 > sma_20 and 
        current_price > sma_10 * 0.98):
        return 1
    
    # Venda apenas em condições muito desfavoráveis
    if (rsi > 75 and 
        sma_10 < sma_20 and 
        current_price < sma_10 * 1.02):
        return -1
    
    return 0