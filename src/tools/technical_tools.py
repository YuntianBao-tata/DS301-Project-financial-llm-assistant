# src/tools/technical_tools.py
from langchain_core.tools import tool
import tushare as ts
import pandas as pd
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load env vars
load_dotenv(dotenv_path='api_keys.env')

@tool
def analyze_stock_technicals(ts_code: str) -> str:
    """
    Analyzes technical indicators for a stock, specifically RSI (Relative Strength Index).
    Use this to determine if a stock is Overbought or Oversold.
    Input: ts_code (e.g., '600519.SH')
    """
    TS_TOKEN = os.getenv("TUSHARE_TOKEN")
    if not TS_TOKEN:
        return "Error: Tushare token missing."

    try:
        pro = ts.pro_api(TS_TOKEN)
        
        # Fetch last 100 days of data to ensure we have enough for the 14-day RSI window
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=100)).strftime('%Y%m%d')
        
        # Get daily data
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        
        if df is None or df.empty:
            return f"No data found for {ts_code}."

        # Sort by date ascending for calculation
        df = df.sort_values('trade_date')
        
        # --- RSI Calculation Logic ---
        # 1. Calculate price difference
        delta = df['close'].diff()
        
        # 2. Separate gains and losses
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        
        # 3. Calculate RS and RSI
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Get the latest RSI value
        current_rsi = rsi.iloc[-1]
        
        # Interpret the signal
        signal = "Neutral"
        if current_rsi > 70:
            signal = "Overbought (Potential Sell Signal)"
        elif current_rsi < 30:
            signal = "Oversold (Potential Buy Signal)"
            
        return f"Technical Analysis for {ts_code}: Current RSI(14) is {current_rsi:.2f}, indicating the stock is {signal}."

    except Exception as e:
        return f"Technical Analysis Error: {str(e)}"