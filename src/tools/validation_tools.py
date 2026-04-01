from langchain.tools import tool
import re

@tool
def validate_stock_code(stock_code: str):
    """Validate A-share stock code format (e.g., 600519.SH)"""
    pattern = r"^\d{6}\.(SH|SZ)$"
    if re.match(pattern, stock_code):
        return "Valid stock code"
    return "Invalid code: Use format like 600519.SH or 000001.SZ"

@tool
def validate_fund_code(fund_code: str):
    """Validate domestic fund code format (6 digits)"""
    if fund_code.isdigit() and len(fund_code) == 6:
        return "Valid fund code"
    return "Invalid code: Fund code must be 6 digits"