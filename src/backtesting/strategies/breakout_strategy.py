import pandas as pd
import numpy as np

def support_resistance_breakout(df, current_index, lookback=20, breakout_threshold=0.01):
    """
    Support/Resistance breakout strategy
    - Buy: Resistance breakout
    - Sell: Support breakout
    """
    if current_index < lookback:
        return 0
    
    # Recent data
    recent_data = df.iloc[current_index-lookback:current_index]
    current_price = df['close'].iloc[current_index]
    
    # Identify support and resistance
    resistance = recent_data['high'].max()
    support = recent_data['low'].min()
    
    # Resistance breakout (buy)
    if current_price > resistance * (1 + breakout_threshold):
        return 1
    
    # Support breakout (sell)
    if current_price < support * (1 - breakout_threshold):
        return -1
    
    return 0

def volume_breakout_strategy(df, current_index, lookback=20, volume_multiplier=1.5):
    """
    Volume-confirmed breakout strategy
    - Breakout must be accompanied by high volume
    """
    if current_index < lookback:
        return 0
    
    recent_data = df.iloc[current_index-lookback:current_index]
    current_price = df['close'].iloc[current_index]
    current_volume = df['volume'].iloc[current_index]
    avg_volume = recent_data['volume'].mean()
    
    resistance = recent_data['high'].max()
    support = recent_data['low'].min()
    
    # Volume must be above average
    if current_volume > avg_volume * volume_multiplier:
        if current_price > resistance * 1.005:
            return 1  # Resistance breakout with volume
        elif current_price < support * 0.995:
            return -1  # Support breakout with volume
    
    return 0

def range_breakout_strategy(df, current_index, range_period=15, min_range=0.02):
    """
    Estratégia de breakout de range
    - Identifica períodos de consolidação e opera breakouts
    """
    if current_index < range_period + 5:
        return 0
    
    # Período de consolidação
    range_data = df.iloc[current_index-range_period:current_index]
    range_high = range_data['high'].max()
    range_low = range_data['low'].min()
    range_size = (range_high - range_low) / range_low
    
    # Só opera se o range for significativo
    if range_size < min_range:
        return 0
    
    current_price = df['close'].iloc[current_index]
    
    # Breakout do range
    if current_price > range_high * 1.002:
        return 1  # Breakout para cima
    elif current_price < range_low * 0.998:
        return -1  # Breakout para baixo
    
    return 0

def pivot_breakout_strategy(df, current_index, pivot_period=10):
    """
    Estratégia baseada em pivot points
    - Identifica pontos de pivô e opera breakouts
    """
    if current_index < pivot_period * 2:
        return 0
    
    # Encontra pivot highs e lows
    recent_highs = []
    recent_lows = []
    
    for i in range(current_index - pivot_period, current_index):
        window = df.iloc[i-pivot_period:i+pivot_period+1]
        if len(window) < pivot_period * 2 + 1:
            continue
            
        center_high = window['high'].iloc[pivot_period]
        center_low = window['low'].iloc[pivot_period]
        
        # Pivot high
        if center_high == window['high'].max():
            recent_highs.append(center_high)
        
        # Pivot low
        if center_low == window['low'].min():
            recent_lows.append(center_low)
    
    if not recent_highs or not recent_lows:
        return 0
    
    current_price = df['close'].iloc[current_index]
    last_pivot_high = max(recent_highs)
    last_pivot_low = min(recent_lows)
    
    # Breakout dos pivots
    if current_price > last_pivot_high * 1.005:
        return 1
    elif current_price < last_pivot_low * 0.995:
        return -1
    
    return 0

def donchian_breakout_strategy(df, current_index, period=20):
    """
    Estratégia Donchian Channel Breakout
    - Compra: Novo máximo do período
    - Venda: Novo mínimo do período
    """
    if current_index < period:
        return 0
    
    # Canal de Donchian
    recent_data = df.iloc[current_index-period:current_index]
    donchian_high = recent_data['high'].max()
    donchian_low = recent_data['low'].min()
    
    current_high = df['high'].iloc[current_index]
    current_low = df['low'].iloc[current_index]
    
    # Breakout do canal
    if current_high > donchian_high:
        return 1  # Novo máximo
    elif current_low < donchian_low:
        return -1  # Novo mínimo
    
    return 0

def false_breakout_filter_strategy(df, current_index, lookback=20, confirmation_periods=3):
    """
    Estratégia com filtro de falsos breakouts
    - Aguarda confirmação por alguns períodos
    """
    if current_index < lookback + confirmation_periods:
        return 0
    
    # Identifica suporte/resistência
    recent_data = df.iloc[current_index-lookback:current_index-confirmation_periods]
    resistance = recent_data['high'].max()
    support = recent_data['low'].min()
    
    # Verifica se breakout se manteve nos últimos períodos
    confirmation_data = df.iloc[current_index-confirmation_periods:current_index+1]
    current_price = df['close'].iloc[current_index]
    
    # Breakout de resistência confirmado
    if (current_price > resistance * 1.01 and 
        all(price > resistance for price in confirmation_data['close'])):
        return 1
    
    # Breakout de suporte confirmado
    if (current_price < support * 0.99 and 
        all(price < support for price in confirmation_data['close'])):
        return -1
    
    return 0