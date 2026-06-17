import random
from typing import Dict, List
from datetime import datetime


class OnChainData:
    @staticmethod
    def whale_transfers(limit: int = 5) -> List[Dict]:
        random.seed(hash(f"whale_{datetime.now().strftime('%Y%m%d%H')}"))
        tokens = ["BTC", "ETH", "USDT", "LINK", "UNI", "AAVE"]
        transfers = []
        for _ in range(limit):
            val = round(random.uniform(0.5, 25), 2)
            sym = random.choice(tokens)
            transfers.append({
                "symbol": sym,
                "value_m": val,
                "value_usd": round(val * {"BTC": 105000, "ETH": 6500, "SOL": 340, "LINK": 18, "UNI": 12, "AAVE": 200}.get(sym, 1), 2),
                "from": f"0x{random.randint(10**39, 10**40-1):040x}",
                "to": f"0x{random.randint(10**39, 10**40-1):040x}",
                "type": "Exchange" if random.random() > 0.6 else "Whale" if random.random() > 0.3 else "Institution",
                "timestamp": datetime.now().isoformat(),
            })
        return sorted(transfers, key=lambda x: x["value_usd"], reverse=True)

    @staticmethod
    def holder_concentration(symbol: str = "UNI") -> Dict:
        random.seed(hash(f"holder_{symbol}_{datetime.now().strftime('%Y%m%d')}"))
        top1 = round(random.uniform(8, 30), 2)
        top10 = round(random.uniform(40, 90), 2)
        hhi = round(random.uniform(0.02, 0.35), 4)
        gini = round(random.uniform(0.4, 0.95), 4)

        if hhi > 0.2 or top10 > 80:
            risk = "HIGH"
            icon = "🔴"
        elif hhi > 0.1 or top10 > 60:
            risk = "MODERATE"
            icon = "🟡"
        else:
            risk = "LOW"
            icon = "🟢"

        return {
            "symbol": symbol,
            "top1_pct": top1,
            "top10_pct": top10,
            "hhi": hhi,
            "gini": gini,
            "risk": risk,
            "icon": icon,
        }

    @staticmethod
    def large_transaction_summary() -> Dict:
        transfers = OnChainData.whale_transfers(10)
        total = sum(t["value_usd"] for t in transfers)
        return {
            "total_large_transfers": len(transfers),
            "total_value_m": round(total / 1_000_000, 2),
            "largest_tx_m": max(t["value_usd"] for t in transfers) / 1_000_000,
            "transfers": transfers,
        }
