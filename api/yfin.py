from fastapi import APIRouter, HTTPException
from services import yfin as yfin_service

router = APIRouter(tags=["yfin"], prefix="/api/yfin")

# ------------------------------
# Current Price
# ------------------------------
@router.get("/stock/{symbol}/price", operation_id="get_stock_current_price")
async def get_stock_current_price(symbol: str) -> dict:
    return await yfin_service.get_stock_current_price(symbol)

# ------------------------------
# Historical Prices
# ------------------------------
@router.get("/stock/{symbol}/history", operation_id="get_stock_historical_prices")
async def get_stock_historical_prices(symbol: str, period: str = "1mo", interval: str = "1d") -> dict:
    return await yfin_service.get_stock_historical_prices(symbol, period, interval)

# ------------------------------
# Stock Info / Metadata
# ------------------------------
@router.get("/stock/{symbol}/info", operation_id="get_stock_info")
async def get_stock_info(symbol: str) -> dict:
    return await yfin_service.get_stock_info(symbol)

# ------------------------------
# Dividends
# ------------------------------
@router.get("/stock/{symbol}/dividends", operation_id="get_stock_dividends")
async def get_stock_dividends(symbol: str) -> dict:
    return await yfin_service.get_stock_dividends(symbol)
# ------------------------------
# Splits
# ------------------------------
@router.get("/stock/{symbol}/splits", operation_id="get_stock_splits")
async def get_stock_splits(symbol: str) -> dict:
    return await yfin_service.get_stock_splits(symbol)

# ------------------------------
# Financials (Income Statement, Balance Sheet, Cashflow)
# ------------------------------
@router.get("/stock/{symbol}/financials", operation_id="get_stock_financials")
async def get_stock_financials(symbol: str) -> dict:
    return await yfin_service.get_stock_financials(symbol)

# ------------------------------
# Analyst Recommendations
# ------------------------------
@router.get("/stock/{symbol}/recommendations", operation_id="get_stock_recommendations")
async def get_stock_recommendations(symbol: str) -> dict:
    return await yfin_service.get_stock_recommendations(symbol)

# ------------------------------
# News
# ------------------------------
@router.get("/stock/{symbol}/news", operation_id="get_stock_news")
async def get_stock_news(symbol: str) -> dict:
    return await yfin_service.get_stock_news(symbol)