import random
from typing import Dict, List
from datetime import datetime


class FuturesData:
    @staticmethod
    def funding_rate(symbol: str = "BTC") -> Dict:
        random.seed(hash(f"funding_{symbol}_{datetime.now().strftime('%Y%m%d%H')}"))
        rate = round(random.uniform(-0.05, 0.08), 3)
        return {
            "symbol": symbol,
            "funding_rate": rate,
            "annualized": round(rate * 3 * 365, 2),
            "timestamp": datetime.now().isoformat(),
            "status": "Overheated" if rate > 0.05 else "Normal" if rate > -0.02 else "Cooling",
        }

    @staticmethod
    def open_interest(symbol: str = "BTC") -> Dict:
        random.seed(hash(f"oi_{symbol}_{datetime.now().strftime('%Y%m%d')}"))
        base = {"BTC": 42, "ETH": 18, "SOL": 5}
        oi = round(base.get(symbol, 10) + random.uniform(-5, 5), 1)
        change = round(random.uniform(-8, 12), 1)
        return {
            "symbol": symbol,
            "open_interest_b": oi,
            "change_24h_pct": change,
            "timestamp": datetime.now().isoformat(),
        }

    @staticmethod
    def long_short_ratio(symbol: str = "BTC") -> Dict:
        random.seed(hash(f"ls_{symbol}_{datetime.now().strftime('%Y%m%d%H')}"))
        ratio = round(random.uniform(0.5, 3.5), 2)
        long_pct = round((ratio / (ratio + 1)) * 100, 1)
        short_pct = round(100 - long_pct, 1)
        return {
            "symbol": symbol,
            "ratio": ratio,
            "long_pct": long_pct,
            "short_pct": short_pct,
            "bias": "Long" if ratio > 1.2 else "Short" if ratio < 0.8 else "Neutral",
        }

    @staticmethod
    def aggregated(symbol: str = "BTC") -> Dict:
        return {
            "funding": FuturesData.funding_rate(symbol),
            "open_interest": FuturesData.open_interest(symbol),
            "long_short": FuturesData.long_short_ratio(symbol),
        }

    @staticmethod
    def all_symbols() -> List[Dict]:
        return [FuturesData.aggregated(s) for s in ["BTC", "ETH", "SOL"]]
