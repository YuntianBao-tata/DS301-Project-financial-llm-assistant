import pandas as pd
import numpy as np

# read csv from raw data dir
stock_df = pd.read_csv("experiments/raw_data/a_share_price.csv")
fund_df = pd.read_csv("experiments/raw_data/fund_nav.csv")

def eda_stock_data(df):
    """EDA FOR STOCK"""
    print("=== Basic Info of Chinese A-shares ===")
    # 1. basic info
    print(df.info())
    # 2. mean, std, max
    print(df[["open", "high", "low", "close", "vol"]].describe())
    # 3. nuns test
    print("The number of nuns：\n", df.isnull().sum())
    # 4. abnormal value (eg. extreme fluctuates)
    df["pct_chg"] = df["close"].pct_change()
    abnormal = df[abs(df["pct_chg"]) > 0.05]  # An increase or decrease of more than 5% is considered abnormal.
    print(f"# Rows with abnormal value：{len(abnormal)}")
    return df

def eda_fund_data(df):
    """EDA for funds"""
    print("\n=== Basic Info of Chinese funds ===")
    print(df.info())
    print(df.describe())
    print("The number of nuns：\n", df.isnull().sum())
    return df

# EDA
if __name__ == "__main__":
    eda_stock_data(stock_df)
    eda_fund_data(fund_df)