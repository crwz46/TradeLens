import json
import os
from typing import Dict, List, Optional
from datetime import datetime


HOLDINGS_FILE = "portfolio_holdings.json"


class Portfolio:
    def __init__(self, holdings: Dict[str, float] = None):
        self.holdings = holdings or {}
        self.cost_basis: Dict[str, float] = {}

    def set_holding(self, symbol: str, amount: float, cost_price: float = 0):
        self.holdings[symbol.upper()] = amount
        if cost_price > 0:
            self.cost_basis[symbol.upper()] = cost_price

    def remove_holding(self, symbol: str):
        self.holdings.pop(symbol.upper(), None)
        self.cost_basis.pop(symbol.upper(), None)

    def value(self, prices: Dict[str, float]) -> Dict[str, float]:
        values = {}
        for sym, amt in self.holdings.items():
            price = prices.get(sym.upper(), 0)
            values[sym] = round(amt * price, 2)
        return values

    def total_value(self, prices: Dict[str, float]) -> float:
        return round(sum(self.value(prices).values()), 2)

    def allocation(self, prices: Dict[str, float]) -> List[Dict]:
        total = self.total_value(prices)
        if total == 0:
            return []
        alloc = []
        for sym, amt in self.holdings.items():
            val = prices.get(sym.upper(), 0) * amt
            alloc.append({
                "symbol": sym,
                "amount": amt,
                "value_usd": round(val, 2),
                "pct": round((val / total) * 100, 1),
            })
        return sorted(alloc, key=lambda x: x["value_usd"], reverse=True)

    def pnl(self, prices: Dict[str, float]) -> Dict:
        total_cost = 0
        total_value = 0
        details = []
        for sym, amt in self.holdings.items():
            price = prices.get(sym.upper(), 0)
            current_val = amt * price
            cost = self.cost_basis.get(sym.upper(), 0)
            cost_total = amt * cost
            pnl = current_val - cost_total
            pnl_pct = ((price - cost) / cost * 100) if cost > 0 else 0
            total_cost += cost_total
            total_value += current_val
            details.append({
                "symbol": sym,
                "amount": amt,
                "cost_price": cost,
                "current_price": price,
                "value_usd": round(current_val, 2),
                "pnl_usd": round(pnl, 2),
                "pnl_pct": round(pnl_pct, 1),
            })
        return {
            "total_cost": round(total_cost, 2),
            "total_value": round(total_value, 2),
            "total_pnl": round(total_value - total_cost, 2),
            "total_pnl_pct": round(((total_value - total_cost) / total_cost) * 100, 1) if total_cost > 0 else 0,
            "details": details,
        }

    def save(self, path: str = HOLDINGS_FILE):
        with open(path, "w") as f:
            json.dump({"holdings": self.holdings, "cost_basis": self.cost_basis}, f)

    @classmethod
    def load(cls, path: str = HOLDINGS_FILE) -> "Portfolio":
        if not os.path.exists(path):
            return cls()
        with open(path) as f:
            data = json.load(f)
        p = cls(data.get("holdings", {}))
        p.cost_basis = data.get("cost_basis", {})
        return p
