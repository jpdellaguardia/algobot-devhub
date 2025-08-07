import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

class AdvancedAnalytics:
    def __init__(self, engine, df):
        self.engine = engine
        self.df = df
        self.equity_df = pd.DataFrame(engine.equity_curve)
        self.trades_df = pd.DataFrame(engine.trades)
        
        if not self.equity_df.empty:
            self.equity_df['timestamp'] = pd.to_datetime(self.equity_df['timestamp'])
            self.equity_df['returns'] = self.equity_df['portfolio_value'].pct_change()
    
    def calculate_sharpe_ratio(self, risk_free_rate=0.02):
        """Calculate Sharpe Ratio"""
        if self.equity_df.empty or len(self.equity_df) < 2:
            return 0
        
        returns = self.equity_df['returns'].dropna()
        if len(returns) == 0:
            return 0
        
        excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
        if excess_returns.std() == 0:
            return 0
        
        return excess_returns.mean() / excess_returns.std() * np.sqrt(252)
    
    def calculate_sortino_ratio(self, risk_free_rate=0.02):
        """Calculate Sortino Ratio"""
        if self.equity_df.empty or len(self.equity_df) < 2:
            return 0
        
        returns = self.equity_df['returns'].dropna()
        if len(returns) == 0:
            return 0
        
        excess_returns = returns - (risk_free_rate / 252)
        downside_returns = excess_returns[excess_returns < 0]
        
        if len(downside_returns) == 0 or downside_returns.std() == 0:
            return 0
        
        return excess_returns.mean() / downside_returns.std() * np.sqrt(252)
    
    def calculate_max_drawdown(self):
        """Calculate maximum drawdown"""
        if self.equity_df.empty:
            return 0, 0, None, None
        
        portfolio_values = self.equity_df['portfolio_value']
        peak = portfolio_values.expanding().max()
        drawdown = (portfolio_values - peak) / peak
        
        max_dd = drawdown.min()
        max_dd_pct = max_dd * 100
        
        # Find drawdown period
        max_dd_idx = drawdown.idxmin()
        peak_idx = peak[:max_dd_idx].idxmax()
        
        start_date = self.equity_df.loc[peak_idx, 'timestamp'] if peak_idx in self.equity_df.index else None
        end_date = self.equity_df.loc[max_dd_idx, 'timestamp'] if max_dd_idx in self.equity_df.index else None
        
        return max_dd, max_dd_pct, start_date, end_date
    
    def performance_by_period(self, period='M'):
        """Calculate performance by month/week"""
        if self.equity_df.empty:
            return pd.DataFrame()
        
        df_period = self.equity_df.set_index('timestamp')
        df_period['period'] = df_period.index.to_period(period)
        
        period_performance = df_period.groupby('period').agg({
            'portfolio_value': ['first', 'last'],
            'returns': ['sum', 'std', 'count']
        }).round(4)
        
        period_performance.columns = ['start_value', 'end_value', 'total_return', 'volatility', 'periods']
        period_performance['return_pct'] = ((period_performance['end_value'] - period_performance['start_value']) / period_performance['start_value'] * 100).round(2)
        
        return period_performance
    
    def create_performance_heatmap(self, save_path=None):
        """Create performance heatmap"""
        if self.equity_df.empty:
            print("❌ No data for heatmap")
            return
        
        # Monthly performance
        monthly_perf = self.performance_by_period('M')
        if monthly_perf.empty:
            print("❌ Insufficient data for heatmap")
            return
        
        # Create pivot table for heatmap
        monthly_perf.reset_index(inplace=True)
        monthly_perf['year'] = monthly_perf['period'].dt.year
        monthly_perf['month'] = monthly_perf['period'].dt.month
        
        pivot_table = monthly_perf.pivot(index='year', columns='month', values='return_pct')
        
        # Create heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table, annot=True, fmt='.1f', cmap='RdYlGn', center=0,
                   cbar_kws={'label': 'Return %'})
        plt.title('Monthly Performance Heatmap')
        plt.xlabel('Month')
        plt.ylabel('Year')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Heatmap saved to: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def drawdown_analysis(self):
        """Analyze drawdown periods"""
        if self.equity_df.empty:
            return pd.DataFrame()
        
        portfolio_values = self.equity_df['portfolio_value']
        peak = portfolio_values.expanding().max()
        drawdown = (portfolio_values - peak) / peak * 100
        
        # Find drawdown periods
        in_drawdown = drawdown < -0.1  # More than 0.1% drawdown
        drawdown_periods = []
        
        start_idx = None
        for i, is_dd in enumerate(in_drawdown):
            if is_dd and start_idx is None:
                start_idx = i
            elif not is_dd and start_idx is not None:
                end_idx = i - 1
                period_dd = drawdown.iloc[start_idx:end_idx+1]
                max_dd = period_dd.min()
                
                drawdown_periods.append({
                    'start_date': self.equity_df.iloc[start_idx]['timestamp'],
                    'end_date': self.equity_df.iloc[end_idx]['timestamp'],
                    'duration_days': (self.equity_df.iloc[end_idx]['timestamp'] - self.equity_df.iloc[start_idx]['timestamp']).days,
                    'max_drawdown_pct': max_dd,
                    'recovery_date': self.equity_df.iloc[end_idx]['timestamp']
                })
                start_idx = None
        
        return pd.DataFrame(drawdown_periods)
    
    def generate_advanced_report(self, save_path=None):
        """Generate comprehensive analytics report"""
        report = []
        report.append("=" * 60)
        report.append("📊 ADVANCED PERFORMANCE ANALYTICS")
        report.append("=" * 60)
        
        # Risk-adjusted metrics
        sharpe = self.calculate_sharpe_ratio()
        sortino = self.calculate_sortino_ratio()
        max_dd, max_dd_pct, dd_start, dd_end = self.calculate_max_drawdown()
        
        report.append(f"\n🎯 Risk-Adjusted Metrics:")
        report.append(f"   Sharpe Ratio: {sharpe:.3f}")
        report.append(f"   Sortino Ratio: {sortino:.3f}")
        report.append(f"   Max Drawdown: {max_dd_pct:.2f}%")
        if dd_start and dd_end:
            report.append(f"   Drawdown Period: {dd_start.date()} to {dd_end.date()}")
        
        # Monthly performance
        monthly_perf = self.performance_by_period('M')
        if not monthly_perf.empty:
            report.append(f"\n📅 Monthly Performance Summary:")
            report.append(f"   Best Month: {monthly_perf['return_pct'].max():.2f}%")
            report.append(f"   Worst Month: {monthly_perf['return_pct'].min():.2f}%")
            report.append(f"   Avg Monthly Return: {monthly_perf['return_pct'].mean():.2f}%")
            report.append(f"   Monthly Win Rate: {(monthly_perf['return_pct'] > 0).mean() * 100:.1f}%")
        
        # Weekly performance
        weekly_perf = self.performance_by_period('W')
        if not weekly_perf.empty:
            report.append(f"\n📊 Weekly Performance Summary:")
            report.append(f"   Best Week: {weekly_perf['return_pct'].max():.2f}%")
            report.append(f"   Worst Week: {weekly_perf['return_pct'].min():.2f}%")
            report.append(f"   Avg Weekly Return: {weekly_perf['return_pct'].mean():.2f}%")
            report.append(f"   Weekly Win Rate: {(weekly_perf['return_pct'] > 0).mean() * 100:.1f}%")
        
        # Drawdown analysis
        dd_analysis = self.drawdown_analysis()
        if not dd_analysis.empty:
            report.append(f"\n📉 Drawdown Analysis:")
            report.append(f"   Number of Drawdown Periods: {len(dd_analysis)}")
            report.append(f"   Average Drawdown Duration: {dd_analysis['duration_days'].mean():.1f} days")
            report.append(f"   Longest Drawdown: {dd_analysis['duration_days'].max()} days")
        
        report.append("=" * 60)
        
        report_text = "\n".join(report)
        print(report_text)
        
        if save_path:
            with open(save_path, 'w') as f:
                f.write(report_text)
            print(f"\n✅ Advanced report saved to: {save_path}")
        
        return report_text
    
    def create_drawdown_chart(self, save_path=None):
        """Create drawdown chart"""
        if self.equity_df.empty:
            print("❌ No data for drawdown chart")
            return
        
        portfolio_values = self.equity_df['portfolio_value']
        peak = portfolio_values.expanding().max()
        drawdown = (portfolio_values - peak) / peak * 100
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Portfolio value chart
        ax1.plot(self.equity_df['timestamp'], portfolio_values, label='Portfolio Value', color='blue')
        ax1.plot(self.equity_df['timestamp'], peak, label='Peak Value', color='red', alpha=0.7)
        ax1.set_title('Portfolio Value and Peaks')
        ax1.set_ylabel('Portfolio Value ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Drawdown chart
        ax2.fill_between(self.equity_df['timestamp'], drawdown, 0, alpha=0.3, color='red')
        ax2.plot(self.equity_df['timestamp'], drawdown, color='red')
        ax2.set_title('Drawdown Over Time')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Drawdown (%)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Drawdown chart saved to: {save_path}")
        else:
            plt.show()
        
        plt.close()

def run_advanced_analytics(engine, df, strategy_name):
    """Run all advanced analytics"""
    analytics = AdvancedAnalytics(engine, df)
    
    # Create reports directory
    reports_dir = os.path.join("..", "..", "data", "advanced_reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generate comprehensive report
    report_file = os.path.join(reports_dir, f"advanced_report_{strategy_name.replace(' ', '_')}.txt")
    analytics.generate_advanced_report(report_file)
    
    # Create visualizations
    heatmap_file = os.path.join(reports_dir, f"heatmap_{strategy_name.replace(' ', '_')}.png")
    analytics.create_performance_heatmap(heatmap_file)
    
    drawdown_file = os.path.join(reports_dir, f"drawdown_{strategy_name.replace(' ', '_')}.png")
    analytics.create_drawdown_chart(drawdown_file)
    
    # Save period performance data
    monthly_perf = analytics.performance_by_period('M')
    if not monthly_perf.empty:
        monthly_file = os.path.join(reports_dir, f"monthly_performance_{strategy_name.replace(' ', '_')}.csv")
        monthly_perf.to_csv(monthly_file)
        print(f"✅ Monthly performance saved to: {monthly_file}")
    
    weekly_perf = analytics.performance_by_period('W')
    if not weekly_perf.empty:
        weekly_file = os.path.join(reports_dir, f"weekly_performance_{strategy_name.replace(' ', '_')}.csv")
        weekly_perf.to_csv(weekly_file)
        print(f"✅ Weekly performance saved to: {weekly_file}")
    
    return analytics