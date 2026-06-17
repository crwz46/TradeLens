from typing import Dict, List
from datetime import datetime

from .futures import FuturesData
from .market import MarketData


class SentimentEngine:
    def __init__(self, market: MarketData = None):
        self.market = market or MarketData()

    def score(self) -> Dict:
        fng = self.market.fear_greed()
        futures = FuturesData.aggregated("BTC")

        fear_greed_score = fng.get("value", 50) * 0.30

        funding = futures["funding"]
        fr = funding.get("funding_rate", 0)
        if fr > 0.05:
            funding_score = 80
        elif fr > 0.01:
            funding_score = 60
        elif fr > -0.01:
            funding_score = 40
        else:
            funding_score = 20
        funding_score_weighted = funding_score * 0.25

        oi = futures["open_interest"]
        oi_change = oi.get("change_24h_pct", 0)
        if oi_change > 5:
            oi_score = 70
        elif oi_change > 0:
            oi_score = 55
        elif oi_change > -5:
            oi_score = 40
        else:
            oi_score = 25
        oi_score_weighted = oi_score * 0.20

        ls = futures["long_short"]
        ls_ratio = ls.get("ratio", 1)
        if ls_ratio > 1.5:
            ls_score = 75
        elif ls_ratio > 1.0:
            ls_score = 55
        elif ls_ratio > 0.7:
            ls_score = 40
        else:
            ls_score = 20
        ls_score_weighted = ls_score * 0.25

        total = round(fear_greed_score + funding_score_weighted + oi_score_weighted + ls_score_weighted, 1)

        if total >= 70:
            status = "BULLISH"
            icon = "🟢"
        elif total >= 50:
            status = "NEUTRAL"
            icon = "🟡"
        elif total >= 30:
            status = "BEARISH"
            icon = "🟠"
        else:
            status = "EXTREME FEAR"
            icon = "🔴"

        return {
            "total_score": total,
            "max_score": 100,
            "status": status,
            "icon": icon,
            "components": {
                "fear_greed": {"raw": fng.get("value", 50), "score": round(fear_greed_score, 1), "weight": "30%"},
                "funding_rate": {"raw": funding.get("funding_rate", 0), "score": round(funding_score_weighted, 1), "weight": "25%"},
                "open_interest": {"raw": oi.get("change_24h_pct", 0), "score": round(oi_score_weighted, 1), "weight": "20%"},
                "long_short": {"raw": ls.get("ratio", 1), "score": round(ls_score_weighted, 1), "weight": "25%"},
            },
            "timestamp": datetime.now().isoformat(),
        }
