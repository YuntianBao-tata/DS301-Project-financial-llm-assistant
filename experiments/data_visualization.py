import os
import pandas as pd
import matplotlib.pyplot as plt


# Create directory for plots
os.makedirs("experiments/plots", exist_ok=True)

# Load data
stock_df = pd.read_csv("experiments/raw_data/a_share_price.csv")
stock_df["trade_date"] = pd.to_datetime(stock_df["trade_date"])

def plot_stock_price_trend(df):
    """
    Plot the closing price trend of A-share stock.
    
    Args:
        df (pd.DataFrame): Processed A-share data with datetime format
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df["trade_date"], df["close"], label="Closing Price", color="red")
    plt.title("Kweichow Moutai (600519.SH) Price Trend (Jan-Mar 2025)")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (CNY)")
    plt.legend()
    plt.grid(True)
    plt.savefig("experiments/plots/stock_price_trend.png", dpi=300, bbox_inches="tight")
    plt.close()

def plot_stock_trading_volume(df):
    """
    Plot the trading volume of A-share stock.
    
    Args:
        df (pd.DataFrame): Processed A-share data with datetime format
    """
    plt.figure(figsize=(10, 4))
    plt.bar(df["trade_date"], df["vol"], color="blue", alpha=0.7)
    plt.title("Kweichow Moutai (600519.SH) Trading Volume Trend (Jan-Mar 2025)")
    plt.xlabel("Date")
    plt.ylabel("Trading Volume (Lots)")
    plt.grid(True, axis="y")
    plt.savefig("experiments/plots/stock_volume.png", dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    plot_stock_price_trend(stock_df)
    plot_stock_trading_volume(stock_df)
    print("Visualization plots saved to experiments/plots/")