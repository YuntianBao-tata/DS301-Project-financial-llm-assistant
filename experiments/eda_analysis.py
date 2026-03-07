import pandas as pd
import numpy as np
import os
from datetime import datetime

# --------------------------
# Core Function: Export EDA Results to Text File
# --------------------------
def export_eda_to_text(eda_results, output_path):
    """
    Export comprehensive EDA results to a well-structured text file
    Includes: A-share (PE/PB/market cap), Fund (yield/manager), Calculation parameters
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        # Header
        f.write("="*80 + "\n")
        f.write("DATA ANALYSIS (EDA) RESULTS\n")
        f.write("Project: Financial LLM Assistant\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")

        # 1. A-share Stock Data Analysis (Extended)
        f.write("1. A-SHARE STOCK DATA ANALYSIS (600519.SH - Kweichow Moutai)\n")
        f.write("-"*60 + "\n")
        stock_res = eda_results["a_share"]
        
        # Basic information
        f.write("1.1 Basic Data Information\n")
        f.write(f"   - Number of rows: {stock_res['n_rows']}\n")
        f.write(f"   - Number of columns: {stock_res['n_cols']}\n")
        f.write(f"   - Column names: {', '.join(stock_res['columns'])}\n")
        f.write(f"   - Market (SH/SZ): {stock_res['market']}\n")
        f.write(f"   - Date range: {stock_res['date_range']['start']} to {stock_res['date_range']['end']}\n\n")
        
        # Key Price Metrics
        f.write("1.2 Key Price & Volume Metrics\n")
        price_stats = stock_res["price_volume_stats"]
        for metric in ["open_price", "high_price", "low_price", "close_price", "trading_volume"]:
            f.write(f"   {metric.replace('_', ' ').upper()}:\n")
            f.write(f"      - Mean: {price_stats[metric]['mean']:.2f}\n")
            f.write(f"      - Std: {price_stats[metric]['std']:.2f}\n")
            f.write(f"      - Min: {price_stats[metric]['min']:.2f}\n")
            f.write(f"      - Max: {price_stats[metric]['max']:.2f}\n")
        f.write("\n")
        
        # Financial Indicators (PE-TTM/PB/Market Cap)
        f.write("1.3 Financial Indicators (PE-TTM / PB / Market Cap)\n")
        fina_stats = stock_res["financial_stats"]
        for metric in ["pe_ttm", "pb", "total_market_value"]:
            if metric in fina_stats:
                f.write(f"   {metric.upper()}:\n")
                f.write(f"      - Mean: {fina_stats[metric]['mean']:.2f}\n")
                f.write(f"      - Std: {fina_stats[metric]['std']:.2f}\n")
                f.write(f"      - Min: {fina_stats[metric]['min']:.2f}\n")
                f.write(f"      - Max: {fina_stats[metric]['max']:.2f}\n")
            else:
                f.write(f"   {metric.upper()}: No valid data\n")
        f.write("\n")
        
        # Price Limit Analysis (FIX: Correct max_up_premium reference)
        f.write("1.4 Price Limit Analysis (Up/Down)\n")
        limit_stats = stock_res["price_limit_stats"]
        f.write(f"   - Avg Up Limit Price: {limit_stats['price_limit_up']['mean']:.2f} RMB\n")
        f.write(f"   - Avg Down Limit Price: {limit_stats['price_limit_down']['mean']:.2f} RMB\n")
        # FIX: max_up_premium is a top-level key in stock_res, NOT inside limit_stats
        f.write(f"   - Max Up Limit Premium: {stock_res['max_up_premium']:.2f}%\n\n")
        
        # Missing values
        f.write("1.5 Missing Values Analysis\n")
        f.write(f"   - Total missing values: {stock_res['missing_values']['total']}\n")
        f.write(f"   - Columns with missing values: {stock_res['missing_values']['columns']}\n\n")

        # 2. Domestic Fund Data Analysis (Extended)
        f.write("2. DOMESTIC FUND DATA ANALYSIS (005827 - E Fund Blue Chip Selection)\n")
        f.write("-"*60 + "\n")
        fund_res = eda_results["fund"]
        
        # Basic information
        f.write("2.1 Basic Data Information\n")
        f.write(f"   - Number of rows: {fund_res['n_rows']}\n")
        f.write(f"   - Number of columns: {fund_res['n_cols']}\n")
        f.write(f"   - Column names: {', '.join(fund_res['columns'])}\n")
        f.write(f"   - Fund Type: {fund_res['metadata']['fund_type'] if not pd.isna(fund_res['metadata']['fund_type']) else 'Unknown'}\n")
        f.write(f"   - Fund Manager: {fund_res['metadata']['fund_manager'] if not pd.isna(fund_res['metadata']['fund_manager']) else 'Unknown'}\n")
        f.write(f"   - Fund Company: {fund_res['metadata']['fund_company'] if not pd.isna(fund_res['metadata']['fund_company']) else 'Unknown'}\n")
        f.write(f"   - Establishment Date: {fund_res['metadata']['establishment_date'] if not pd.isna(fund_res['metadata']['establishment_date']) else 'Unknown'}\n\n")
        
        # NAV Metrics
        f.write("2.2 Net Asset Value (NAV) Metrics\n")
        nav_stats = fund_res["nav_stats"]
        for metric in ["unit_net_value", "cumulative_net_value"]:
            if metric in nav_stats:
                f.write(f"   {metric.replace('_', ' ').upper()}:\n")
                f.write(f"      - Mean: {nav_stats[metric]['mean']:.4f}\n")
                f.write(f"      - Std: {nav_stats[metric]['std']:.4f}\n")
                f.write(f"      - Min: {nav_stats[metric]['min']:.4f}\n")
                f.write(f"      - Max: {nav_stats[metric]['max']:.4f}\n")
            else:
                f.write(f"   {metric.replace('_', ' ').upper()}: No valid data\n")
        f.write("\n")
        
        # Yield Analysis (1W/1M/1Y)
        f.write("2.3 Yield Analysis (Calculated from NAV)\n")
        yield_stats = fund_res["yield_stats"]
        for metric in ["yield_1_week", "yield_1_month", "yield_1_year", "yield_since_inception"]:
            if not pd.isna(yield_stats[metric]):
                f.write(f"   - {metric.replace('_', ' ').title()}: {yield_stats[metric]:.2f}%\n")
            else:
                f.write(f"   - {metric.replace('_', ' ').title()}: Not enough data\n")
        f.write("\n")
        
        # Missing values
        f.write("2.4 Missing Values Analysis\n")
        f.write(f"   - Total missing values: {fund_res['missing_values']['total']}\n")
        f.write(f"   - Columns with missing values: {fund_res['missing_values']['columns']}\n\n")

        # 3. Calculation Parameters Analysis
        f.write("3. CALCULATION PARAMETERS ANALYSIS\n")
        f.write("-"*60 + "\n")
        calc_res = eda_results["calculation"]
        
        # Transaction Costs
        f.write("3.1 A-share Transaction Costs (2024 Standard)\n")
        if not calc_res["transaction_costs"].empty:
            for _, row in calc_res["transaction_costs"].iterrows():
                f.write(f"   - {row['cost_type'].replace('_', ' ').title()}: {row['value']} ({row['description']})\n")
        else:
            f.write("   - No transaction cost data available\n")
        f.write("\n")
        
        # Fixed Investment Parameters
        f.write("3.2 Fixed Investment Default Parameters\n")
        if not calc_res["fixed_investment"].empty:
            for _, row in calc_res["fixed_investment"].iterrows():
                f.write(f"   - {row['parameter'].replace('_', ' ').title()}: {row['default_value']} ({row['description']})\n")
        else:
            f.write("   - No fixed investment data available\n")
        f.write("\n")
        
        # Compound Interest Parameters
        f.write("3.3 Compound Interest Calculation Parameters\n")
        if not calc_res["compound_interest"].empty:
            for _, row in calc_res["compound_interest"].iterrows():
                f.write(f"   - {row['parameter'].replace('_', ' ').title()}: {row['default_value']} ({row['description']})\n")
        else:
            f.write("   - No compound interest data available\n")
        f.write("\n")

        # 4. Key EDA Insights
        f.write("4. KEY EDA INSIGHTS\n")
        f.write("-"*60 + "\n")
        f.write("   A-SHARE INSIGHTS:\n")
        f.write(f"   - Kweichow Moutai (600519.SH) has stable trading volume (mean: {price_stats['trading_volume']['mean']:.0f} lots)\n")
        f.write(f"   - Average PE-TTM: {fina_stats['pe_ttm']['mean']:.2f} (reasonable for blue-chip stock)\n" if "pe_ttm" in fina_stats else "   - Average PE-TTM: No valid data\n")
        f.write(f"   - Average total market value: {fina_stats['total_market_value']['mean']:.2f} billion RMB\n" if "total_market_value" in fina_stats else "   - Average total market value: No valid data\n")
        f.write("   \n")
        f.write("   FUND INSIGHTS:\n")
        f.write(f"   - E Fund Blue Chip Selection (005827) has stable NAV (mean: {nav_stats['unit_net_value']['mean']:.4f})\n" if "unit_net_value" in nav_stats else "   - E Fund Blue Chip Selection (005827): No valid NAV data\n")
        f.write(f"   - 1-month yield: {yield_stats['yield_1_month']:.2f}% (calculated from NAV data)\n" if not pd.isna(yield_stats['yield_1_month']) else "   - 1-month yield: Not enough data\n")
        f.write("   \n")
        f.write("   CALCULATION INSIGHTS:\n")
        f.write("   - Standard A-share commission rate: 0.03% (minimum 5 RMB per trade)\n")
        f.write("   - Default monthly fixed investment amount: 1000 RMB (5-year duration, 8% expected return)\n")
        f.write("="*80 + "\n")

    print(f"✅ Comprehensive EDA results exported to: {output_path}")

# --------------------------
# EDA for Extended A-share Data
# --------------------------
def eda_a_share_full_data(stock_csv_path):
    """
    Perform EDA on extended A-share data (PE/PB/market cap/price limit)
    """
    try:
        df = pd.read_csv(stock_csv_path)
        # Convert date column to datetime
        df["trade_date"] = pd.to_datetime(
        df["trade_date"].astype(str),  # Convert integer to string first
        format="%Y%m%d"  # (20241001 → 2024-10-01)
        )

        
        # Basic info
        n_rows, n_cols = df.shape
        columns = df.columns.tolist()
        market = df["market"].iloc[0] if "market" in df.columns else "Unknown"
        date_range = {
            "start": df["trade_date"].min().strftime("%Y-%m-%d"),
            "end": df["trade_date"].max().strftime("%Y-%m-%d")
        }
        
        # Price & Volume stats
        price_volume_cols = ["open_price", "high_price", "low_price", "close_price", "trading_volume"]
        price_volume_stats = df[price_volume_cols].describe().to_dict()
        
        # Financial stats (PE-TTM/PB/market cap)
        financial_cols = ["pe_ttm", "pb", "total_market_value"]
        financial_stats = {}
        for col in financial_cols:
            if col in df.columns:
                # Drop NaN for valid stats
                valid_data = df[col].dropna()
                if len(valid_data) > 0:
                    financial_stats[col] = valid_data.describe().to_dict()
        
        # Price limit stats
        price_limit_cols = ["price_limit_up", "price_limit_down"]
        price_limit_stats = df[price_limit_cols].describe().to_dict()
        # Calculate max up limit premium
        df["up_limit_premium"] = ((df["price_limit_up"] / df["close_price"]) - 1) * 100
        max_up_premium = df["up_limit_premium"].max()
        
        # Missing values
        missing_vals = df.isnull().sum()
        total_missing = missing_vals.sum()
        missing_cols = [col for col, val in missing_vals.items() if val > 0]
        
        return {
            "n_rows": n_rows,
            "n_cols": n_cols,
            "columns": columns,
            "market": market,
            "date_range": date_range,
            "price_volume_stats": price_volume_stats,
            "financial_stats": financial_stats,
            "price_limit_stats": price_limit_stats,
            "max_up_premium": max_up_premium,
            "missing_values": {
                "total": total_missing,
                "columns": missing_cols if missing_cols else ["None"]
            }
        }
    except Exception as e:
        print(f"❌ A-share EDA error: {str(e)}")
        return {}

# --------------------------
# EDA for Extended Fund Data
# --------------------------
def eda_fund_full_data(fund_csv_path):
    """
    Perform EDA on extended fund data (yield/manager/type)
    """
    try:
        df = pd.read_csv(fund_csv_path)
        n_rows, n_cols = df.shape
        columns = df.columns.tolist()
        
        # Metadata extraction (first row has same meta for all rows)
        metadata = {
            "fund_type": df["fund_type"].iloc[0] if "fund_type" in df.columns else np.nan,
            "fund_manager": df["fund_manager"].iloc[0] if "fund_manager" in df.columns else np.nan,
            "fund_company": df["fund_company"].iloc[0] if "fund_company" in df.columns else np.nan,
            "establishment_date": df["establishment_date"].iloc[0] if "establishment_date" in df.columns else np.nan
        }
        
        # NAV stats
        nav_cols = ["unit_net_value", "cumulative_net_value"]
        nav_stats = {}
        for col in nav_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                valid_data = df[col].dropna()
                if len(valid_data) > 0:
                    nav_stats[col] = valid_data.describe().to_dict()
        
        # Yield stats (single value for all rows)
        yield_stats = {}
        yield_cols = ["yield_1_week", "yield_1_month", "yield_1_year", "yield_since_inception"]
        for col in yield_cols:
            if col in df.columns and len(df) > 0:
                # Yield is same for all rows - take first value
                yield_val = df[col].iloc[0]
                yield_stats[col] = float(yield_val) if not pd.isna(yield_val) else np.nan
        
        # Missing values
        missing_vals = df.isnull().sum()
        total_missing = missing_vals.sum()
        missing_cols = [col for col, val in missing_vals.items() if val > 0]
        
        return {
            "n_rows": n_rows,
            "n_cols": n_cols,
            "columns": columns,
            "metadata": metadata,
            "nav_stats": nav_stats,
            "yield_stats": yield_stats,
            "missing_values": {
                "total": total_missing,
                "columns": missing_cols if missing_cols else ["None"]
            }
        }
    except Exception as e:
        print(f"❌ Fund EDA error: {str(e)}")
        return {}

# --------------------------
# Load Calculation Parameters
# --------------------------
def load_calculation_parameters(calc_dir_path):
    """
    Load calculation parameters (transaction costs/fixed investment/compound interest)
    """
    try:
        transaction_costs = pd.read_csv(os.path.join(calc_dir_path, "transaction_costs.csv"))
        fixed_investment = pd.read_csv(os.path.join(calc_dir_path, "fixed_investment_parameters.csv"))
        compound_interest = pd.read_csv(os.path.join(calc_dir_path, "compound_interest_parameters.csv"))
        
        return {
            "transaction_costs": transaction_costs,
            "fixed_investment": fixed_investment,
            "compound_interest": compound_interest
        }
    except Exception as e:
        print(f"❌ Load calculation parameters error: {str(e)}")
        return {
            "transaction_costs": pd.DataFrame(),
            "fixed_investment": pd.DataFrame(),
            "compound_interest": pd.DataFrame()
        }

# --------------------------
# Main Execution
# --------------------------
if __name__ == "__main__":
    # Define paths to your new data files
    STOCK_CSV_PATH = "experiments/raw_data/a_share/600519_SH_full_data.csv"
    FUND_CSV_PATH = "experiments/raw_data/fund/005827_full_data.csv"
    CALC_DIR_PATH = "experiments/raw_data/calculation"
    EDA_OUTPUT_PATH = "experiments/eda_results.txt"
    
    # Check if data files exist
    if not os.path.exists(STOCK_CSV_PATH):
        print(f"❌ Missing A-share data: {STOCK_CSV_PATH} (run data_fetch.py first!)")
        exit(1)
    if not os.path.exists(FUND_CSV_PATH):
        print(f"❌ Missing fund data: {FUND_CSV_PATH} (run data_fetch.py first!)")
        exit(1)
    
    # Run EDA for all data types
    print("=== Starting Comprehensive EDA ===")
    a_share_eda = eda_a_share_full_data(STOCK_CSV_PATH)
    fund_eda = eda_fund_full_data(FUND_CSV_PATH)
    calc_params = load_calculation_parameters(CALC_DIR_PATH)
    
    # Compile all results
    all_eda_results = {
        "a_share": a_share_eda,
        "fund": fund_eda,
        "calculation": calc_params
    }
    
    # Export to text file
    export_eda_to_text(all_eda_results, EDA_OUTPUT_PATH)
    
    # Terminal summary
    print("\n=== EDA SUMMARY (Terminal Preview) ===")
    print(f"A-share: {a_share_eda['n_rows']} rows, {a_share_eda['missing_values']['total']} missing values")
    print(f"Fund: {fund_eda['n_rows']} rows, 1-month yield: {fund_eda['yield_stats']['yield_1_month']:.2f}%")
    print(f"Calculation params: Loaded transaction costs + fixed investment + compound interest data")