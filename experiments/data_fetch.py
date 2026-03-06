import pandas as pd
import tushare as ts
import akshare as ak
import os

# Initialize API with tushare personal Token
ts.set_token("31547b2f7191feeeaddd7561959b189c3f7e2bfd216cedbfa32baf0b")
pro = ts.pro_api()

# Make a new dir to save raw_data
os.makedirs("raw_data", exist_ok=True)

# fetch share data function 
# default stock: Kweichow Moutai
def fetch_a_share_data(stock_code="600519.SH", start_date="2025-01-01", end_date="2025-03-01"):
    """
    Fetch historical trading data of A-share stocks via Tushare API.
    
    Args:
        stock_code (str): Stock code (e.g., "600519.SH" for Kweichow Moutai)
        start_date (str): Start date in YYYYMMDD format
        end_date (str): End date in YYYYMMDD format
    
    Returns:
        pd.DataFrame: Historical trading data of the stock
    """
    # Tushare API
    df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
    # save as CSV
    df.to_csv("experiments/raw_data/a_share_price.csv", index=False)
    return df

# fetch fund data
# default: E Fund Blue Chip Selection
def fetch_fund_data(fund_code="005827"):
    """
    Fetch net asset value (NAV) data of domestic funds via AkShare API.
    
    Args:
        fund_code (str): Fund code (e.g., "005827" for E Fund Blue Chip Selection)
    
    Returns:
        pd.DataFrame: NAV data of the fund
    """
    df = ak.fund_open_fund_info_em(fund_code=fund_code, indicator="单位净值走势")
    df.to_csv("experiments/raw_data/fund_nav.csv", index=False)
    return df

# run fetch functions
if __name__ == "__main__":
    fetch_a_share_data()
    fetch_fund_data()
    print("Raw data successfully fetched, saved in experiments/raw_data/")