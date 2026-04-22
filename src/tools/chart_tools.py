# src/tools/chart_tools.py
from langchain_core.tools import tool
import matplotlib.pyplot as plt
import pandas as pd
import json
import base64
from io import BytesIO

@tool
def generate_price_chart(data_json: str, title: str = "Price Trend") -> str:
    """
    Generates a price trend chart from JSON data.
    Use this tool after fetching historical data to visualize the trend.
    Input: data_json (JSON string from fetch_stock_history_data), title (Chart title).
    Returns: A Base64 encoded image string.
    """
    try:
        data = json.loads(data_json)
        
        # --- FIX 1: Check if data list is empty ---
        if not data:
            return "Error: No data provided to generate chart."

        df = pd.DataFrame(data)
        
        # --- FIX 2: Check for required columns ---
        if 'close' not in df.columns:
            return "Error: 'close' price column missing in data."
            
        date_col = None
        if 'trade_date' in df.columns:
            date_col = 'trade_date'
        elif 'date' in df.columns:
            date_col = 'date'
        else:
            return "Error: Date column missing."

        df['date'] = pd.to_datetime(df[date_col])
        df = df.set_index('date').sort_index()

        # --- FIX 3: Ensure we have data points to plot ---
        if len(df) == 0:
            return "Error: No valid data points to plot."

        plt.figure(figsize=(10, 4))
        plt.plot(df.index, df['close'], label='Close Price', color='#1f77b4', linewidth=2)
        plt.title(title, fontsize=14)
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150)
        plt.close()
        buffer.seek(0)
        
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png).decode('utf-8')
        return f"data:image/png;base64,{graphic}"
        
    except json.JSONDecodeError:
        return "Error: Invalid JSON format provided."
    except Exception as e:
        return f"Chart Error: {str(e)}"