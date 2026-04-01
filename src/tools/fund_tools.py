from langchain_community.tools import BaseTool
from src.api.akshare_api import get_fund_info

class FundInfoTool(BaseTool):
    name: str = "fund_info_lookup"
    description: str = "Useful for fetching net value trends for a specific fund. Input should be the fund code (e.g., 005827)."

    def _run(self, symbol: str):
        data = get_fund_info(symbol)
        # Return only the last few records to avoid context overflow
        return str(data[-5:]) 