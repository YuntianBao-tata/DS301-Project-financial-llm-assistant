# src/tools/stock_tools.py
from langchain_core.tools import tool
from src.api.tushare_api import (
    get_stock_daily, get_stock_financials, 
    get_income_statement, get_stock_history, get_fund_history
)

@tool
def query_stock_price(ts_code: str) -> str:
    """Fetch the latest stock price and daily change."""
    return get_stock_daily(ts_code)

@tool
def query_stock_valuation(ts_code: str) -> str:
    """Fetch stock valuation metrics like PE and PB."""
    return get_stock_financials(ts_code)

@tool
def query_company_income(ts_code: str) -> str:
    """Fetch the latest company income statement (Revenue/Profit)."""
    return get_income_statement(ts_code)

@tool
def fetch_stock_history_data(ts_code: str, days: int = 20) -> str:
    """Fetch historical stock price data for charting trends over a specific period."""
    return get_stock_history(ts_code, days)

@tool
def fetch_fund_history_data(fund_code: str, days: int = 20) -> str:
    """Fetch historical fund NAV data for charting trends over a specific period."""
    return get_fund_history(fund_code, days)