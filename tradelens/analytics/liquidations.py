import random
from typing import Dict, List
from datetime import datetime, timedelta


class LiquidationData:
    @staticmethod
    def _seed(key: str):
        random.seed(hash(f"{key}_{datetime.now().strftime('%Y%m%d%H')}"))

    @staticmethod
    def summary() -> Dict:
        LiquidationData._seed("liq_summary")
        total_long = round(random.uniform(80, 450), 1)
        total_short = round(random.uniform(20, 180), 1)
        return {
            "long_24h_m": total_long,
            "short_24h_m": total_short,
            "total_24h_m": round(total_long + total_short, 1),
            "long_short_ratio": round(total_long / total_short, 2) if total_short > 0 else 0,
            "largest_single_m": round(random.uniform(5, 60), 1),
            "timestamp": datetime.now().isoformat(),
        }

    @staticmethod
    def heatmap_data(hours: int = 24) -> List[Dict]:
        LiquidationData._seed("heatmap")
        now = datetime.now()
        data = []
        for i in range(hours):
            ts = now - timedelta(hours=hours - i)
            long_liq = round(random.uniform(1, 60), 1)
            short_liq = round(random.uniform(0.5, 30), 1)
            data.append({
                "timestamp": ts.isoformat(),
                "hour": ts.strftime("%H:00"),
                "long_liq_m": long_liq,
                "short_liq_m": short_liq,
                "total_liq_m": round(long_liq + short_liq, 1),
            })
        return data

    @staticmethod
    def top_liquidations(limit: int = 10) -> List[Dict]:
        LiquidationData._seed("top_liq")
        symbols = ["BTC", "ETH", "SOL", "LINK", "DOGE", "AVAX", "MATIC", "UNI", "ARB", "OP"]
        top = []
        for sym in symbols[:limit]:
            val = round(random.uniform(0.5, 85), 1)
            side = "Long" if random.random() > 0.4 else "Short"
            top.append({
                "symbol": sym,
                "value_m": val,
                "side": side,
                "price": round(random.uniform(1, 70000), 2),
            })
        return sorted(top, key=lambda x: x["value_m"], reverse=True)
