import random
from typing import Dict, List
from datetime import datetime, timedelta

import numpy as np


class RiskMetrics:
    @staticmethod
    def _daily_returns(days: int = 365, annual_vol: float = 0.5, drift: float = 0.0005) -> np.ndarray:
        random.seed(42)
        np.random.seed(42)
        daily_vol = annual_vol / np.sqrt(252)
        returns = np.random.normal(drift, daily_vol, days)
        return returns

    @staticmethod
    def sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.05) -> float:
        if len(returns) < 2 or np.std(returns) == 0:
            return 0.0
        daily_rfr = risk_free_rate / 252
        excess = returns - daily_rfr
        annualized_excess = np.mean(excess) * 252
        annualized_vol = np.std(returns) * np.sqrt(252)
        return round(annualized_excess / annualized_vol, 2) if annualized_vol > 0 else 0.0

    @staticmethod
    def max_drawdown(returns: np.ndarray) -> float:
        cumulative = np.cumprod(1 + returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        return round(float(np.min(drawdown)) * 100, 1)

    @staticmethod
    def volatility(returns: np.ndarray) -> float:
        return round(float(np.std(returns) * np.sqrt(252) * 100), 1)

    @staticmethod
    def calculate(annual_vol: float = 0.5, drift: float = 0.0005) -> Dict:
        returns = RiskMetrics._daily_returns(365, annual_vol, drift)
        sharpe = RiskMetrics.sharpe_ratio(returns)
        max_dd = RiskMetrics.max_drawdown(returns)
        vol = RiskMetrics.volatility(returns)

        if sharpe >= 2.0:
            sharpe_label = "Excellent"
        elif sharpe >= 1.0:
            sharpe_label = "Good"
        elif sharpe >= 0.5:
            sharpe_label = "Fair"
        else:
            sharpe_label = "Poor"

        if vol < 30:
            vol_label = "Low"
        elif vol < 60:
            vol_label = "Moderate"
        else:
            vol_label = "High"

        if max_dd > -15:
            dd_label = "Controlled"
        elif max_dd > -30:
            dd_label = "Moderate"
        else:
            dd_label = "Severe"

        return {
            "sharpe_ratio": sharpe,
            "sharpe_label": sharpe_label,
            "volatility_pct": vol,
            "volatility_label": vol_label,
            "max_drawdown_pct": max_dd,
            "max_drawdown_label": dd_label,
            "annualized_return_pct": round(float(np.mean(returns) * 252 * 100), 1),
            "risk_free_rate": 0.05,
        }

    @staticmethod
    def portfolio_risk_score(portfolio_value: float, allocation_count: int,
                             sharpe: float, volatility: float) -> Dict:
        score = 50
        if sharpe > 1.5:
            score += 20
        elif sharpe > 0.5:
            score += 10
        elif sharpe < 0:
            score -= 15

        if volatility < 30:
            score += 15
        elif volatility < 60:
            score += 5
        else:
            score -= 10

        if allocation_count >= 5:
            score += 10
        elif allocation_count >= 3:
            score += 5
        else:
            score -= 5

        if portfolio_value > 100000:
            score += 5

        score = max(0, min(100, score))

        if score >= 75:
            level = "LOW"
            icon = "🟢"
        elif score >= 45:
            level = "MODERATE"
            icon = "🟡"
        else:
            level = "HIGH"
            icon = "🔴"

        return {"score": score, "level": level, "icon": icon}
