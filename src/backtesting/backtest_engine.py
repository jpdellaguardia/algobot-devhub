import pandas as pd
import numpy as np
from datetime import datetime
import os

class BacktestEngine:
    def __init__(self, initial_balance=10000, commission=0.001):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.commission = commission
        self.position = 0
        self.entry_price = 0
        self.trades = []
        self.equity_curve = []
        
    def buy(self, price, quantity, timestamp):
        """Executes buy order"""
        cost = quantity * price * (1 + self.commission)
        if cost <= self.balance:
            self.balance -= cost
            self.position += quantity
            self.entry_price = price
            self.trades.append({
                'type': 'BUY',
                'timestamp': timestamp,
                'price': price,
                'quantity': quantity,
                'cost': cost,
                'balance': self.balance
            })
            return True
        return False
    
    def sell(self, price, quantity, timestamp):
        """Executes sell order"""
        if quantity <= self.position:
            revenue = quantity * price * (1 - self.commission)
            self.balance += revenue
            self.position -= quantity
            
            profit = (price - self.entry_price) * quantity
            profit_pct = ((price - self.entry_price) / self.entry_price) * 100
            
            self.trades.append({
                'type': 'SELL',
                'timestamp': timestamp,
                'price': price,
                'quantity': quantity,
                'revenue': revenue,
                'profit': profit,
                'profit_pct': profit_pct,
                'balance': self.balance
            })
            return True
        return False
    
    def get_portfolio_value(self, current_price):
        """Calculates total portfolio value"""
        return self.balance + (self.position * current_price)
    
    def run_backtest(self, df, strategy_func):
        """Runs backtest with a strategy"""
        print("🚀 Starting backtest...")
        
        for i, row in df.iterrows():
            current_price = float(row['close'])
            timestamp = row['open_time']
            
            # Apply strategy
            signal = strategy_func(df, i)
            
            # Execute orders based on signal
            if signal == 1 and self.position == 0:  # Buy
                quantity = self.balance / current_price * 0.95  # 95% of balance
                self.buy(current_price, quantity, timestamp)
                
            elif signal == -1 and self.position > 0:  # Sell
                self.sell(current_price, self.position, timestamp)
            
            # Record equity curve
            portfolio_value = self.get_portfolio_value(current_price)
            self.equity_curve.append({
                'timestamp': timestamp,
                'portfolio_value': portfolio_value,
                'price': current_price
            })
    
    def get_performance_metrics(self):
        """Calculates performance metrics"""
        if not self.trades:
            return {"error": "No trades executed"}
        
        # Sell trades (profits/losses)
        sell_trades = [t for t in self.trades if t['type'] == 'SELL']
        
        if not sell_trades:
            return {"error": "No sell trades executed"}
        
        profits = [t['profit'] for t in sell_trades]
        profit_pcts = [t['profit_pct'] for t in sell_trades]
        
        total_return = sum(profits)
        total_return_pct = ((self.get_portfolio_value(self.trades[-1]['price']) - self.initial_balance) / self.initial_balance) * 100
        
        win_trades = [p for p in profits if p > 0]
        lose_trades = [p for p in profits if p < 0]
        
        metrics = {
            'total_trades': len(sell_trades),
            'winning_trades': len(win_trades),
            'losing_trades': len(lose_trades),
            'win_rate': len(win_trades) / len(sell_trades) * 100,
            'total_return': total_return,
            'total_return_pct': total_return_pct,
            'avg_profit': np.mean(profits),
            'avg_profit_pct': np.mean(profit_pcts),
            'max_profit': max(profits),
            'max_loss': min(profits),
            'final_balance': self.balance,
            'final_position': self.position
        }
        
        return metrics
    
    def print_summary(self):
        """Prints backtest summary"""
        metrics = self.get_performance_metrics()
        
        if "error" in metrics:
            print(f"❌ {metrics['error']}")
            return
        
        print("\n" + "="*50)
        print("📊 BACKTEST SUMMARY")
        print("="*50)
        print(f"💰 Initial balance: ${self.initial_balance:,.2f}")
        print(f"💰 Final balance: ${metrics['final_balance']:,.2f}")
        print(f"📈 Total return: {metrics['total_return_pct']:.2f}%")
        print(f"🔢 Total trades: {metrics['total_trades']}")
        print(f"✅ Winning trades: {metrics['winning_trades']} ({metrics['win_rate']:.1f}%)")
        print(f"❌ Losing trades: {metrics['losing_trades']}")
        print(f"📊 Average profit: ${metrics['avg_profit']:.2f} ({metrics['avg_profit_pct']:.2f}%)")
        print(f"🚀 Max profit: ${metrics['max_profit']:.2f}")
        print(f"📉 Max loss: ${metrics['max_loss']:.2f}")
        print("="*50)

# Example strategies
def sma_crossover_strategy(df, current_index, short_period=10, long_period=20):
    """Simple Moving Average crossover strategy"""
    if current_index < long_period:
        return 0
    
    short_sma = df['close'].iloc[current_index-short_period:current_index].mean()
    long_sma = df['close'].iloc[current_index-long_period:current_index].mean()
    prev_short_sma = df['close'].iloc[current_index-short_period-1:current_index-1].mean()
    prev_long_sma = df['close'].iloc[current_index-long_period-1:current_index-1].mean()
    
    # Buy signal: Short SMA crosses above long SMA
    if short_sma > long_sma and prev_short_sma <= prev_long_sma:
        return 1
    # Sell signal: Short SMA crosses below long SMA
    elif short_sma < long_sma and prev_short_sma >= prev_long_sma:
        return -1
    
    return 0

def rsi_strategy(df, current_index, period=14, oversold=30, overbought=70):
    """RSI-based strategy"""
    if current_index < period:
        return 0
    
    # Calculate RSI
    closes = df['close'].iloc[current_index-period:current_index]
    delta = closes.diff()
    gain = (delta.where(delta > 0, 0)).mean()
    loss = (-delta.where(delta < 0, 0)).mean()
    
    if loss == 0:
        return 0
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Signals
    if rsi < oversold:
        return 1  # Buy (oversold)
    elif rsi > overbought:
        return -1  # Sell (overbought)
    
    return 0

if __name__ == "__main__":
    # Usage example
    data_path = os.path.join("..", "..", "data", "processed")
    csv_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]
    
    if csv_files:
        file_path = os.path.join(data_path, csv_files[0])
        df = pd.read_csv(file_path)
        df['open_time'] = pd.to_datetime(df['open_time'])
        
        # Run backtest
        engine = BacktestEngine(initial_balance=10000)
        engine.run_backtest(df, sma_crossover_strategy)
        engine.print_summary()
    else:
        print("❌ No files found in processed folder")