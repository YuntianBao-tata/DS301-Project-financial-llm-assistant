# src/tools/news_tools.py
from langchain_core.tools import tool
from src.tools.rag_manager import kb_manager

@tool
def ingest_financial_news(file_path: str, source_name: str) -> str:
    """
    Adds a financial report or news file to the system's memory.
    Input: file_path (local path to .txt or .pdf), source_name (e.g., 'Bloomberg', 'Tesla_Q3_Report').
    """
    return kb_manager.add_document(file_path, source_name)

@tool
def search_market_sentiment(topic: str) -> str:
    """
    Searches internal knowledge base for recent news or reports regarding a specific topic.
    Use this to find reasons behind price movements (e.g., "Moutai regulatory news").
    Input: topic (search query).
    """
    return kb_manager.search_news(topic)