import streamlit as st
from tradelens.analytics.market import MarketData
from tradelens.components import metric_card, section_header, dark_fig, plot_line

st.set_page_config(page_title="Market Overview", page_icon="🔵", layout="wide")
market = MarketData()

st.markdown("# 🔵 Market Overview")
st.markdown("*Live crypto market data — prices, capitalization, dominance, and sentiment*")

try:
    prices = market.prices()
    global_d = market.global_data()
    fng = market.fear_greed()
except Exception:
    st.error("Could not fetch market data. Check your connection.")
    st.stop()

cols = st.columns(5)
tokens = [("BTC", prices.get("BTC", 0), "$"), ("ETH", prices.get("ETH", 0), "$"),
           ("SOL", prices.get("SOL", 0), "$")]
for i, (sym, price, prefix) in enumerate(tokens):
    with cols[i]:
        metric_card(sym, f"{prefix}{price:,.0f}" if price else "N/A")

with cols[3]:
    metric_card("Market Cap", f"${global_d.get('total_market_cap', 0)/1e12:.2f}T")
with cols[4]:
    metric_card("BTC Dominance", f"{global_d.get('btc_dominance', 0):.1f}%")

cols2 = st.columns(3)
with cols2[0]:
    metric_card("24h Volume", f"${global_d.get('volume_24h', 0)/1e9:.2f}B")
with cols2[1]:
    metric_card("Active Cryptos", f"{global_d.get('active_cryptos', 0):,}")
with cols2[2]:
    fng_val = fng.get("value", 50)
    fng_class = fng.get("classification", "Neutral")
    color = "#3fb950" if fng_val > 55 else "#f59e0b" if fng_val > 40 else "#ef4444"
    metric_card("Fear & Greed", f"{fng_val} — {fng_class}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    try:
        btc_chart = market.market_chart("bitcoin", 30)
        if btc_chart and "prices" in btc_chart:
            dates = [x[0] / 1000 for x in btc_chart["prices"]]
            vals = [x[1] for x in btc_chart["prices"]]
            fig = plot_line(dates, vals, "BTC — 30 Day Price", "#f7931a")
            st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.info("BTC chart unavailable")

with col2:
    try:
        eth_chart = market.market_chart("ethereum", 30)
        if eth_chart and "prices" in eth_chart:
            dates = [x[0] / 1000 for x in eth_chart["prices"]]
            vals = [x[1] for x in eth_chart["prices"]]
            fig = plot_line(dates, vals, "ETH — 30 Day Price", "#627eea")
            st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.info("ETH chart unavailable")
