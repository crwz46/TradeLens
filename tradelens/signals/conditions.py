from typing import Dict

from ..analytics.futures import FuturesData
from ..analytics.market import MarketData
from ..risk.metrics import RiskMetrics


class MarketConditions:
    def __init__(self, market: MarketData = None):
        self.market = market or MarketData()

    def analyze(self) -> Dict:
        futures = FuturesData.aggregated("BTC")
        fng = self.market.fear_greed()

        funding = futures["funding"]
        fr = funding.get("funding_rate", 0)
        if fr > 0.03:
            trend = "Bullish (Overheated)"
            trend_icon = "🔥"
            funding_status = "Overheated"
        elif fr > 0.005:
            trend = "Bullish"
            trend_icon = "📈"
            funding_status = "Elevated"
        elif fr > -0.01:
            trend = "Neutral"
            trend_icon = "➡️"
            funding_status = "Normal"
        else:
            trend = "Bearish"
            trend_icon = "📉"
            funding_status = "Negative"

        fng_val = fng.get("value", 50)
        if fng_val > 70:
            sentiment = "Greed"
            sentiment_icon = "🟢"
        elif fng_val > 40:
            sentiment = "Neutral"
            sentiment_icon = "🟡"
        else:
            sentiment = "Fear"
            sentiment_icon = "🔴"

        oi = futures["open_interest"]
        oi_change = oi.get("change_24h_pct", 0)
        if abs(oi_change) > 8:
            oi_risk = "High"
        elif abs(oi_change) > 3:
            oi_risk = "Medium"
        else:
            oi_risk = "Low"

        ls = futures["long_short"]
        ls_ratio = ls.get("ratio", 1)
        if ls_ratio > 2.0:
            risk = "High (crowded long)"
        elif ls_ratio > 1.3:
            risk = "Medium"
        elif ls_ratio > 0.7:
            risk = "Low"
        else:
            risk = "High (crowded short)"

        return {
            "trend": {"label": trend, "icon": trend_icon},
            "funding_status": funding_status,
            "sentiment": {"label": sentiment, "icon": sentiment_icon, "value": fng_val},
            "open_interest_risk": oi_risk,
            "long_short_risk": risk,
            "composite_risk": "Low" if (oi_risk == "Low" and "Low" in risk and fng_val < 70)
                               else "High" if (oi_risk == "High" or "High" in risk)
                               else "Medium",
        }
