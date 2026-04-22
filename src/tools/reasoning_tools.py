# src/tools/reasoning_tools.py
from langchain_core.tools import tool

@tool
def break_down_question(question: str) -> str:
    """
    Break down a complex financial question into smaller, answerable steps.
    Use this when the user asks something multi-part or ambiguous.
    Input: The original question
    Returns: A structured breakdown of sub-questions to answer.
    """
    q_lower = question.lower()
    steps = []
    
    # Check for comparison keywords
    if any(word in q_lower for word in ['compare', 'vs', 'versus', 'which one']):
        # Check if it's about historical performance
        if any(word in q_lower for word in ['perform', 'performance', 'better', 'worse', '2022', '2023', 'year']):
            steps.append("1. Identify the two assets being compared (e.g., Moutai and Wuliangye).")
            steps.append("2. Determine the time period for the comparison (e.g., 'in 2022' means Jan 1 to Dec 31).")
            steps.append("3. Call 'analyze_historical_performance' for the first asset.")
            steps.append("4. Call 'analyze_historical_performance' for the second asset.")
            steps.append("5. Compare the 'Total Return' from both results to determine which performed better.")
        else:
            # It's likely a valuation comparison
            steps.append("1. Identify the assets being compared.")
            steps.append("2. Call 'compare_stocks' to get their current valuation metrics (PE, PB, etc.).")
            steps.append("3. Present the comparison table to the user.")
            
    # Check for single-asset historical performance
    elif any(word in q_lower for word in ['performance', 'perform', 'trend']) and not any(word in q_lower for word in ['compare', 'vs']):
         steps.append("1. Identify the asset and the time period mentioned.")
         steps.append("2. Call 'analyze_historical_performance' with the correct dates.")
         steps.append("3. Summarize the key metrics: Total Return, Volatility, and Max Drawdown.")
         
    # Default fallback for other questions
    else:
        steps.append("1. Identify the core question and the main subject (e.g., a stock).")
        steps.append("2. Determine the most relevant tool to answer it (e.g., 'query_stock_price', 'analyze_stock_technicals').")
        steps.append("3. Execute the tool and present the findings clearly.")
    
    return f"Reasoning Steps:\n" + "\n".join(steps)