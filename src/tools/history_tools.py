# src/tools/history_tools.py
from langchain_core.tools import tool
import tushare as ts
import pandas as pd
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(dotenv_path='api_keys.env')

@tool
def analyze_historical_performance(ts_code: str, start_date: str, end_date: str) -> str:
    """
    Analyze stock performance over a specific historical period.
    Input: 
        - ts_code (e.g., '600519.SH')
        - start_date (format: 'YYYYMMDD' or 'YYYY-MM-DD')
        - end_date (format: 'YYYYMMDD' or 'YYYY-MM-DD')
    Returns: Performance summary including return %, volatility, and key stats.
    """
    TS_TOKEN = os.getenv("TUSHARE_TOKEN")
    if not TS_TOKEN:
        return "Error: Tushare token missing."

    try:
        pro = ts.pro_api(TS_TOKEN)
        
        # Fetch historical data for the specified period
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        
        if df is None or df.empty:
            return f"No data found for {ts_code} in the given period."
        
        # Sort by date ascending
        df = df.sort_values('trade_date')
        
        # Calculate performance metrics
        start_price = df['close'].iloc[0]
        end_price = df['close'].iloc[-1]
        return_pct = ((end_price - start_price) / start_price) * 100
        
        # Volatility (standard deviation of daily returns)
        df['daily_return'] = df['close'].pct_change()
        volatility = df['daily_return'].std() * 100
        
        # Max drawdown
        df['cum_max'] = df['close'].cummax()
        df['drawdown'] = (df['close'] - df['cum_max']) / df['cum_max'] * 100
        max_drawdown = df['drawdown'].min()
        
        result = (
            f"Historical Analysis for {ts_code} ({start_date} to {end_date}):\n"
            f"- Start Price: ¥{start_price:.2f}\n"
            f"- End Price: ¥{end_price:.2f}\n"
            f"- Total Return: {return_pct:+.2f}%\n"
            f"- Volatility: {volatility:.2f}%\n"
            f"- Max Drawdown: {max_drawdown:.2f}%"
        )
        
        return result

    except Exception as e:
        return f"Historical Analysis Error: {str(e)}"