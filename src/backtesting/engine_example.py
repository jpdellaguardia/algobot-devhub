import pandas as pd
import os
from backtest_engine import BacktestEngine, sma_crossover_strategy

def simple_example():
    """Simple example of how to use the backtesting engine"""
    
    # Load processed data
    data_path = os.path.join("..", "..", "data", "processed")
    csv_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ No files found. Run get_datas.py and preprocess.py first")
        return
    
    # Use first available file
    file_path = os.path.join(data_path, csv_files[0])
    df = pd.read_csv(file_path)
    df['open_time'] = pd.to_datetime(df['open_time'])
    
    print(f"📊 Testing with {csv_files[0]} ({len(df)} candles)")
    
    # Create backtest engine
    engine = BacktestEngine(
        initial_balance=10000,  # $10,000 initial
        commission=0.001        # 0.1% commission
    )
    
    # Run backtest with moving average strategy
    engine.run_backtest(df, sma_crossover_strategy)
    
    # Show results
    engine.print_summary()
    
    # Show some trades
    print("\n🔍 Last 5 trades:")
    for trade in engine.trades[-5:]:
        print(f"{trade['type']} - {trade['timestamp']} - ${trade['price']:.2f}")

def educational_example():
    """Educational example showing trading concepts"""
    print("📚 BACKTESTING CONCEPTS")
    print("=" * 40)
    print("\n🎯 What is Backtesting?")
    print("- Testing strategies with historical data")
    print("- Simulates past buy and sell decisions")
    print("- Evaluates performance without real risk")
    
    print("\n💡 Main components:")
    print("- Initial balance: Capital to invest")
    print("- Position: Amount of assets in portfolio")
    print("- Signals: When to buy (1) or sell (-1)")
    print("- Commissions: Brokerage fees")
    
    print("\n📈 Important metrics:")
    print("- Win Rate: % of profitable trades")
    print("- Total return: Final profit/loss")
    print("- Drawdown: Largest consecutive loss")
    
    print("\n⚠️ Limitations:")
    print("- Past data ≠ future results")
    print("- Doesn't consider real slippage")
    print("- May have overfitting issues")

if __name__ == "__main__":
    educational_example()
    print("\n" + "="*50)
    simple_example()
