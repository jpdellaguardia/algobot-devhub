import pandas as pd
import os
from backtest_engine import BacktestEngine, sma_crossover_strategy
from advanced_analytics import AdvancedAnalytics

def demo_advanced_analytics():
    """Demonstrates advanced analytics features"""
    print("📊 ADVANCED ANALYTICS DEMO")
    print("=" * 40)
    
    # Load sample data
    data_path = os.path.join("..", "..", "data", "processed")
    csv_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ No processed data found. Run get_datas.py and preprocess.py first")
        return
    
    # Use first available file
    file_path = os.path.join(data_path, csv_files[0])
    df = pd.read_csv(file_path)
    df['open_time'] = pd.to_datetime(df['open_time'])
    
    print(f"📈 Using data: {csv_files[0]} ({len(df)} candles)")
    
    # Run backtest
    engine = BacktestEngine(initial_balance=10000, commission=0.001)
    engine.run_backtest(df, sma_crossover_strategy)
    
    # Create analytics instance
    analytics = AdvancedAnalytics(engine, df)
    
    print("\n🎯 RISK METRICS:")
    print(f"Sharpe Ratio: {analytics.calculate_sharpe_ratio():.3f}")
    print(f"Sortino Ratio: {analytics.calculate_sortino_ratio():.3f}")
    
    max_dd, max_dd_pct, dd_start, dd_end = analytics.calculate_max_drawdown()
    print(f"Max Drawdown: {max_dd_pct:.2f}%")
    
    print("\n📅 PERIOD PERFORMANCE:")
    
    # Monthly performance
    monthly_perf = analytics.performance_by_period('M')
    if not monthly_perf.empty:
        print(f"Best Month: {monthly_perf['return_pct'].max():.2f}%")
        print(f"Worst Month: {monthly_perf['return_pct'].min():.2f}%")
        print(f"Monthly Win Rate: {(monthly_perf['return_pct'] > 0).mean() * 100:.1f}%")
    
    # Weekly performance
    weekly_perf = analytics.performance_by_period('W')
    if not weekly_perf.empty:
        print(f"Best Week: {weekly_perf['return_pct'].max():.2f}%")
        print(f"Worst Week: {weekly_perf['return_pct'].min():.2f}%")
        print(f"Weekly Win Rate: {(weekly_perf['return_pct'] > 0).mean() * 100:.1f}%")
    
    print("\n📉 DRAWDOWN ANALYSIS:")
    dd_analysis = analytics.drawdown_analysis()
    if not dd_analysis.empty:
        print(f"Number of Drawdown Periods: {len(dd_analysis)}")
        print(f"Average Duration: {dd_analysis['duration_days'].mean():.1f} days")
        print(f"Longest Drawdown: {dd_analysis['duration_days'].max()} days")
    
    # Generate full report
    print("\n📋 GENERATING COMPREHENSIVE REPORT...")
    analytics.generate_advanced_report()
    
    print("\n✅ Demo completed! Run with save_path parameter to save charts and reports.")

def explain_metrics():
    """Explains what each metric means"""
    print("📚 METRICS EXPLANATION")
    print("=" * 40)
    
    print("\n🎯 SHARPE RATIO:")
    print("   - Measures risk-adjusted returns")
    print("   - Higher is better (>1.0 is good, >2.0 is excellent)")
    print("   - Formula: (Return - Risk-free rate) / Standard deviation")
    
    print("\n🎯 SORTINO RATIO:")
    print("   - Like Sharpe but only considers downside risk")
    print("   - Better for strategies with asymmetric returns")
    print("   - Higher is better")
    
    print("\n📉 MAX DRAWDOWN:")
    print("   - Largest peak-to-trough decline")
    print("   - Shows worst-case scenario")
    print("   - Lower is better (closer to 0%)")
    
    print("\n📅 PERIOD PERFORMANCE:")
    print("   - Monthly/Weekly returns breakdown")
    print("   - Shows consistency and seasonality")
    print("   - Win rate = % of profitable periods")
    
    print("\n🔥 HEATMAPS:")
    print("   - Visual representation of monthly returns")
    print("   - Green = profits, Red = losses")
    print("   - Helps identify seasonal patterns")

if __name__ == "__main__":
    explain_metrics()
    print("\n" + "="*50)
    demo_advanced_analytics()