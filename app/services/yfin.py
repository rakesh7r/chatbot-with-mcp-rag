from fastapi import APIRouter, HTTPException
import yfinance as yf


async def get_stock_current_price(symbol: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        current_price = ticker.info.get("currentPrice")
        if current_price:
            return {"symbol": symbol, "current_price": current_price}
        raise HTTPException(status_code=404, detail="Current price not available for this symbol.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock price: {e}")


# ------------------------------
# Historical Prices
# ------------------------------
async def get_stock_historical_prices(symbol: str, period: str = "1mo", interval: str = "1d") -> dict:
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        if not hist.empty:
            hist.index = hist.index.astype(str)
            return {"symbol": symbol, "historical_prices": hist.to_dict(orient="records")}
        raise HTTPException(status_code=404, detail="Historical data not available for this symbol or period.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching historical data: {e}")


# ------------------------------
# Stock Info / Metadata
# ------------------------------
async def get_stock_info(symbol: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        if info:
            return {"symbol": symbol, "info": info}
        raise HTTPException(status_code=404, detail="Info not available for this symbol.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock info: {e}")


# ------------------------------
# Dividends
# ------------------------------
async def get_stock_dividends(symbol: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        dividends = ticker.dividends
        if not dividends.empty:
            return {"symbol": symbol, "dividends": dividends.to_dict()}
        raise HTTPException(status_code=404, detail="Dividends not available for this symbol.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dividends: {e}")


# ------------------------------
# Splits
# ------------------------------
async def get_stock_splits(symbol: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        splits = ticker.splits
        if not splits.empty:
            return {"symbol": symbol, "splits": splits.to_dict()}
        raise HTTPException(status_code=404, detail="Splits not available for this symbol.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching splits: {e}")


# ------------------------------
# Financials (Income Statement, Balance Sheet, Cashflow)
# ------------------------------
async def get_stock_financials(symbol: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        return {
            "symbol": symbol,
            "financials": {
                "income_statement": ticker.financials.to_dict() if not ticker.financials.empty else {},
                "balance_sheet": ticker.balance_sheet.to_dict() if not ticker.balance_sheet.empty else {},
                "cashflow": ticker.cashflow.to_dict() if not ticker.cashflow.empty else {},
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching financials: {e}")


# ------------------------------
# Analyst Recommendations
# ------------------------------
async def get_stock_recommendations(symbol: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        recs = ticker.recommendations
        if recs is not None and not recs.empty:
            recs.index = recs.index.astype(str)
            return {"symbol": symbol, "recommendations": recs.to_dict(orient="records")}
        raise HTTPException(status_code=404, detail="Recommendations not available for this symbol.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recommendations: {e}")


# ------------------------------
# News
# ------------------------------
async def get_stock_news(symbol: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        news = ticker.news
        if news:
            return {"symbol": symbol, "news": news}
        raise HTTPException(status_code=404, detail="News not available for this symbol.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {e}")
