import pytest
import requests
import os
from src.api.tushare_api import get_stock_daily
from src.api.akshare_api import get_fund_nav

def test_tushare_api():
    df = get_stock_daily("600519.SH", "20240101", "20240131")
    assert not df.empty
    assert "close" in df.columns

def test_akshare_api():
    df = get_fund_nav("005827")
    assert not df.empty
    assert "单位净值" in df.columns

def test_backend_health():
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

if __name__ == "__main__":
    pytest.main()