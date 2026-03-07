import os
import pandas as pd
import matplotlib.pyplot as plt


# Create directory for plots
os.makedirs("experiments/plots", exist_ok=True)

# Load data
stock_df = pd.read_csv("experiments/raw_data/a_share_price.csv")
stock_df["trade_date"] = pd.to_datetime(stock_df["trade_date"])
stock_df = stock_df.sort_values("trade_date").reset_index(drop=True)
stock_df["vol_change_pct"] = stock_df["vol"].pct_change() * 100

def plot_stock_price_trend(df):
    """
    Plot the closing price trend of A-share stock.
    
    Args:
        df (pd.DataFrame): Processed A-share data with datetime format
    """

    
    vol_min = df["vol"].min()
    vol_max = df["vol"].max()
    # Add 5% buffer above/below min/max to focus on fluctuations
    y_min = vol_min * 0.95
    y_max = vol_max * 1.05

    # === Create plot ===
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot bars with conditional coloring
    bars = ax.bar(
        df["trade_date"],
        df["vol"],
        width=0.8,  # Slightly narrower bars
        alpha=0.8,  # Transparency for clarity
        edgecolor="black",  # Black edges to separate bars
        linewidth=0.5
    )

    # === Highlight bars with >5% volume change ===
    for i, bar in enumerate(bars):
        if abs(df.loc[i, "vol_change_pct"]) > 5:  # >5% change
            bar.set_color("#e74c3c")  # Red for big changes
        else:
            bar.set_color("#3498db")  # Blue for normal days

    # === Add daily volume labels (small font, rotated) ===
    ax.bar_label(
        bars,
        labels=[f"{int(v):,}" for v in df["vol"]], 
        fontsize=8,
        rotation=90,
        padding=3,  # Distance from bar top
        color="black"
    )

   
    ax.set_ylim(y_min, y_max)  # Focus on fluctuation range
    ax.set_xlabel("Trade Date", fontsize=12, fontweight="bold")
    ax.set_ylabel("Trading Volume (Lots)", fontsize=12, fontweight="bold")
    ax.set_title("Kweichow Moutai (600519.SH) Daily Trading Volume (Jan 2024)", fontsize=14, fontweight="bold")

   
    ax.grid(True, axis="y", alpha=0.3, linestyle="--")  # Light grid lines
    plt.xticks(rotation=45, ha="right")  # Rotate dates to avoid overlap
    plt.tight_layout()  # Auto-adjust layout

    
    plt.savefig(
        "experiments/plots/stock_volume.png",
        bbox_inches="tight",  # Prevent label cutoff
        facecolor="white"     # White background (not transparent)
    )
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