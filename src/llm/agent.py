import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

from src.tools.calc_tools import calculate_expression
from src.tools.stock_tools import (
    query_stock_price,
    query_stock_profile,
    query_market_news,
    query_macro_data
)

load_dotenv(dotenv_path='api_keys.env')

def create_agent():
    # 1. Initialize Qwen
    llm = ChatTongyi(
        model="qwen-plus", # Updated parameter name from model_name to model
        temperature=0.3,
        api_key=os.getenv("DASHSCOPE_API_KEY") # Updated parameter name
    )

    # 2. Define Tools
    tools = [
        calculate_expression,
        query_stock_price,
        query_stock_profile,
        query_market_news,
        query_macro_data
    ]

    # 3. Define Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful financial assistant. Use tools to answer questions about stocks and markets."),
        MessagesPlaceholder("chat_history", optional=True), # Optional history placeholder
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # 4. Create Agent & Executor
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor