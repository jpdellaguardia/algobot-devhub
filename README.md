# 🤖 Algorithmic Trading Bot System

**A prototype Python based system thats for developing, testing, and analyzing quantitative trading strategies using **Binance API** integration. Built with modular architecture and advanced analytics capabilities.

---

## 🎯 Key Features

### 📊 **Data Management**
- **Historical data collection** from Binance API
- **Automated preprocessing** with data cleaning
- **Multiple timeframes** support (1m, 5m, 15m, 1h, 1d)
- **Flexible symbol selection** for any trading pair




### 🔬 **Backtesting**
- **Backtesting.py lib** 
- **Position management** and risk controls
- **Multiple order types** (Market orders)
- **Equity curve tracking** and trade logging

### 📈 **Advanced Analytics**
- **Risk-adjusted metrics**: Sharpe Ratio, Sortino Ratio
- **Drawdown analysis** with visualization
- **Performance heatmaps** by month/week
- **Period-based performance** breakdown
- **Professional reporting** with charts

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|----------|
| **Core Engine** | Python 3.8+ | Main backtesting logic |
| **Data Source** | Binance API | Historical market data |
| **Analytics** | Pandas, Pandas TA | NumPy | Backtesting.py |
| **Visualization** | To be determined |
| **Storage** | CSV Files | Data persistence |
| **Architecture** | Modular Design | Scalable and maintainable |

---

## 🚀 Quick Start

### 1. **Setup Environment**
```bash
# Clone repository
git clone https://github.com/jpdellaguardia/algobot-devhub.git
cd algobot-devhub-main

# Install basic dependencies
pip install pandas numpy python-binance

# Install analytics dependencies (optional)
pip install -r requirements_analytics.txt
```

### 2. **Collect Data**
```bash
cd src/data_fetch
python get_datas.py
# Follow interactive prompts to select:
# - Time interval (1m, 5m, 1h, etc.)
# - Number of days
# - Trading symbols (BTCUSDT, ETHUSDT, etc.)
```

### 3. **Process Data**
```bash
python preprocess.py
# Automatically cleans data and removes duplicates
```

### 4. **Run Backtest**
```bash
cd ../backtesting
python run_backtest.py


---

## 📁 Project Structure

```
algobot-devhub-main/
├── src/
│   ├── data_fetch/
│   │   ├── get_datas.py          # Interactive data collection
│   │   └── preprocess.py         # Data cleaning and validation
│   └── backtesting/
│       ├─
│       └── strategies/
│           ├── rulebased.py      # Multi-rule strategies
│           ├── macd_strategy.py  # MACD-based strategies
│           ├── rsi_strategy.py   # RSI-based strategies
│           ├── bollinger_strategy.py # Bollinger Bands strategies
│           └── breakout_strategy.py  # Breakout strategies
├── data/
│   ├── raw/                      # Raw market data
│   ├── processed/                # Cleaned data
│   ├── backtest_reports/         # Basic backtest results
│   └── advanced_reports/         # Advanced analytics reports
└── requirements_analytics.txt    # Analytics dependencies
```

---

## 🎯 Available Strategies

### **Technical Indicators**
1. **Moving Average Crossover** - SMA trend following
2. **Basic RSI** - Overbought/oversold signals
3. **MACD Crossover** - Momentum-based signals
4. **MACD Histogram** - Histogram divergence
5. **Bollinger Bands** - Mean reversion at bands
6. **Bollinger Squeeze** - Low volatility breakouts

### **Advanced Strategies**
7. **RSI Divergence** - Price vs RSI divergence detection
8. **RSI Mean Reversion** - Extreme RSI levels
9. **Bollinger Mean Reversion** - Band-to-center reversals
10. **Bollinger Trend** - Trend confirmation with bands

### **Breakout Systems**
11. **Support/Resistance Breakout** - Key level breaks
12. **Volume Breakout** - Volume-confirmed breakouts
13. **Range Breakout** - Consolidation breakouts
14. **Pivot Points Breakout** - Technical pivot levels
15. **Donchian Channel** - Classic breakout system
16. **False Breakout Filter** - Anti-whipsaw protection

### **Rule-Based Systems**
17. **Multi-Rule Strategy** - Combined indicator signals
18. **Advanced Rule-Based** - Complex multi-factor model
19. **Conservative Rule-Based** - High-confidence signals only

---

## 📊 Analytics & Reporting

### **Risk Metrics**
- **Sharpe Ratio**: Risk-adjusted returns (>1.0 good, >2.0 excellent)
- **Sortino Ratio**: Downside risk-adjusted returns
- **Maximum Drawdown**: Worst peak-to-trough decline
- **Drawdown Duration**: Recovery time analysis

### **Performance Analysis**
- **Monthly/Weekly Returns**: Period-based breakdown
- **Win Rate**: Percentage of profitable periods
- **Best/Worst Periods**: Performance extremes
- **Volatility Metrics**: Return consistency measures

### **Visualizations**
- **Performance Heatmaps**: Monthly return calendar
- **Drawdown Charts**: Visual drawdown analysis
- **Equity Curves**: Portfolio value over time
- **Trade Distribution**: Win/loss analysis

---

## 🔧 Usage Examples

### **Basic Backtesting**
```python
from backtest_engine import BacktestEngine, sma_crossover_strategy
import pandas as pd

# Load data
df = pd.read_csv('data/processed/BTCUSDT_1h_30d.csv')
df['open_time'] = pd.to_datetime(df['open_time'])

# Create engine
engine = BacktestEngine(initial_balance=10000, commission=0.001)

# Run backtest
engine.run_backtest(df, sma_crossover_strategy)
engine.print_summary()
```

### **Advanced Analytics**
```python
from advanced_analytics import AdvancedAnalytics

# Create analytics instance
analytics = AdvancedAnalytics(engine, df)

# Calculate metrics
sharpe = analytics.calculate_sharpe_ratio()
sortino = analytics.calculate_sortino_ratio()

# Generate reports
analytics.generate_advanced_report('report.txt')
analytics.create_performance_heatmap('heatmap.png')
```

---

## 📈 Performance Metrics Explained

| Metric | Good Value | Interpretation |
|--------|------------|----------------|
| **Sharpe Ratio** | > 1.0 | Risk-adjusted return efficiency |
| **Sortino Ratio** | > 1.5 | Downside risk-adjusted returns |
| **Max Drawdown** | < 20% | Maximum portfolio decline |
| **Win Rate** | > 50% | Percentage of winning trades |
| **Profit Factor** | > 1.5 | Gross profit / Gross loss |

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### **Adding New Strategies**
1. Create strategy function in `src/backtesting/strategies/`
2. Follow the signature: `strategy_func(df, current_index) -> int`
3. Return: `1` (buy), `-1` (sell), `0` (hold)
4. Add to strategy menu in `run_backtest.py`

### **Improving Analytics**
1. Extend `AdvancedAnalytics` class
2. Add new metrics or visualizations
3. Update documentation

### **Bug Reports & Features**
1. Open GitHub issues with detailed descriptions
2. Include code examples and error messages
3. Suggest improvements or new features

---

## ⚠️ Disclaimer

**This software is for educational and research purposes only.**

- Past performance does not guarantee future results
- Backtesting may not reflect real market conditions
- Always test strategies with paper trading first
- Consider slippage, latency, and market impact
- Cryptocurrency trading involves significant risk

---

## 📄 License

This project is open source. Please check the LICENSE file for details.

---

## 🆘 Support

- **Documentation**: Check example files in `src/backtesting/`
- **Issues**: Report bugs via GitHub issues
- **Discussions**: Use GitHub discussions for questions
- **Examples**: Run `python engine_example.py` for tutorials

---

**Built with ❤️ for  the algorithmic trading community**
