# src/api/tushare_api.py
import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='api_keys.env')

TS_TOKEN = os.getenv("TUSHARE_TOKEN")
pro = ts.pro_api(TS_TOKEN) if TS_TOKEN else None

def get_stock_daily(ts_code: str, start_date: str = None, end_date: str = None):
    if not pro:
        return "Tushare token missing."
    try:
        end_date = end_date or datetime.now().strftime('%Y%m%d')
        start_date = start_date or (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        if df is not None and not df.empty:
            latest = df.sort_values('trade_date').iloc[-1]
            return f"Latest: {latest['trade_date']} Close={latest['close']} ({latest['pct_chg']}%)"
        return "No data found."
    except Exception as e:
        return str(e)

def get_stock_financials(ts_code: str):
    if not pro:
        return "Tushare token missing."
    try:
        df = pro.daily_basic(ts_code=ts_code, trade_date=datetime.now().strftime('%Y%m%d'))
        if df is not None and not df.empty:
            row = df.iloc[-1]
            return f"PE: {row['pe_ttm']}, PB: {row['pb']}"
        return "Financials unavailable."
    except Exception as e:
        return str(e)

def get_income_statement(ts_code: str):
    if not pro:
        return "Tushare token missing."
    try:
        df = pro.income(ts_code=ts_code, start_date='20230101', fields='ann_date,total_revenue,net_profit')
        if df is not None and not df.empty:
            latest = df.iloc[-1]
            return f"Revenue: {latest['total_revenue']}, Profit: {latest['net_profit']} (Report: {latest['ann_date']})"
        return "Income statement unavailable."
    except Exception as e:
        return str(e)

# --- New: Historical Data for Charts ---
def get_stock_history(ts_code: str, days: int = 20):
    if not pro:
        return "Error: Tushare token missing."
    try:
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days * 2)).strftime('%Y%m%d')
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        
        if df is None or df.empty:
            return f"No data for {ts_code} in last {days} days."

        df = df.sort_values('trade_date', ascending=True).tail(days)
        df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
        return df[['trade_date', 'open', 'high', 'low', 'close', 'vol']].to_json(orient='records')
        
    except Exception as e:
        return f"Data Error: {str(e)}"

def get_fund_history(fund_code: str, days: int = 20):
    if not pro:
        return "Error: Tushare token missing."
    try:
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days * 2)).strftime('%Y%m%d')
        
        df = pro.fund_daily(ts_code=fund_code, start_date=start_date, end_date=end_date)
        if df.empty:
            df = pro.fund_nav(ts_code=fund_code, start_date=start_date, end_date=end_date)
            
        if not df.empty:
            date_col = 'trade_date' if 'trade_date' in df.columns else 'end_date'
            df[date_col] = pd.to_datetime(df[date_col], format='%Y%m%d', errors='ignore')
            return df[[date_col, 'close', 'nav_value']].tail(days).to_json(orient='records')
        return f"No history for fund {fund_code}"
        
    except Exception as e:
        return f"Fund Data Error: {str(e)}"