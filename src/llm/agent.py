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

def create_agent():
    try:
        llm = ChatTongyi(
            model="qwen-plus",
            temperature=0.3,
            api_key=os.getenv("DASHSCOPE_API_KEY")
        )
    except Exception as e:
        print(f"LLM Init Error: {e}")
        return None

    tools = [
        calculate_expression,
        validate_stock_code, validate_fund_code,
        query_stock_price, query_stock_valuation,
        fetch_stock_history_data, fetch_fund_history_data,
        generate_price_chart
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Senior Financial Analyst.
        1. For 'trends', 'charts', or 'last N days': 
           - Use 'fetch_stock_history_data' or 'fetch_fund_history_data' first.
           - Then use 'generate_price_chart' to visualize.
        2. For specific metrics (PE, PB), use the specific tools.
        3. Always validate codes before use."""),
        MessagesPlaceholder("chat_history"),
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