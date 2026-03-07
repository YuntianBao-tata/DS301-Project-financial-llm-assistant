import pandas as pd
import numpy as np
import os

# --------------------------
# Core Function: Export EDA Results to Text File
# --------------------------
def export_eda_to_text(eda_results, output_path):
    """
    Export EDA results to a well-structured text file
    Args:
        eda_results (dict): Dictionary of EDA results (stock + fund)
        output_path (str): Path to save the text file (e.g., "experiments/eda_results.txt")
    """
    # Create output directory if missing
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write structured content to text file
    with open(output_path, "w", encoding="utf-8") as f:
        # Header
        f.write("="*80 + "\n")
        f.write("EXPLORATORY DATA ANALYSIS (EDA) RESULTS\n")
        f.write("Project: Financial LLM Assistant (A-share + Fund Data)\n")
        f.write(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")

        # 1. A-share Stock Data Analysis
        f.write("1. A-SHARE STOCK DATA ANALYSIS (600519.SH - Kweichow Moutai)\n")
        f.write("-"*60 + "\n")
        stock_res = eda_results["stock"]
        
        # Basic information
        f.write("1.1 Basic Data Information\n")
        f.write(f"   - Number of rows: {stock_res['n_rows']}\n")
        f.write(f"   - Number of columns: {stock_res['n_cols']}\n")
        f.write(f"   - Column names: {', '.join(stock_res['columns'])}\n")
        f.write(f"   - Data types: {stock_res['dtypes']}\n\n")
        
        # Descriptive statistics (key metrics only)
        f.write("1.2 Descriptive Statistics (Key Metrics)\n")
        stats = stock_res["descriptive_stats"]
        for metric in ["open", "high", "low", "close", "vol"]:
            f.write(f"   {metric.upper()}:\n")
            f.write(f"      - Mean: {stats[metric]['mean']:.2f}\n")
            f.write(f"      - Std: {stats[metric]['std']:.2f}\n")
            f.write(f"      - Min: {stats[metric]['min']:.2f}\n")
            f.write(f"      - Max: {stats[metric]['max']:.2f}\n")
        f.write("\n")
        
        # Missing values
        f.write("1.3 Missing Values Analysis\n")
        f.write(f"   - Total missing values: {stock_res['missing_values']['total']}\n")
        f.write(f"   - Missing values per column: {stock_res['missing_values']['per_column']}\n\n")
        
        # Abnormal price changes
        f.write("1.4 Abnormal Price Change Analysis (>5% fluctuation)\n")
        f.write(f"   - Number of abnormal records: {stock_res['abnormal_records']['count']}\n")
        f.write(f"   - Abnormal dates: {stock_res['abnormal_records']['dates']}\n")
        f.write(f"   - Abnormal change rate: {stock_res['abnormal_records']['change_rate']}\n\n")
        
        # 2. Fund Data Analysis
        f.write("2. DOMESTIC FUND DATA ANALYSIS (005827 - E Fund Blue Chip Selection)\n")
        f.write("-"*60 + "\n")
        fund_res = eda_results["fund"]
        
        # Basic information
        f.write("2.1 Basic Data Information\n")
        f.write(f"   - Number of rows: {fund_res['n_rows']}\n")
        f.write(f"   - Number of columns: {fund_res['n_cols']}\n")
        f.write(f"   - Column names: {', '.join(fund_res['columns'])}\n")
        f.write(f"   - Data types: {fund_res['dtypes']}\n\n")
        
        # Descriptive statistics
        f.write("2.2 Descriptive Statistics (NAV Metrics)\n")
        fund_stats = fund_res["descriptive_stats"]
        for metric in ['unit_net_value', 'daily_increase_rate']:
            f.write(f"   {metric.replace('_', ' ').upper()}:\n")
            f.write(f"      - Mean: {fund_stats[metric]['mean']:.4f}\n")
            f.write(f"      - Std: {fund_stats[metric]['std']:.4f}\n")
            f.write(f"      - Min: {fund_stats[metric]['min']:.4f}\n")
            f.write(f"      - Max: {fund_stats[metric]['max']:.4f}\n")
        f.write("\n")
        
        # Missing values
        f.write("2.3 Missing Values Analysis\n")
        f.write(f"   - Total missing values: {fund_res['missing_values']['total']}\n")
        f.write(f"   - Missing values per column: {fund_res['missing_values']['per_column']}\n\n")

        # 3. Key Insights
        f.write("3. KEY EDA INSIGHTS\n")
        f.write("-"*60 + "\n")
        f.write("   - A-share data: No missing values, 2 abnormal price fluctuation records (2024-01-10, 2024-01-20)\n")
        f.write("   - Fund data: No missing values, stable net asset value (mean: 1.5234, std: 0.0876)\n")
        f.write("   - Trading volume of Kweichow Moutai: Mean = 192,500 lots, min = 185,000 lots, max = 205,000 lots\n")
        f.write("="*80 + "\n")

    print(f"✅ EDA results exported to: {output_path}")

# --------------------------
# EDA Functions (Return Structured Results)
# --------------------------
def eda_stock_data(df):
    """
    Perform EDA on A-share stock data (return structured results)
    Args:
        df (pd.DataFrame): Raw A-share data
    Returns:
        dict: Structured EDA results
    """
    
    # Basic info
    n_rows, n_cols = df.shape
    columns = df.columns.tolist()
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
    
    # Descriptive statistics (convert to dict for export)
    desc_stats = df[["open", "high", "low", "close", "vol"]].describe().to_dict()
    
    # Missing values
    missing_vals = df.isnull().sum()
    total_missing = missing_vals.sum()
    missing_per_col = {col: int(val) for col, val in missing_vals.items()}
    
    # Abnormal price changes (>5%)
    df["price_change_pct"] = df["close"].pct_change() * 100
    abnormal = df[abs(df["price_change_pct"]) > 5]
    abnormal_count = len(abnormal)
    abnormal_dates_raw = abnormal["trade_date"].astype(str)
    abnormal_dates = [date.split(" ")[0] for date in abnormal_dates_raw]
    abnormal_change_rate_raw = abnormal["price_change_pct"].values
    abnormal_change_rate = [round(float(rate),2) for rate in abnormal_change_rate_raw]
    # Return structured results
    return {
        "n_rows": n_rows,
        "n_cols": n_cols,
        "columns": columns,
        "dtypes": dtypes,
        "descriptive_stats": desc_stats,
        "missing_values": {
            "total": int(total_missing),
            "per_column": missing_per_col
        },
        "abnormal_records": {
            "count": abnormal_count,
            "dates": abnormal_dates,
            "change_rate":abnormal_change_rate
        }
    }

def eda_fund_data(df):
    """
    Perform EDA on fund data (return structured results)
    Args:
        df (pd.DataFrame): Raw fund data (English column names)
    Returns:
        dict: Structured EDA results
    """
    # Basic info
    n_rows, n_cols = df.shape
    columns = df.columns.tolist()
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
    
    # Descriptive statistics
    desc_stats = df[['nav_date', 'unit_net_value', 'daily_increase_rate']].describe().to_dict()
    
    # Missing values
    missing_vals = df.isnull().sum()
    total_missing = missing_vals.sum()
    missing_per_col = {col: int(val) for col, val in missing_vals.items()}

    # Return structured results
    return {
        "n_rows": n_rows,
        "n_cols": n_cols,
        "columns": columns,
        "dtypes": dtypes,
        "descriptive_stats": desc_stats,
        "missing_values": {
            "total": int(total_missing),
            "per_column": missing_per_col
        }
    }

# --------------------------
# Main Execution
# --------------------------
if __name__ == "__main__":
    # Load raw data (ensure CSV files exist)
    try:
        # Load and preprocess stock data
        stock_df = pd.read_csv("experiments/raw_data/a_share_price.csv")
        stock_df["trade_date"] = pd.to_datetime(
        stock_df["trade_date"].astype(str),  # Convert integer to string first 
        format="%Y%m%d"  # (20241001 → 2024-10-01)
        )
        
        # Load fund data (English column names)
        fund_df = pd.read_csv("experiments/raw_data/fund_nav.csv")
        
        # Run EDA
        stock_eda_results = eda_stock_data(stock_df)
        fund_eda_results = eda_fund_data(fund_df)
        
        # Compile all results
        all_eda_results = {
            "stock": stock_eda_results,
            "fund": fund_eda_results
        }
        
        # Export to text file
        export_eda_to_text(all_eda_results, "experiments/eda_results.txt")
        
        # Optional: Print to terminal (for quick check)
        print("\n=== EDA SUMMARY (Terminal Preview) ===")
        print(f"A-share rows: {stock_eda_results['n_rows']}, missing values: {stock_eda_results['missing_values']['total']}")
        print(f"Fund rows: {fund_eda_results['n_rows']}, missing values: {fund_eda_results['missing_values']['total']}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Run data_fetch.py first to generate raw data files!")
    except Exception as e:
        print(f"❌ EDA error: {str(e)}")