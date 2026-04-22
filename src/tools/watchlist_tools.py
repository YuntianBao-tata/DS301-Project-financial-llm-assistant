# src/tools/watchlist_tools.py
from langchain_core.tools import tool
import json
import os
from pathlib import Path

WATCHLIST_FILE = Path("data/watchlist.json")

def ensure_watchlist_file():
    """Create the data directory and file if they don't exist."""
    WATCHLIST_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not WATCHLIST_FILE.exists():
        WATCHLIST_FILE.write_text(json.dumps({"stocks": []}))

@tool
def add_to_watchlist(ts_code: str, name: str = "") -> str:
    """
    Add a stock to your personal watchlist.
    Input: ts_code (e.g., '600519.SH'), optional name
    Returns: Confirmation message.
    """
    ensure_watchlist_file()
    
    try:
        with open(WATCHLIST_FILE, 'r') as f:
            watchlist = json.load(f)
        
        # Check if already exists
        for stock in watchlist['stocks']:
            if stock['code'] == ts_code:
                return f"{ts_code} is already in your watchlist."
        
        # Add new stock
        watchlist['stocks'].append({'code': ts_code, 'name': name or ts_code})
        
        with open(WATCHLIST_FILE, 'w') as f:
            json.dump(watchlist, f, indent=2)
            
        return f"Added {name or ts_code} ({ts_code}) to your watchlist."
        
    except Exception as e:
        return f"Error adding to watchlist: {str(e)}"

@tool
def remove_from_watchlist(ts_code: str) -> str:
    """
    Remove a stock from your watchlist.
    Input: ts_code (e.g., '600519.SH')
    Returns: Confirmation message.
    """
    ensure_watchlist_file()
    
    try:
        with open(WATCHLIST_FILE, 'r') as f:
            watchlist = json.load(f)
        
        watchlist['stocks'] = [s for s in watchlist['stocks'] if s['code'] != ts_code]
        
        with open(WATCHLIST_FILE, 'w') as f:
            json.dump(watchlist, f, indent=2)
            
        return f"Removed {ts_code} from your watchlist."
        
    except Exception as e:
        return f"Error removing from watchlist: {str(e)}"

@tool
def list_watchlist() -> str:
    """
    List all stocks currently in your watchlist.
    Returns: Formatted list of watchlist stocks.
    """
    ensure_watchlist_file()
    
    try:
        with open(WATCHLIST_FILE, 'r') as f:
            watchlist = json.load(f)
        
        if not watchlist['stocks']:
            return "Your watchlist is empty. Use add_to_watchlist to add stocks."
        
        result = ["Your Watchlist:"]
        for i, stock in enumerate(watchlist['stocks'], 1):
            result.append(f"{i}. {stock['name']} ({stock['code']})")
            
        return "\n".join(result)
        
    except Exception as e:
        return f"Error reading watchlist: {str(e)}"