import pandas as pd
import os
from glob import glob
from backtest_engine import BacktestEngine, sma_crossover_strategy, rsi_strategy
from strategies.rulebased import rulebased_strategy, advanced_rulebased_strategy, conservative_rulebased_strategy
from strategies.macd_strategy import macd_strategy, macd_histogram_strategy
from strategies.rsi_strategy import rsi_strategy as rsi_strat, rsi_divergence_strategy, rsi_mean_reversion_strategy
from strategies.bollinger_strategy import bollinger_bands_strategy, bollinger_squeeze_strategy, bollinger_mean_reversion_strategy, bollinger_trend_strategy
from strategies.breakout_strategy import support_resistance_breakout, volume_breakout_strategy, range_breakout_strategy, pivot_breakout_strategy, donchian_breakout_strategy, false_breakout_filter_strategy
from advanced_analytics import run_advanced_analytics

def select_data_file():
    """Allows user to select data file"""
    data_path = os.path.join("..", "..", "data", "processed")
    csv_files = glob(os.path.join(data_path, "*.csv"))
    
    if not csv_files:
        print("❌ No files found in processed folder")
        return None
    
    print("📁 Available files:")
    for i, file_path in enumerate(csv_files, 1):
        filename = os.path.basename(file_path)
        print(f"{i}. {filename}")
    
    while True:
        try:
            choice = int(input("\nChoose file (number): ")) - 1
            if 0 <= choice < len(csv_files):
                return csv_files[choice]
            print("❌ Invalid option")
        except ValueError:
            print("❌ Enter a valid number")

def select_strategy():
    """Allows user to select strategy"""
    strategies = {
        1: ("Moving Average Crossover", sma_crossover_strategy),
        2: ("Basic RSI", rsi_strategy),
        3: ("Rule-Based (Multiple Rules)", rulebased_strategy),
        4: ("Advanced Rule-Based", advanced_rulebased_strategy),
        5: ("Conservative Rule-Based", conservative_rulebased_strategy),
        6: ("MACD Crossover", macd_strategy),
        7: ("MACD Histogram", macd_histogram_strategy),
        8: ("RSI Divergence", rsi_divergence_strategy),
        9: ("RSI Mean Reversion", rsi_mean_reversion_strategy),
        10: ("Bollinger Bands", bollinger_bands_strategy),
        11: ("Bollinger Squeeze", bollinger_squeeze_strategy),
        12: ("Bollinger Mean Reversion", bollinger_mean_reversion_strategy),
        13: ("Bollinger Trend", bollinger_trend_strategy),
        14: ("Support/Resistance Breakout", support_resistance_breakout),
        15: ("Volume Breakout", volume_breakout_strategy),
        16: ("Range Breakout", range_breakout_strategy),
        17: ("Pivot Points Breakout", pivot_breakout_strategy),
        18: ("Donchian Channel Breakout", donchian_breakout_strategy),
        19: ("False Breakout Filter", false_breakout_filter_strategy)
    }
    
    print("\n📈 Available strategies:")
    for key, (name, _) in strategies.items():
        print(f"{key}. {name}")
    
    while True:
        try:
            choice = int(input("\nChoose strategy (number): "))
            if choice in strategies:
                return strategies[choice]
            print("❌ Invalid option")
        except ValueError:
            print("❌ Enter a valid number")

def main():
    print("🤖 BACKTESTING SYSTEM")
    print("=" * 40)
    
    # Select file
    file_path = select_data_file()
    if not file_path:
        return
    
    # Load data
    print(f"\n📊 Loading data from {os.path.basename(file_path)}...")
    df = pd.read_csv(file_path)
    df['open_time'] = pd.to_datetime(df['open_time'])
    print(f"✅ {len(df)} candles loaded")
    
    # Select strategy
    strategy_name, strategy_func = select_strategy()
    
    # Backtest settings
    print(f"\n⚙️ Settings:")
    initial_balance = float(input("Initial balance ($): ") or "10000")
    commission = float(input("Commission rate (0.001 = 0.1%): ") or "0.001")
    
    print(f"\n🚀 Running backtest with {strategy_name}...")
    print(f"📅 Period: {df['open_time'].iloc[0]} to {df['open_time'].iloc[-1]}")
    
    # Run backtest
    engine = BacktestEngine(initial_balance=initial_balance, commission=commission)
    engine.run_backtest(df, strategy_func)
    
    # Show results
    engine.print_summary()
    
    # Advanced analytics option
    run_advanced = input("\n📊 Run advanced analytics? (y/n): ").lower() == 'y'
    if run_advanced:
        print("\n🔍 Running advanced analytics...")
        try:
            analytics = run_advanced_analytics(engine, df, strategy_name)
            print("\n✅ Advanced analytics completed!")
        except ImportError:
            print("❌ Missing required packages. Install: pip install matplotlib seaborn")
        except Exception as e:
            print(f"❌ Error in advanced analytics: {e}")
    
    # Save basic report
    save_report = input("\n💾 Save basic reports? (y/n): ").lower() == 'y'
    if save_report:
        report_path = os.path.join("..", "..", "data", "backtest_reports")
        os.makedirs(report_path, exist_ok=True)
        
        # Save trades
        trades_df = pd.DataFrame(engine.trades)
        trades_file = os.path.join(report_path, f"trades_{strategy_name.replace(' ', '_')}.csv")
        trades_df.to_csv(trades_file, index=False)
        
        # Save equity curve
        equity_df = pd.DataFrame(engine.equity_curve)
        equity_file = os.path.join(report_path, f"equity_{strategy_name.replace(' ', '_')}.csv")
        equity_df.to_csv(equity_file, index=False)
        
        print(f"✅ Basic reports saved to: {report_path}")

if __name__ == "__main__":
    main()