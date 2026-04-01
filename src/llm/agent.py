import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

from src.tools.calc_tools import calculate_expression
from src.tools.stock_tools import (
    query_stock_price,
    query_stock_valuation,
    query_company_income,
    query_fund_data,
    query_market_news,
    query_global_market,
    query_technical_analysis
)

load_dotenv(dotenv_path='api_keys.env')

def create_agent():
    # Initialize Qwen
    llm = ChatTongyi(
        model="qwen-plus",
        temperature=0.3,
        api_key=os.getenv("DASHSCOPE_API_KEY")
    )

    # Define Tools
    tools = [
        calculate_expression,
        query_stock_price,
        query_stock_valuation,
        query_company_income,
        query_fund_data,
        query_market_news,
        query_global_market,
        query_technical_analysis
    ]

    # Enhanced System Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior Financial Analyst AI. 
         You have access to real-time market data, fundamental data (PE/PB/Revenue), and technical indicators (RSI).
         1. When asked about a stock, check its price, valuation (PE/PB), and technicals (RSI).
         2. For Funds/ETFs, use the specific fund tool.
         3. Use the calculator for any percentage changes or growth rates.
         4. Provide professional, data-driven insights."""),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor