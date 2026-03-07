import os

import tushare as ts
import akshare as ak
import pandas as pd
import numpy as np



# Create directories for data storage (split by data type)
os.makedirs("experiments/raw_data", exist_ok=True)
os.makedirs("experiments/raw_data/a_share", exist_ok=True)
os.makedirs("experiments/raw_data/fund", exist_ok=True)
os.makedirs("experiments/raw_data/calculation", exist_ok=True)

# Initialize Tushare API (critical: must be valid)
try:
    ts.set_token("31547b2f7191feeeaddd7561959b189c3f7e2bfd216cedbfa32baf0b")
    pro = ts.pro_api()
    print("✅ Tushare API initialized successfully")
except Exception as e:
    print(f"❌ Tushare API init failed: {str(e)}")
    pro = None  # Prevent crash if Token is invalid

# --------------------------
# 1. A-share Data 
# --------------------------
def fetch_a_share_full_data(stock_code="600519.SH", start_date="20240101", end_date="20241231"):
    """
    Fetch A-share data with extended financial indicators:
    - Basic: price, volume, price limit
    - Financial: PE-TTM, PB, total market value
    - Market: Shanghai/Shenzhen coverage
    """
    if pro is None:
        print("❌ Tushare API not initialized - skip A-share data fetch")
        return pd.DataFrame()
    
    try:
        # 1. Basic trading data (daily)
        daily_df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
        
        # 2. Financial indicators (PE-TTM, PB, market cap)
        # Get stock basic info (for market cap/industry)
        basic_df = pro.stock_basic(ts_code=stock_code)
        # Get daily financial indicators (PE/PB)
        fina_indicator_df = pro.daily_basic(
            ts_code=stock_code, 
            start_date=start_date, 
            end_date=end_date,
            fields="trade_date,pe_ttm,pb,total_mv"  # PE-TTM, PB, total market value
        )
        
        # 3. Price limit data (up/down limit)
        # Calculate price limit (10% for normal stocks, 5% for ST)
        daily_df["price_limit_up"] = daily_df["close"] * 1.1  # Up limit
        daily_df["price_limit_down"] = daily_df["close"] * 0.9  # Down limit
        # Round to 2 decimal places (stock price precision)
        daily_df[["price_limit_up", "price_limit_down"]] = daily_df[["price_limit_up", "price_limit_down"]].round(2)
        
        # 4. Merge all A-share data
        a_share_df = pd.merge(daily_df, fina_indicator_df, on="trade_date", how="left")
        # Add basic info (market: SH/SZ)
        a_share_df["market"] = stock_code.split(".")[-1]  # SH=Shanghai, SZ=Shenzhen
        a_share_df["stock_name"] = basic_df["name"].iloc[0] if not basic_df.empty else "Unknown"
        
        # 5. Rename columns to English (standardized)
        a_share_df.rename(
            columns={
                "ts_code": "stock_code",
                "trade_date": "trade_date",
                "open": "open_price",
                "high": "high_price",
                "low": "low_price",
                "close": "close_price",
                "vol": "trading_volume",
                "amount": "trading_amount",
                "pe_ttm": "pe_ttm",  # Price-Earnings TTM
                "pb": "pb",  # Price-to-Book
                "total_mv": "total_market_value",  # Total market value (100 million RMB)
                "price_limit_up": "price_limit_up",
                "price_limit_down": "price_limit_down",
                "market": "market",  # SH/SZ
                "stock_name": "stock_name"
            },
            inplace=True
        )
        
        # 6. Save to CSV (split by stock code)
        a_share_df.to_csv(f"experiments/raw_data/a_share/{stock_code.replace('.', '_')}_full_data.csv", index=False)
        print(f"✅ A-share full data saved: {len(a_share_df)} rows × {len(a_share_df.columns)} columns")
        return a_share_df
    
    except Exception as e:
        print(f"❌ A-share full data fetch error: {str(e)}")
        return pd.DataFrame()

# --------------------------
# 2. Domestic Fund Data
# --------------------------
def fetch_fund_full_data(fund_code="005827"):
    """
    Fetch fund data with extended indicators (compatible with all AkShare versions)
    Enhanced: Calculate 1-week/1-month/1-year yield from NAV data (fallback)
    """
    try:
        # 1. Basic NAV data (unit/net value)
        nav_df = ak.fund_open_fund_info_em(fund_code, "单位净值走势")
        # Robust column renaming (handle missing columns)
        column_mapping = {
            "净值日期": "nav_date",
            "单位净值": "unit_net_value",
            "累计净值": "cumulative_net_value",
            "日增长率": "daily_return_rate"
        }
        existing_cols = nav_df.columns.tolist()
        rename_dict = {k: v for k, v in column_mapping.items() if k in existing_cols}
        nav_df.rename(columns=rename_dict, inplace=True)
        
        # 2. Fund yield data (1 week/1 month/1 year) - COMPATIBLE VERSION
        fund_yield = {
            "yield_1_week": np.nan,
            "yield_1_month": np.nan,
            "yield_1_year": np.nan,
            "yield_since_inception": np.nan
        }
        
        # Try multiple AkShare fund yield interfaces (fallback if one fails)
        yield_fetched = False
        try:
            # Method 1: New AkShare version (fund performance summary)
            perf_df = ak.fund_open_fund_performance_em(fund_code=fund_code)
            if not perf_df.empty:
                perf_dict = perf_df.set_index("指标名称")["最新值"].to_dict()
                fund_yield = {
                    "yield_1_week": perf_dict.get("近1周", np.nan),
                    "yield_1_month": perf_dict.get("近1月", np.nan),
                    "yield_1_year": perf_dict.get("近1年", np.nan),
                    "yield_since_inception": perf_dict.get("成立来", np.nan)
                }
                yield_fetched = True
        except:
            try:
                # Method 2: Old AkShare version (fund yield)
                yield_df = ak.fund_yield(fund=fund_code)
                if not yield_df.empty:
                    fund_yield = {
                        "yield_1_week": yield_df["近一周"].iloc[0] if "近一周" in yield_df.columns else np.nan,
                        "yield_1_month": yield_df["近一月"].iloc[0] if "近一月" in yield_df.columns else np.nan,
                        "yield_1_year": yield_df["近一年"].iloc[0] if "近一年" in yield_df.columns else np.nan,
                        "yield_since_inception": yield_df["成立来"].iloc[0] if "成立来" in yield_df.columns else np.nan
                    }
                    yield_fetched = True
            except:
                # Method 3: Calculate yield from NAV data (ENHANCED for all timeframes)
                if "unit_net_value" in nav_df.columns and len(nav_df) > 0:
                    nav_df["unit_net_value"] = pd.to_numeric(nav_df["unit_net_value"], errors="coerce")
                    nav_df = nav_df.sort_values("nav_date").dropna(subset=["unit_net_value"])
                    nav_df["nav_date"] = pd.to_datetime(nav_df["nav_date"])  # Ensure date format
                    
                    if len(nav_df) >= 2:
                        latest_nav = nav_df["unit_net_value"].iloc[-1]
                        latest_date = nav_df["nav_date"].iloc[-1]
                        
                        # 1-WEEK yield (last 7 days)
                        one_week_ago = latest_date - pd.Timedelta(days=7)
                        week_df = nav_df[nav_df["nav_date"] <= one_week_ago]
                        if not week_df.empty:
                            week_ago_nav = week_df["unit_net_value"].iloc[-1]
                            fund_yield["yield_1_week"] = ((latest_nav / week_ago_nav) - 1) * 100
                        
                        # 1-MONTH yield (last 30 days)
                        one_month_ago = latest_date - pd.Timedelta(days=30)
                        month_df = nav_df[nav_df["nav_date"] <= one_month_ago]
                        if not month_df.empty:
                            month_ago_nav = month_df["unit_net_value"].iloc[-1]
                            fund_yield["yield_1_month"] = ((latest_nav / month_ago_nav) - 1) * 100
                        
                        # 1-YEAR yield (last 365 days)
                        one_year_ago = latest_date - pd.Timedelta(days=365)
                        year_df = nav_df[nav_df["nav_date"] <= one_year_ago]
                        if not year_df.empty:
                            year_ago_nav = year_df["unit_net_value"].iloc[-1]
                            fund_yield["yield_1_year"] = ((latest_nav / year_ago_nav) - 1) * 100
                        
                        # Yield since inception
                        first_nav = nav_df["unit_net_value"].iloc[0]
                        fund_yield["yield_since_inception"] = ((latest_nav / first_nav) - 1) * 100
                    
                    print(f"✅ Calculated fund yields from NAV data (fallback):")
                    print(f"   - 1-week: {fund_yield['yield_1_week']:.2f}%" if not np.isnan(fund_yield['yield_1_week']) else "   - 1-week: Not enough data")
                    print(f"   - 1-month: {fund_yield['yield_1_month']:.2f}%" if not np.isnan(fund_yield['yield_1_month']) else "   - 1-month: Not enough data")
                    print(f"   - 1-year: {fund_yield['yield_1_year']:.2f}%" if not np.isnan(fund_yield['yield_1_year']) else "   - 1-year: Not enough data")
        
        # 3. Fund metadata (type/manager) - Stable interface
        fund_meta = {
            "fund_type": np.nan,
            "fund_manager": np.nan,
            "fund_company": np.nan,
            "establishment_date": np.nan,
            "fund_scale": np.nan
        }
        try:
            meta_df = ak.fund_open_fund_info_em(fund_code, "基金概况")
            if not meta_df.empty:
                # Handle different meta df formats
                if "项目" in meta_df.columns and "内容" in meta_df.columns:
                    meta_dict = meta_df.set_index("项目")["内容"].to_dict()
                elif "指标名称" in meta_df.columns and "最新值" in meta_df.columns:
                    meta_dict = meta_df.set_index("指标名称")["最新值"].to_dict()
                else:
                    meta_dict = {}
                
                fund_meta = {
                    "fund_type": meta_dict.get("基金类型", np.nan),
                    "fund_manager": meta_dict.get("基金经理", np.nan),
                    "fund_company": meta_dict.get("基金管理人", np.nan),
                    "establishment_date": meta_dict.get("成立日期", np.nan),
                    "fund_scale": meta_dict.get("基金规模", np.nan)
                }
        except:
            print(f"⚠️ Could not fetch fund metadata for {fund_code}")
        
        # 4. Merge fund data
        for key, value in fund_yield.items():
            nav_df[key] = value
        for key, value in fund_meta.items():
            nav_df[key] = value
        
        # 5. Save to CSV
        nav_df.to_csv(f"experiments/raw_data/fund/{fund_code}_full_data.csv", index=False)
        print(f"✅ Fund full data saved: {len(nav_df)} rows × {len(nav_df.columns)} columns")
        return nav_df
    
    except Exception as e:
        print(f"❌ Fund full data fetch error: {str(e)}")
        # Fallback: Empty DF with required columns
        fallback_df = pd.DataFrame(columns=["nav_date", "unit_net_value", "cumulative_net_value"])
        fallback_df.to_csv(f"experiments/raw_data/fund/{fund_code}_full_data.csv", index=False)
        return fallback_df

# --------------------------
# 3. Calculation-Related Data 
# --------------------------
def fetch_calculation_parameters():
    """
    Generate calculation-related data:
    - A-share transaction costs (commission, stamp duty)
    - Fixed investment parameters
    - Compound interest calculation parameters
    """
    # 1. Transaction cost parameters (2024 China A-share standard)
    transaction_costs = pd.DataFrame({
        "cost_type": [
            "commission_rate",  # Broker commission (0.02% - 0.3%)
            "stamp_duty_rate",  # Stamp duty (0.1% for sell only)
            "transfer_fee_rate",  # Transfer fee (0.002% for Shanghai only)
            "minimum_commission",  # Minimum commission (5 RMB per trade)
        ],
        "value": [0.0003, 0.001, 0.00002, 5.0],  # Default rates (common values)
        "description": [
            "Broker commission rate (0.03% of trade amount)",
            "Stamp duty rate (0.1% for sell orders only)",
            "Transfer fee rate (Shanghai stock market only)",
            "Minimum commission per trade (RMB)"
        ],
        "applicability": [
            "Buy + Sell",
            "Sell only",
            "Shanghai stocks only (Buy + Sell)",
            "All trades (if commission < 5 RMB, charge 5 RMB)"
        ]
    })
    
    # 2. Fixed investment parameters (common settings)
    fixed_investment = pd.DataFrame({
        "parameter": [
            "fixed_investment_amount",  # Monthly fixed investment amount
            "investment_frequency",  # Frequency (monthly/weekly)
            "investment_duration_years",  # Total duration (years)
            "expected_annual_return_rate"  # Expected annual return
        ],
        "default_value": [1000.0, "monthly", 5.0, 0.08],
        "description": [
            "Default monthly fixed investment amount (RMB)",
            "Investment frequency (monthly/weekly)",
            "Total fixed investment duration (years)",
            "Expected annual return rate (8% for moderate risk)"
        ]
    })
    
    # 3. Compound interest parameters
    compound_interest = pd.DataFrame({
        "parameter": [
            "principal",  # Initial principal
            "annual_rate",  # Annual interest rate
            "compounding_frequency",  # Times per year (1=annual, 12=monthly)
            "years"  # Investment years
        ],
        "default_value": [10000.0, 0.04, 12, 10.0],
        "description": [
            "Initial investment principal (RMB)",
            "Annual interest rate (4% for low-risk)",
            "Compounding frequency per year (12=monthly compounding)",
            "Total investment period (years)"
        ]
    })
    
    # 4. Save calculation data to CSV
    transaction_costs.to_csv("experiments/raw_data/calculation/transaction_costs.csv", index=False)
    fixed_investment.to_csv("experiments/raw_data/calculation/fixed_investment_parameters.csv", index=False)
    compound_interest.to_csv("experiments/raw_data/calculation/compound_interest_parameters.csv", index=False)
    
    print("✅ Calculation parameters saved:")
    print("   - Transaction costs: experiments/raw_data/calculation/transaction_costs.csv")
    print("   - Fixed investment: experiments/raw_data/calculation/fixed_investment_parameters.csv")
    print("   - Compound interest: experiments/raw_data/calculation/compound_interest_parameters.csv")
    
    return {
        "transaction_costs": transaction_costs,
        "fixed_investment": fixed_investment,
        "compound_interest": compound_interest
    }

# --------------------------
# Main Execution
# --------------------------
if __name__ == "__main__":
    print("=== Starting Full Data Fetch ===")
    
    # 1. Fetch A-share full data (Kweichow Moutai 600519.SH)
    fetch_a_share_full_data(stock_code="600519.SH", start_date="20240101", end_date="20240131")
    
    # 2. Fetch Fund full data (E Fund Blue Chip Selection 005827)
    fetch_fund_full_data(fund_code="005827")
    
    # 3. Generate calculation parameters
    fetch_calculation_parameters()
    
    print("\n=== All data fetch completed! ===")
    print("Check experiments/raw_data/ for:")
    print("   - A-share data: a_share/600519_SH_full_data.csv")
    print("   - Fund data: fund/005827_full_data.csv")
    print("   - Calculation data: calculation/ (transaction costs, fixed investment, compound interest)")