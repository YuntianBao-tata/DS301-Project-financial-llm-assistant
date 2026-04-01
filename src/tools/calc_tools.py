from langchain_core.tools import tool

@tool
def calculate_expression(expression: str) -> str:
    """Useful for math calculations. Input: math expression string (e.g. '2 + 2')."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {str(e)}"