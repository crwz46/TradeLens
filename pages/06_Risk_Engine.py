import streamlit as st
from tradelens.analytics.market import MarketData
from tradelens.portfolio.tracker import Portfolio
from tradelens.risk.metrics import RiskMetrics
from tradelens.components import metric_card, section_header, dark_fig, plot_gauge

st.set_page_config(page_title="Risk Engine", page_icon="⚡", layout="wide")

section_header("⚡ Risk Engine", "Portfolio risk analysis — Sharpe Ratio, Volatility, Max Drawdown")

market = MarketData()
portfolio = Portfolio.load()

with st.sidebar:
    st.markdown("### Risk Parameters")
    annual_vol = st.slider("Assumed Annual Volatility", 0.1, 1.5, 0.5, 0.05)
    drift = st.slider("Daily Drift (Return)", -0.005, 0.005, 0.0005, 0.0001)

try:
    metrics = RiskMetrics.calculate(annual_vol, drift)
    prices = market.prices()
    total_value = portfolio.total_value(prices)
    allocation = portfolio.allocation(prices)
    risk_score = RiskMetrics.portfolio_risk_score(total_value, len(allocation),
                                                   metrics["sharpe_ratio"], metrics["volatility_pct"])
except Exception:
    st.error("Risk engine unavailable")
    st.stop()

cols = st.columns(4)
with cols[0]:
    sharpe = metrics["sharpe_ratio"]
    sharpe_color = "#3fb950" if sharpe > 1.0 else "#f59e0b" if sharpe > 0 else "#ef4444"
    metric_card("Sharpe Ratio", f"{sharpe:.2f}", metrics["sharpe_label"])

with cols[1]:
    vol = metrics["volatility_pct"]
    vol_color = "#3fb950" if vol < 30 else "#f59e0b" if vol < 60 else "#ef4444"
    metric_card("Volatility", f"{vol:.1f}%", metrics["volatility_label"])

with cols[2]:
    dd = metrics["max_drawdown_pct"]
    metric_card("Max Drawdown", f"{dd:.1f}%", metrics["max_drawdown_label"])

with cols[3]:
    metric_card("Annualized Return", f"{metrics['annualized_return_pct']:.1f}%")

st.divider()

col1, col2 = st.columns(2)
with col1:
    fig = plot_gauge(sharpe * 33.3, 100, f"Sharpe Ratio: {sharpe:.2f}", "#3fb950")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    r = risk_score
    fig = plot_gauge(r["score"], 100, f"Portfolio Risk: {r['level']}", "#58a6ff")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("### Risk Metrics Breakdown")
st.markdown(f"""
| Metric | Value | Rating | Interpretation |
|---|---|---|---|
| **Sharpe Ratio** | {sharpe:.2f} | {metrics['sharpe_label']} | Risk-adjusted return > 1 is good |
| **Volatility** | {vol:.1f}% | {metrics['volatility_label']} | Annualized standard deviation |
| **Max Drawdown** | {dd:.1f}% | {metrics['max_drawdown_label']} | Worst peak-to-trough decline |
| **Portfolio Risk Score** | {risk_score['score']}/100 | {risk_score['icon']} {risk_score['level']} | Composite risk assessment |
""")

st.code("""
# Sharpe Ratio Formula
sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility

# Max Drawdown
max_drawdown = min(cumulative_return / peak_value - 1)

# Volatility
volatility = std(daily_returns) * sqrt(252)
""", language="python")
