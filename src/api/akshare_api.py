# src/api/akshare_api.py
import akshare as ak
import yfinance as yf
import pandas as pd
import numpy as np

def get_stock_news(symbol: str):
    try:
        df = ak.stock_news_em(symbol=symbol)
        if not df.empty:
            news_list = df.head(3)['content'].tolist()
            return "Recent News: " + "; ".join(news_list)
        return "No recent news."
    except Exception as e:
        return f"News error: {str(e)}"

def get_macro_economic():
    try:
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

# --- REMOVED calculate_rsi and analyze_technicals ---
# These have been moved to src/tools/technical_tools.py