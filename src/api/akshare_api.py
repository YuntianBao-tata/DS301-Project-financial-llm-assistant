import akshare as ak
import pandas as pd

def get_stock_news(symbol: str = "600519"):
    """
    Fetch latest stock news using AkShare.
    Symbol example: 600519 (Kweichow Moutai)
    """
    try:
        # Note: Akshare interface might change, this is a common example
        # Using individual stock news interface
        stock_news_em_df = ak.stock_news_em(symbol=symbol)
        if not stock_news_em_df.empty:
            return stock_news_em_df[['title', 'publish_time', 'source']].head(5).to_string(index=False)
        return "No news found."
    except Exception as e:
        return f"Error fetching news: {str(e)}"

def get_macro_economic():
    """
    Fetch a simple macroeconomic indicator (e.g., US Non-farm payrolls)
    """
    try:
        # Example: US Non-farm payrolls
        macro_usa_non_farm_df = ak.macro_usa_non_farm()
        return macro_usa_non_farm_df.head(5).to_string(index=False)
    except Exception as e:
        return f"Error fetching macro data: {str(e)}"