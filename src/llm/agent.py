# src/llm/agent.py
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Import existing tools
from src.tools.calc_tools import calculate_expression
from src.tools.stock_tools import (
    query_stock_price,
    query_stock_valuation,
    fetch_stock_history_data,
    fetch_fund_history_data
)
from src.tools.chart_tools import generate_price_chart
from src.tools.validation_tools import validate_stock_code, validate_fund_code
from src.tools.technical_tools import analyze_stock_technicals

# --- IMPORT NEW SECTOR TOOLS ---
from src.tools.sector_tools import get_sector_stocks, compare_stocks

load_dotenv(dotenv_path='api_keys.env')

def create_agent(model_name: str = "qwen-plus"):
    try:
        llm = ChatTongyi(
            model=model_name,
            temperature=0.3,
            api_key=os.getenv("DASHSCOPE_API_KEY")
        )
    except Exception as e:
        print(f"LLM Init Error: {e}")
        return None

    # --- ADD NEW TOOLS TO LIST ---
    tools = [
        calculate_expression,
        validate_stock_code,
        validate_fund_code,
        query_stock_price,
        query_stock_valuation,
        fetch_stock_history_data,
        fetch_fund_history_data,
        generate_price_chart,
        analyze_stock_technicals,
        get_sector_stocks,      # Added here
        compare_stocks          # Added here
    ]

    system_message = """You are a Senior Financial Analyst AI.
    1. VISUAL INPUT: If the user provides an image (e.g., a chart), analyze it first.
    2. DATA ACCURACY: Do NOT rely solely on the image for specific numbers. Use tools.
    3. CHARTING: For 'trends', use 'fetch_stock_history_data' and 'generate_price_chart'.
    4. TECHNICALS: If the user asks about 'overbought', 'oversold', or 'RSI', use 'analyze_stock_technicals'.
    5. SECTOR ANALYSIS: If the user asks about an industry or wants to compare stocks, use 'get_sector_stocks' or 'compare_stocks'.
    6. TOOLS: Always validate codes before querying."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    return agent_executor