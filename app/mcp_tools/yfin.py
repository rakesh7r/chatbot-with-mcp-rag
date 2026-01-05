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
    return await get_stock_news(req.symbol)
