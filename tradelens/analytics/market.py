import time
from typing import Dict, Optional
from datetime import datetime, timedelta

import requests


class MarketData:
    BASE = "https://api.coingecko.com/api/v3"

    def __init__(self, api_key: str = ""):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "TradeLens/1.0"})
        self.api_key = api_key
        self._cache = {}
        self._cache_ts = {}

    def _get(self, endpoint: str, params: dict = None, ttl: int = 60) -> dict:
        now = time.time()
        cache_key = f"{endpoint}_{params}"
        if cache_key in self._cache and (now - self._cache_ts.get(cache_key, 0)) < ttl:
            return self._cache[cache_key]
        url = f"{self.BASE}/{endpoint}"
        if self.api_key:
            params = params or {}
            params["x_cg_pro_api_key"] = self.api_key
        try:
            resp = self.session.get(url, params=params, timeout=15)
            data = resp.json()
            self._cache[cache_key] = data
            self._cache_ts[cache_key] = now
            return data
        except Exception:
            return {}

    def prices(self) -> Dict[str, float]:
        data = self._get("simple/price", {"ids": "bitcoin,ethereum,solana", "vs_currencies": "usd"}, ttl=30)
        return {
            "BTC": data.get("bitcoin", {}).get("usd", 0),
            "ETH": data.get("ethereum", {}).get("usd", 0),
            "SOL": data.get("solana", {}).get("usd", 0),
        }

    def global_data(self) -> Dict:
        data = self._get("global", ttl=120)
        result = {}
        d = data.get("data", {})
        result["total_market_cap"] = d.get("total_market_cap", {}).get("usd", 0)
        result["btc_dominance"] = d.get("market_cap_percentage", {}).get("btc", 0)
        result["eth_dominance"] = d.get("market_cap_percentage", {}).get("eth", 0)
        result["active_cryptos"] = d.get("active_cryptocurrencies", 0)
        result["volume_24h"] = d.get("total_volume", {}).get("usd", 0)
        return result

    def fear_greed(self) -> Dict:
        try:
            resp = self.session.get("https://api.alternative.me/fng/?limit=1", timeout=10)
            data = resp.json()
            d = data.get("data", [{}])[0]
            return {
                "value": int(d.get("value", 50)),
                "classification": d.get("value_classification", "Neutral"),
                "timestamp": d.get("timestamp", ""),
            }
        except Exception:
            return {"value": 50, "classification": "Neutral", "timestamp": ""}

    def ohlc(self, coin: str = "bitcoin", days: int = 30) -> list:
        data = self._get(f"coins/{coin}/ohlc", {"vs_currency": "usd", "days": days}, ttl=300)
        return data if isinstance(data, list) else []

    def market_chart(self, coin: str = "bitcoin", days: int = 7) -> Dict:
        data = self._get(f"coins/{coin}/market_chart", {"vs_currency": "usd", "days": days}, ttl=120)
        return data if isinstance(data, dict) else {}

    def overview(self) -> Dict:
        prices = self.prices()
        global_d = self.global_data()
        fng = self.fear_greed()
        return {
            "prices": prices,
            "market_cap": global_d.get("total_market_cap", 0),
            "btc_dominance": global_d.get("btc_dominance", 0),
            "volume_24h": global_d.get("volume_24h", 0),
            "active_cryptos": global_d.get("active_cryptos", 0),
            "fear_greed": fng,
            "updated_at": datetime.now().isoformat(),
        }
