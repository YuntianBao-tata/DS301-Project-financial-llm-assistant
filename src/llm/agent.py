# src/llm/agent.py
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Import Tools
from src.tools.calc_tools import calculate_expression
from src.tools.stock_tools import (
    query_stock_price, query_stock_valuation,
    fetch_stock_history_data, fetch_fund_history_data
)
from src.tools.chart_tools import generate_price_chart
from src.tools.validation_tools import validate_stock_code, validate_fund_code

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

    tools = [
        calculate_expression,
        validate_stock_code,
        validate_fund_code,
        query_stock_price,
        query_stock_valuation,
        fetch_stock_history_data,
        fetch_fund_history_data,
        generate_price_chart
    ]

    system_message = """You are a Senior Financial Analyst AI.
    1. VISUAL INPUT: If the user provides an image (e.g., a chart), analyze it first. Identify the trend or pattern.
    2. DATA ACCURACY: Do NOT rely solely on the image for specific numbers (prices/PE) as images may be outdated. Use tools to verify current data if the user asks for specific metrics.
    3. CHARTING: For 'trends' or 'last N days', use 'fetch_stock_history_data' and 'generate_price_chart'.
    4. TOOLS: Always validate codes before querying."""

    # We use a specific placeholder name 'chat_history'
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