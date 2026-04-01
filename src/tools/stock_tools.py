from langchain_core.tools import tool
from src.api.tushare_api import get_stock_daily, get_stock_info
from src.api.akshare_api import get_stock_news, get_macro_economic

@tool
def query_stock_price(ts_code: str, start_date: str, end_date: str) -> str:
    """Query historical stock price data. Input: ts_code (e.g. '600519.SH'), start_date (YYYYMMDD), end_date (YYYYMMDD)."""
    return get_stock_daily(ts_code, start_date, end_date)

@tool
def query_stock_profile(ts_code: str) -> str:
    """Query basic stock profile. Input: ts_code (e.g. '600519.SH')."""
    return get_stock_info(ts_code)

@tool
def query_market_news(symbol: str) -> str:
    """Query latest stock news. Input: stock symbol (e.g. '600519')."""
    return get_stock_news(symbol)

@tool
def query_macro_data() -> str:
    """Query recent macroeconomic data."""
    return get_macro_economic()