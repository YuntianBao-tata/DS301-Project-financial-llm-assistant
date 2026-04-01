import akshare as ak
import yfinance as yf
import pandas as pd
import numpy as np

def get_stock_news(symbol: str):
    try:
        # Akshare news interface
        df = ak.stock_news_em(symbol=symbol)
        if not df.empty:
            news_list = df.head(3)['content'].tolist()
            return "Recent News: " + "; ".join(news_list)
        return "No recent news."
    except Exception as e:
        return f"News error: {str(e)}"

def get_macro_economic():
    try:
        # Example: GDP or CPI data
        df = ak.macro_cn_gdp_year()
        if not df.empty:
            return f"Macro Data (GDP): {df.iloc[-1].to_dict()}"
        return "Macro data unavailable."
    except Exception as e:
        return str(e)

def get_global_index(symbol: str):
    """Use yfinance for global indices like ^GSPC, ^IXIC"""
    try:
        ticker = symbol
        data = yf.Ticker(ticker)
        hist = data.history(period="1d")
        if not hist.empty:
            return f"{symbol} Price: {hist['Close'].iloc[-1]}"
        return "Data not found."
    except Exception as e:
        return str(e)

def calculate_rsi(data, window=14):
    """Manual RSI calculation using Pandas to avoid pandas_ta dependency"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def analyze_technicals(symbol: str):
    """Calculate RSI using Tushare data and manual Pandas logic"""
    import tushare as ts
    from datetime import datetime, timedelta
    import os
    from dotenv import load_dotenv
    
    load_dotenv(dotenv_path='api_keys.env')
    TS_TOKEN = os.getenv("TUSHARE_TOKEN")
    
    if not TS_TOKEN: return "Tushare token missing."
    
    try:
        pro = ts.pro_api()
        # Fetch last 60 days of data for RSI calculation
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=100)).strftime('%Y%m%d')
        
        # Fetch data
        df = pro.daily(ts_code=symbol, start_date=start_date, end_date=end_date)
        
        if df is not None and not df.empty:
            # Calculate RSI
            df = df.sort_values('trade_date')
            rsi_value = calculate_rsi(df['close'], window=14)
            
            signal = "Neutral"
            if rsi_value > 70: signal = "Overbought (Sell Signal)"
            elif rsi_value < 30: signal = "Oversold (Buy Signal)"
            
            return f"Technical Analysis for {symbol}: RSI(14) is {rsi_value:.2f}, indicating {signal}."
        
        return "Data insufficient for technical analysis."
    except Exception as e:
        return str(e)