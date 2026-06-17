import streamlit as st
import pandas as pd
from tradelens.analytics.market import MarketData
from tradelens.analytics.sentiment import SentimentEngine
from tradelens.components import metric_card, section_header, dark_fig, plot_gauge

st.set_page_config(page_title="Sentiment Engine", page_icon="🧠", layout="wide")

section_header("🧠 Market Sentiment Engine", "Custom scoring algorithm combining funding, fear & greed, OI, and L/S ratio")

market = MarketData()
engine = SentimentEngine(market)

try:
    result = engine.score()
except Exception:
    st.error("Sentiment engine unavailable")
    st.stop()

status = result["status"]
icon = result["icon"]
total = result["total_score"]
color = "#3fb950" if "BULL" in status else "#f59e0b" if "NEUTRAL" in status else "#ef4444"

col1, col2 = st.columns([1, 2])
with col1:
    fig = plot_gauge(total, 100, f"Market Sentiment: {status}", color)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"<div style='text-align:center; font-size:32px; margin-top:-20px;'>{icon} <strong>{status}</strong></div>",
                unsafe_allow_html=True)

with col2:
    comps = result["components"]
    st.markdown("### Component Scores")
    comp_df = pd.DataFrame([{
        "Component": k.replace("_", " ").title(),
        "Raw Value": v["raw"],
        "Weighted Score": f"{v['score']:.1f}/{100 * float(v['weight'].replace('%', '')) / 100:.0f}",
        "Weight": v["weight"],
    } for k, v in comps.items()])
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

st.divider()
st.markdown("### Formula")
st.code("sentiment_score = fear_greed(30%) + funding_rate(25%) + open_interest(20%) + long_short(25%)", language="python")

st.divider()
st.markdown("### Interpretation")
st.markdown(f"""
| Score Range | Signal | Action |
|---|---|---|
| 70–100 | 🟢 **Bullish** | Strong market confidence, elevated funding |
| 50–69 | 🟡 **Neutral** | Balanced sentiment, normal conditions |
| 30–49 | 🟠 **Bearish** | Caution, negative funding pressure |
| 0–29 | 🔴 **Extreme Fear** | Panic selling, potential bottom |
""")
st.markdown(f"**Current: {total:.1f}/100 — {icon} {status}**")
