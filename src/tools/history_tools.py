# src/tools/history_tools.py
from langchain_core.tools import tool
import tushare as ts
import pandas as pd
import os
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
        
        # --- ROBUST FIX: Handle empty or None data ---
        if df is None or df.empty:
            return f"No trading data found for {ts_code} between {start_date} and {end_date}. The date range might be invalid or the stock was not trading."
        
        # Sort by date ascending and reset index for safe iloc access
        df = df.sort_values('trade_date').reset_index(drop=True)
        
        # --- ROBUST FIX: Ensure we have enough data points ---
        if len(df) < 2:
            return f"Insufficient data for {ts_code} in the given period (only {len(df)} record found). Cannot calculate performance."

        # Calculate performance metrics
        start_price = df['close'].iloc[0]
        end_price = df['close'].iloc[-1]
        
        if start_price == 0:
             return f"Invalid price data (Start price is 0) for {ts_code}."

        return_pct = ((end_price - start_price) / start_price) * 100
        
        # Volatility
        df['daily_return'] = df['close'].pct_change()
        valid_returns = df['daily_return'].dropna()
        volatility = valid_returns.std() * 100 if not valid_returns.empty else 0.0
        
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
        # ---  Catch any other unexpected errors ---
        return f"Historical Analysis Error for {ts_code}: {str(e)}"