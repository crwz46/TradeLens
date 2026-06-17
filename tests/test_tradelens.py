import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from tradelens.analytics.market import MarketData
from tradelens.analytics.futures import FuturesData
from tradelens.analytics.liquidations import LiquidationData
from tradelens.analytics.sentiment import SentimentEngine
from tradelens.analytics.onchain import OnChainData
from tradelens.portfolio.tracker import Portfolio
from tradelens.risk.metrics import RiskMetrics
from tradelens.signals.conditions import MarketConditions
import numpy as np


class TestMarket:
    def test_prices_structure(self):
        m = MarketData()
        p = m.prices()
        assert isinstance(p, dict)
        for sym in ["BTC", "ETH", "SOL"]:
            assert sym in p
            assert isinstance(p[sym], (int, float))

    def test_fear_greed_structure(self):
        m = MarketData()
        f = m.fear_greed()
        assert "value" in f
        assert "classification" in f

    def test_overview_structure(self):
        m = MarketData()
        o = m.overview()
        assert "prices" in o
        assert "market_cap" in o
        assert "btc_dominance" in o


class TestFutures:
    def test_funding_rate(self):
        d = FuturesData.funding_rate("BTC")
        assert d["symbol"] == "BTC"
        assert isinstance(d["funding_rate"], float)

    def test_open_interest(self):
        d = FuturesData.open_interest("ETH")
        assert d["symbol"] == "ETH"
        assert d["open_interest_b"] > 0

    def test_long_short_ratio(self):
        d = FuturesData.long_short_ratio("SOL")
        assert d["symbol"] == "SOL"
        assert 0 < d["ratio"] < 10

    def test_aggregated(self):
        d = FuturesData.aggregated("BTC")
        assert "funding" in d
        assert "open_interest" in d
        assert "long_short" in d

    def test_deterministic(self):
        d1 = FuturesData.funding_rate("BTC")
        d2 = FuturesData.funding_rate("BTC")
        assert d1["funding_rate"] == d2["funding_rate"]


class TestLiquidations:
    def test_summary(self):
        s = LiquidationData.summary()
        assert "long_24h_m" in s
        assert "short_24h_m" in s
        assert s["long_24h_m"] > 0

    def test_heatmap_data(self):
        h = LiquidationData.heatmap_data(6)
        assert len(h) == 6
        assert "hour" in h[0]
        assert "long_liq_m" in h[0]

    def test_top_liquidations(self):
        t = LiquidationData.top_liquidations(3)
        assert len(t) <= 3
        assert t == sorted(t, key=lambda x: x["value_m"], reverse=True)


class TestSentiment:
    def test_score_structure(self):
        s = SentimentEngine()
        r = s.score()
        assert "total_score" in r
        assert "status" in r
        assert "components" in r
        assert 0 <= r["total_score"] <= 100

    def test_components(self):
        s = SentimentEngine()
        r = s.score()
        assert len(r["components"]) == 4


class TestOnChain:
    def test_whale_transfers(self):
        t = OnChainData.whale_transfers(3)
        assert len(t) == 3
        assert "value_m" in t[0]

    def test_holder_concentration(self):
        h = OnChainData.holder_concentration("UNI")
        assert "risk" in h
        assert "hhi" in h
        assert 0 < h["hhi"] < 1


class TestPortfolio:
    def test_empty_portfolio(self):
        p = Portfolio()
        assert p.total_value({"BTC": 50000}) == 0

    def test_single_holding(self):
        p = Portfolio({"BTC": 0.5})
        v = p.value({"BTC": 100000})
        assert v["BTC"] == 50000.0

    def test_total_value(self):
        p = Portfolio({"BTC": 1.0, "ETH": 10.0})
        tv = p.total_value({"BTC": 50000, "ETH": 3000})
        assert tv == 50000 + 30000

    def test_allocation(self):
        p = Portfolio({"BTC": 1.0, "ETH": 10.0})
        a = p.allocation({"BTC": 50000, "ETH": 3000})
        assert len(a) == 2
        assert abs(sum(item["pct"] for item in a) - 100) < 0.1

    def test_pnl(self):
        p = Portfolio({"BTC": 1.0})
        p.cost_basis["BTC"] = 40000
        pnl = p.pnl({"BTC": 50000})
        assert pnl["total_pnl"] == 10000
        assert pnl["total_pnl_pct"] == 25.0

    def test_save_load(self, tmp_path):
        path = tmp_path / "test_portfolio.json"
        p = Portfolio({"BTC": 1.5})
        p.cost_basis["BTC"] = 30000
        p.save(str(path))
        p2 = Portfolio.load(str(path))
        assert p2.holdings["BTC"] == 1.5
        assert p2.cost_basis["BTC"] == 30000


class TestRisk:
    def test_sharpe_ratio(self):
        returns = np.array([0.001] * 252)
        sharpe = RiskMetrics.sharpe_ratio(returns)
        assert sharpe > 0

    def test_sharpe_negative(self):
        returns = np.array([-0.001] * 252)
        sharpe = RiskMetrics.sharpe_ratio(returns)
        assert sharpe < 0

    def test_max_drawdown(self):
        returns = np.array([-0.05, -0.05, -0.05, 0.05, 0.05])
        dd = RiskMetrics.max_drawdown(returns)
        assert dd < 0

    def test_volatility(self):
        returns = np.array([0.01] * 252)
        returns[0] = 0.02
        vol = RiskMetrics.volatility(returns)
        assert vol > 0

    def test_calculate_structure(self):
        r = RiskMetrics.calculate(0.4, 0.0005)
        assert "sharpe_ratio" in r
        assert "volatility_pct" in r
        assert "max_drawdown_pct" in r

    def test_portfolio_risk_score(self):
        r = RiskMetrics.portfolio_risk_score(50000, 3, 1.5, 25)
        assert 0 <= r["score"] <= 100
        assert r["level"] in ["LOW", "MODERATE", "HIGH"]


class TestSignals:
    def test_analyze_structure(self):
        s = MarketConditions()
        r = s.analyze()
        assert "trend" in r
        assert "funding_status" in r
        assert "sentiment" in r
        assert "composite_risk" in r
