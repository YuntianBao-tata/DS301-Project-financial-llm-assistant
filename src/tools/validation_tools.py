# src/tools/validation_tools.py
from langchain_core.tools import tool

@tool
def validate_stock_code(code: str) -> str:
    """
    Validates and formats a stock code. 
    Ensures it has the correct suffix (.SH or .SZ).
    Returns the formatted code.
    """
    code = code.upper().strip()
    
    # Simple logic to append suffix if missing
    if "." not in code:
        if code.startswith("6") or code.startswith("9"):
            return f"{code}.SH"
        elif code.startswith("0") or code.startswith("3"):
            return f"{code}.SZ"
        else:
            return f"{code}.SH" # Default fallback
    return code

@tool
def validate_fund_code(code: str) -> str:
    """
    Validates a fund code (usually 6 digits).
    """
    return code.strip()