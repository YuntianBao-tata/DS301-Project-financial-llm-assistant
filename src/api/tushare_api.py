import os
import tushare as ts
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='api_keys.env')

# Initialize Tushare
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")
if TUSHARE_TOKEN:
    ts.set_token(TUSHARE_TOKEN)
    pro = ts.pro_api()
else:
    print("Warning: TUSHARE_TOKEN not found in api_keys.env")

def get_stock_daily(ts_code: str, start_date: str, end_date: str):
    """
    Fetch daily stock market data.
    """
    try:
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        if df is not None and not df.empty:
            # Sort by date
            df = df.sort_values(by='trade_date')
            return df.to_string(index=False)
        return "No data found."
    except Exception as e:
        return f"Error fetching data: {str(e)}"

def get_stock_info(ts_code: str):
    """
    Fetch basic stock information.
    """
    try:
        df = pro.stock_basic(ts_code=ts_code, fields='ts_code,symbol,name,area,industry,list_date')
        if df is not None and not df.empty:
            return df.to_string(index=False)
        return "No info found."
    except Exception as e:
        return f"Error fetching info: {str(e)}"