import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='api_keys.env')

# Initialize Tushare
TS_TOKEN = os.getenv("TUSHARE_TOKEN")
if TS_TOKEN:
    ts.set_token(TS_TOKEN)
    pro = ts.pro_api()
else:
    pro = None

def get_stock_daily(ts_code: str, start_date: str = None, end_date: str = None):
    if not pro: return "Tushare token missing."
    
    # Dynamic Date Logic: Default to last 1 year if not provided
    if not end_date:
        end_date = datetime.now().strftime('%Y%m%d')
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
        
    try:
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        if df is not None and not df.empty:
            # Sort by date ascending
            df = df.sort_values('trade_date')
            # Get the latest row for summary
            latest = df.iloc[-1]
            return f"Latest data for {ts_code} on {latest['trade_date']}: Close={latest['close']}, Change={latest['pct_chg']}%"
        return "No data found."
    except Exception as e:
        return str(e)

def get_stock_financials(ts_code: str):
    if not pro: return "Tushare token missing."
    try:
        # Get Valuation Metrics (PE, PB, Total Market Cap)
        df = pro.daily_basic(ts_code=ts_code, start_date=(datetime.now() - timedelta(days=1)).strftime('%Y%m%d'), end_date=datetime.now().strftime('%Y%m%d'))
        if df is not None and not df.empty:
            row = df.iloc[-1]
            return f"PE(TTM): {row['pe_ttm']}, PB: {row['pb']}, Total Shareholder Equity: {row['total_shareholder_equity']}"
        return "Financial data unavailable."
    except Exception as e:
        return str(e)

def get_fund_nav(ts_code: str):
    """Get Net Asset Value for ETF or Mutual Funds"""
    if not pro: return "Tushare token missing."
    try:
        # Try ETF first
        df = pro.fund_daily(ts_code=ts_code, start_date=(datetime.now() - timedelta(days=30)).strftime('%Y%m%d'), end_date=datetime.now().strftime('%Y%m%d'))
        if df is not None and not df.empty:
            latest = df.iloc[-1]
            return f"Fund {ts_code} latest NAV: {latest['close']} on {latest['trade_date']}"
        
        # Fallback to general fund NAV
        df = pro.fund_nav(ts_code=ts_code, start_date=(datetime.now() - timedelta(days=30)).strftime('%Y%m%d'), end_date=datetime.now().strftime('%Y%m%d'))
        if df is not None and not df.empty:
             latest = df.iloc[-1]
             return f"Fund {ts_code} NAV: {latest['nav']} on {latest['end_date']}"
             
        return "Fund data unavailable."
    except Exception as e:
        return str(e)

def get_income_statement(ts_code: str):
    if not pro: return "Tushare token missing."
    try:
        df = pro.income(ts_code=ts_code, start_date='20230101', end_date=datetime.now().strftime('%Y%m%d'), fields='ts_code,ann_date,total_revenue,net_profit')
        if df is not None and not df.empty:
            # Get the most recent annual report
            latest = df.iloc[-1]
            return f"Revenue: {latest['total_revenue']}, Net Profit: {latest['net_profit']} (Announced: {latest['ann_date']})"
        return "Income statement unavailable."
    except Exception as e:
        return str(e)