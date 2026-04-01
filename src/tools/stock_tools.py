from langchain_core.tools import tool
from src.api.tushare_api import get_stock_daily, get_stock_financials, get_fund_nav, get_income_statement
from src.api.akshare_api import get_stock_news, get_macro_economic, get_global_index, analyze_technicals

@tool
def query_stock_price(ts_code: str) -> str:
    """Query latest stock price. Input: ts_code (e.g. '600519.SH')."""
    return get_stock_daily(ts_code)

@tool
def query_stock_valuation(ts_code: str) -> str:
    """Query valuation metrics (PE, PB). Input: ts_code (e.g. '600519.SH')."""
    return get_stock_financials(ts_code)

@tool
def query_company_income(ts_code: str) -> str:
    """Query company revenue and profit. Input: ts_code (e.g. '600519.SH')."""
    return get_income_statement(ts_code)

@tool
def query_fund_data(ts_code: str) -> str:
    """Query Fund/ETF Net Asset Value. Input: ts_code (e.g. '510300.SH')."""
    return get_fund_nav(ts_code)

@tool
def query_market_news(symbol: str) -> str:
    """Query latest stock news. Input: stock symbol (e.g. '600519')."""
    return get_stock_news(symbol)

@tool
def query_global_market(symbol: str) -> str:
    """Query global market indices (e.g. ^GSPC, ^IXIC)."""
    return get_global_index(symbol)

@tool
def query_technical_analysis(ts_code: str) -> str:
    """Query technical indicators like RSI. Input: ts_code (e.g. '600519.SH')."""
    return analyze_technicals(ts_code)