from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from typing import Optional
from app.services.yfin import (
    get_stock_current_price,
    get_stock_historical_prices,
    get_stock_info,
    get_stock_dividends,
    get_stock_splits,
    get_stock_financials,
    get_stock_recommendations,
    get_stock_news,
)
from app.llm.gemini import gemini_client

mcp = FastMCP("Stock MCP Server")

class SymbolRequest(BaseModel):
    symbol: str

class HistoricalRequest(BaseModel):
    symbol: str
    period: Optional[str] = "1mo"
    interval: Optional[str] = "1d"


@mcp.tool("get_stock_current_price", description="Fetch the latest stock price for a symbol")
async def tool_current_price(req: SymbolRequest):
    return await get_stock_current_price(req.symbol)

@mcp.tool("get_stock_historical_prices", description="Fetch historical prices for a symbol")
async def tool_historical(req: HistoricalRequest):
    return await get_stock_historical_prices(req.symbol, req.period, req.interval)

@mcp.tool("get_stock_info", description="Fetch metadata/info about a stock")
async def tool_info(req: SymbolRequest):
    return await get_stock_info(req.symbol)

@mcp.tool("get_stock_dividends", description="Fetch dividend history of a stock")
async def tool_dividends(req: SymbolRequest):
    return await get_stock_dividends(req.symbol)

@mcp.tool("get_stock_splits", description="Fetch stock split history")
async def tool_splits(req: SymbolRequest):
    return await get_stock_splits(req.symbol)

@mcp.tool("get_stock_financials", description="Fetch financial statements of a stock")
async def tool_financials(req: SymbolRequest):
    return await get_stock_financials(req.symbol)

@mcp.tool("get_stock_recommendations", description="Fetch analyst recommendations for a stock")
async def tool_recommendations(req: SymbolRequest):
    return await get_stock_recommendations(req.symbol)

@mcp.tool("get_stock_news", description="Fetch recent news articles for a stock")
async def tool_news(req: SymbolRequest):
    print(req)
    return await get_stock_news(req.symbol)


# planner.py
import re

async def stock_planner(query: str):
    """
    A rule-based MCP planner for stock-related queries.
    Maps natural language to the correct tool + arguments.
    """

    query_lower = query.lower()

    # ------------------------------
    # Extract stock symbol (heuristic: look for uppercase ticker)
    # ------------------------------
    match = re.search(r"\b[A-Z]{1,10}\b", query)
    symbol = match.group(0) if match else "AAPL"  # default fallback
    symbol = f"{symbol.upper()}.NS" # assuming NSE stocks for this example
    
    # ------------------------------
    # Historical Prices
    # ------------------------------
    if any(word in query_lower for word in ["history", "past", "trend"]):
        period = "1mo"
        if "week" in query_lower:
            period = "5d"
        elif "month" in query_lower:
            period = "1mo"
        elif "year" in query_lower:
            period = "1y"

        interval = "1d"
        if "hour" in query_lower:
            interval = "1h"
        elif "minute" in query_lower:
            interval = "15m"

        return {"tool": "get_stock_historical_prices", "args": {"symbol": symbol, "period": period, "interval": interval}}

    # ------------------------------
    # Current Price
    # ------------------------------
    if any(word in query_lower for word in ["current price","price", "live price", "now"]):
        return {"tool": "get_stock_current_price", "args": {"symbol": symbol}}

    # ------------------------------
    # Stock Info
    # ------------------------------
    if any(word in query_lower for word in ["info", "details", "metadata"]):
        return {"tool": "get_stock_info", "args": {"symbol": symbol}}

    # ------------------------------
    # Dividends
    # ------------------------------
    if any(word in query_lower for word in ["dividend", "payout"]):
        return {"tool": "get_stock_dividends", "args": {"symbol": symbol}}

    # ------------------------------
    # Splits
    # ------------------------------
    if "split" in query_lower:
        return {"tool": "get_stock_splits", "args": {"symbol": symbol}}

    # ------------------------------
    # Financials
    # ------------------------------
    if any(word in query_lower for word in ["financial", "income", "balance"]):
        return {"tool": "get_stock_financials", "args": {"symbol": symbol}}

    # ------------------------------
    # Analyst Recommendations
    # ------------------------------
    if any(word in query_lower for word in ["recommendation", "analyst", "rating"]):
        return {"tool": "get_stock_recommendations", "args": {"symbol": symbol}}

    # ------------------------------
    # News
    # ------------------------------
    if any(word in query_lower for word in ["news", "article", "headline"]):
        return {"tool": "get_stock_news", "args": {"symbol": symbol}}

    # ------------------------------
    # Fallback
    # ------------------------------
    return {"message": "❌ Sorry, I couldn’t map your request to any stock tool. Try asking about price, history, news, dividends, splits, financials, or recommendations."}


from fastapi import APIRouter, HTTPException

router = APIRouter()

# Step 2: dispatch to the right MCP tool
tool_map = {
    "get_stock_current_price": (tool_current_price, SymbolRequest),
    "get_stock_historical_prices": (tool_historical, HistoricalRequest),
    "get_stock_info": (tool_info, SymbolRequest),
    "get_stock_dividends": (tool_dividends, SymbolRequest),
    "get_stock_splits": (tool_splits, SymbolRequest),
    "get_stock_financials": (tool_financials, SymbolRequest),
    "get_stock_recommendations": (tool_recommendations, SymbolRequest),
    "get_stock_news": (tool_news, SymbolRequest),
}


@router.post("/planner")
async def plan(req: str):
    res = await stock_planner(req)
    tool = res.get("tool")
    args = res.get("args")

    if not tool:
        return res  # fallback message from planner

    if tool not in tool_map:
        raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

    tool_fn, model = tool_map[tool]

    try:
        # ✅ Convert to correct Pydantic request
        req_obj = model(**args)

        # ✅ Run MCP tool (fetch data from yfinance service)
        result = await tool_fn(req_obj)

        # ✅ Ensure result is JSON-safe before passing to Gemini
        import json
        structured_result = json.dumps(result, indent=2, ensure_ascii=False)

        # ✅ Summarize using Gemini (ask for markdown output)
        prompt = f"""
        Summarize the following stock data into a clear, well-structured **Markdown report**.
        Use headings (###), bullet points, and highlight key insights.

        Stock Query: "{req}"
        Tool: {tool}

        Raw Data:
        {structured_result}
        """

        summary = await gemini_client.stock_summarizer(prompt)

        return summary

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
