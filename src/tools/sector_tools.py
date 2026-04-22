# src/tools/sector_tools.py
from langchain_core.tools import tool
import tushare as ts
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='api_keys.env')

@tool
def get_sector_stocks(industry: str) -> str:
    """
    Get a list of stocks in a specific industry/sector.
    Input: industry name (e.g., '白酒', '银行', '新能源')
    Returns: List of stock codes and names in that sector.
    """
    TS_TOKEN = os.getenv("TUSHARE_TOKEN")
    if not TS_TOKEN:
        return "Error: Tushare token missing."

    try:
        pro = ts.pro_api(TS_TOKEN)
        
        # Get all stocks in the specified industry
        df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market')
        
        if df is None or df.empty:
            return f"No data found for industry: {industry}"
        
        # Filter by industry (fuzzy match)
        sector_stocks = df[df['industry'].str.contains(industry, na=False)]
        
        if sector_stocks.empty:
            return f"No stocks found in industry '{industry}'. Try checking the exact industry name."
        
        # Format output
        result = []
        for _, row in sector_stocks.head(10).iterrows():  # Limit to top 10
            result.append(f"{row['name']}({row['ts_code']})")
            
        return f"Stocks in {industry} sector: {', '.join(result)}"

    except Exception as e:
        return f"Sector Query Error: {str(e)}"

@tool
def compare_stocks(ts_codes: str) -> str:
    """
    Compare multiple stocks by their key metrics (PE, PB, Market Cap, etc.)
    Input: comma-separated stock codes (e.g., '600519.SH,000858.SZ')
    Returns: Comparison table in text format.
    """
    TS_TOKEN = os.getenv("TUSHARE_TOKEN")
    if not TS_TOKEN:
        return "Error: Tushare token missing."

    try:
        pro = ts.pro_api(TS_TOKEN)
        codes = [code.strip() for code in ts_codes.split(',')]
        
        comparison_data = []
        
        for code in codes:
            # Get daily valuation data (PE, PB, total_mv)
            df = pro.daily_basic(ts_code=code, trade_date='', fields='ts_code,trade_date,pe,pb,total_mv')
            
            if df is not None and not df.empty:
                latest = df.iloc[0]
                comparison_data.append({
                    'Code': code,
                    'PE': f"{latest['pe']:.2f}",
                    'PB': f"{latest['pb']:.2f}",
                    'Market_Cap_B': f"{latest['total_mv']/100000000:.2f}"
                })
        
        if not comparison_data:
            return f"No data found for the provided stock codes: {ts_codes}"
        
        # Create comparison table
        df_result = pd.DataFrame(comparison_data)
        return df_result.to_string(index=False)

    except Exception as e:
        return f"Comparison Error: {str(e)}"