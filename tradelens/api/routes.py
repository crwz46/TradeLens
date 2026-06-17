from fastapi import APIRouter, Query
from typing import Optional

from ..analytics.market import MarketData
from ..analytics.futures import FuturesData
from ..analytics.liquidations import LiquidationData
from ..analytics.sentiment import SentimentEngine
from ..analytics.onchain import OnChainData
from ..portfolio.tracker import Portfolio
from ..risk.metrics import RiskMetrics
from ..signals.conditions import MarketConditions

router = APIRouter()
market = MarketData()


@router.get("/")
async def root():
    return {
        "service": "TradeLens",
        "version": "1.0.0",
        "modules": [
            "market_overview", "futures_analytics", "liquidation_monitor",
            "sentiment_engine", "portfolio_tracker", "risk_engine",
            "onchain_intelligence", "trading_signals",
        ],
        "docs": "/docs",
    }


@router.get("/market/overview")
async def market_overview():
    return market.overview()


@router.get("/market/prices")
async def prices():
    return market.prices()


@router.get("/market/fear-greed")
async def fear_greed():
    return market.fear_greed()


@router.get("/market/chart/{coin}")
async def market_chart(coin: str = "bitcoin", days: int = 7):
    return market.market_chart(coin, days)


@router.get("/futures/{symbol}")
async def futures(symbol: str = "BTC"):
    return FuturesData.aggregated(symbol.upper())


@router.get("/futures/all")
async def futures_all():
    return FuturesData.all_symbols()


@router.get("/liquidations/summary")
async def liquidations_summary():
    return LiquidationData.summary()


@router.get("/liquidations/heatmap")
async def liquidations_heatmap(hours: int = 24):
    return LiquidationData.heatmap_data(hours)


@router.get("/liquidations/top")
async def liquidations_top(limit: int = 10):
    return LiquidationData.top_liquidations(limit)


@router.get("/sentiment")
async def sentiment():
    engine = SentimentEngine(market)
    return engine.score()


@router.get("/onchain/whales")
async def onchain_whales(limit: int = 5):
    return OnChainData.whale_transfers(limit)


@router.get("/onchain/holders/{symbol}")
async def onchain_holders(symbol: str = "UNI"):
    return OnChainData.holder_concentration(symbol.upper())


@router.get("/portfolio/value")
async def portfolio_value():
    p = Portfolio.load()
    prices = market.prices()
    return {
        "holdings": p.holdings,
        "total_value": p.total_value(prices),
        "allocation": p.allocation(prices),
        "pnl": p.pnl(prices),
    }


@router.get("/risk")
async def risk(annual_vol: float = 0.5, drift: float = 0.0005):
    return RiskMetrics.calculate(annual_vol, drift)


@router.get("/signals")
async def signals():
    conditions = MarketConditions(market)
    return conditions.analyze()


@router.get("/health")
async def health():
    return {"status": "ok", "modules": 8, "live_data": True}
