import streamlit as st
import pandas as pd
from tradelens.analytics.futures import FuturesData
from tradelens.components import metric_card, section_header, dark_fig, plot_gauge

st.set_page_config(page_title="Futures Analytics", page_icon="📈", layout="wide")

section_header("📈 Futures Analytics", "Funding rates, Open Interest, and Long/Short ratios for top assets")

symbol = st.selectbox("Select Asset", ["BTC", "ETH", "SOL"], index=0)

try:
    data = FuturesData.aggregated(symbol)
except Exception:
    st.error("Futures data unavailable")
    st.stop()

funding = data["funding"]
oi = data["open_interest"]
ls = data["long_short"]

cols = st.columns(3)
with cols[0]:
    fr = funding.get("funding_rate", 0)
    delta_str = f"{funding.get('annualized', 0):.1f}% annualized"
    metric_card("Funding Rate", f"{fr:+.3f}%", delta_str if fr > 0 else None)
with cols[1]:
    oi_val = oi.get("open_interest_b", 0)
    oi_chg = oi.get("change_24h_pct", 0)
    metric_card("Open Interest", f"${oi_val:.1f}B", f"{oi_chg:+.1f}% 24h")
with cols[2]:
    ratio = ls.get("ratio", 0)
    metric_card("Long/Short Ratio", f"{ratio:.2f}", f"{ls.get('long_pct', 0)}% Long / {ls.get('short_pct', 0)}% Short")

st.divider()

col1, col2 = st.columns(2)
with col1:
    fig = plot_gauge(fr * 100 + 5, 10, f"{symbol} Funding Health", "#58a6ff")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = plot_gauge(ratio * 25, 100, f"{symbol} Long/Short Score", "#3fb950")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown(f"### {symbol} Futures Summary")
summary_df = pd.DataFrame([{
    "Metric": "Funding Rate", "Value": f"{fr:+.3f}%", "Status": funding.get("status", ""),
}, {
    "Metric": "Open Interest", "Value": f"${oi_val:.1f}B", "Status": f"{oi_chg:+.1f}% 24h",
}, {
    "Metric": "Long/Short Ratio", "Value": f"{ratio:.2f}", "Status": f"Bias: {ls.get('bias', 'Neutral')}",
}])
st.dataframe(summary_df, use_container_width=True, hide_index=True)

st.divider()
st.markdown("### Cross-Asset Comparison")
try:
    all_data = FuturesData.all_symbols()
    rows = []
    for d in all_data:
        rows.append({
            "Symbol": d["funding"]["symbol"],
            "Funding Rate": f"{d['funding']['funding_rate']:+.3f}%",
            "OI ($B)": f"${d['open_interest']['open_interest_b']:.1f}B",
            "L/S Ratio": f"{d['long_short']['ratio']:.2f}",
            "Bias": d["long_short"]["bias"],
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
except Exception:
    st.info("Cross-asset comparison unavailable")
