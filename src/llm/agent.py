# src/llm/agent.py
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Import all tools
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
from src.tools.sector_tools import get_sector_stocks, compare_stocks
from src.tools.history_tools import analyze_historical_performance
from src.tools.watchlist_tools import add_to_watchlist, remove_from_watchlist, list_watchlist
from src.tools.reasoning_tools import break_down_question
from src.tools.news_tools import ingest_financial_news, search_market_sentiment
from datetime import date

# get date time
today_string = date.today().strftime('%Y-%m-%d')

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
        generate_price_chart,
        analyze_stock_technicals,
        get_sector_stocks,
        compare_stocks,
        analyze_historical_performance,
        add_to_watchlist,
        remove_from_watchlist,
        list_watchlist,
        break_down_question,
        ingest_financial_news,
        search_market_sentiment
    ]

    
    
    system_message = """You are a Senior Financial Analyst AI. 
    **CURRENT CONTEXT:** Today is """ + today_string + """

    **NEW CAPABILITY - NEWS & SENTIMENT:**
    - You have access to an internal Knowledge Base containing financial reports and news.
    - If a user asks about "Why did X drop?", "News about Y", or "Market sentiment", use `search_market_sentiment`.
    - If the user provides a file to analyze, use `ingest_financial_news` first.

    **REASONING PROCESS:**
    1. Check if the question requires numerical data (Price/PE) -> Use Stock Tools.
    2. Check if the question requires qualitative context (News/Reasons) -> Use Search Market Sentiment.
    3. Combine both if necessary (e.g., "Stock dropped 5%, why?").

**EXAMPLES OF HOW TO HANDLE COMPLEX QUERIES:**

*   **User Query:** "Compare Moutai and Wuliangye in 2025."
    *   **Your Logic:** "2025 is last year. I can analyze this."
    *   **Action 1:** `analyze_historical_performance(ts_code='600519.SH', start_date='20250101', end_date='20251231')`
    *   **Action 2:** `analyze_historical_performance(ts_code='000858.SZ', start_date='20250101', end_date='20251231')`
    *   **Final Answer:** Compare the returns found in the tool outputs.

*   **User Query:** "What is the price of Moutai?"
    *   **Your Logic:** "User wants current market price."
    *   **Action:** `query_stock_price(ts_code='600519.SH')`

**CAPABILITIES:**
- **VISUAL INPUT:** Analyze images first if provided.
- **DATA ACCURACY:** Use tools for numbers, never guess.
- **CHARTING:** Use 'fetch_stock_history_data' + 'generate_price_chart'.
- **TECHNICALS:** Use 'analyze_stock_technicals'.
- **SECTOR ANALYSIS:** Use 'get_sector_stocks' or 'compare_stocks'.
- **HISTORICAL:** Use 'analyze_historical_performance' for date-specific queries.
- **WATCHLIST:** Users can manage stocks with watchlist tools.

**RESPONSE STYLE:**
- Be concise but thorough.
- Offer follow-up suggestions."""

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
        handle_parsing_errors=True,
        max_iterations=5
    )
    return agent_executor