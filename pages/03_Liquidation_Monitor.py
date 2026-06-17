import streamlit as st
import pandas as pd
from tradelens.analytics.liquidations import LiquidationData
from tradelens.components import metric_card, section_header, dark_fig, plot_heatmap

st.set_page_config(page_title="Liquidation Monitor", page_icon="💦", layout="wide")

section_header("💦 Liquidation Monitor", "Real-time liquidation tracking across top assets")

try:
    summary = LiquidationData.summary()
    heatmap = LiquidationData.heatmap_data(24)
    top_liq = LiquidationData.top_liquidations(10)
except Exception:
    st.error("Liquidation data unavailable")
    st.stop()

cols = st.columns(4)
with cols[0]:
    metric_card("Long Liquidations", f"${summary['long_24h_m']:.1f}M", "24h")
with cols[1]:
    metric_card("Short Liquidations", f"${summary['short_24h_m']:.1f}M", "24h")
with cols[2]:
    metric_card("Total", f"${summary['total_24h_m']:.1f}M", "24h")
with cols[3]:
    metric_card("L/S Ratio", f"{summary['long_short_ratio']:.2f}", "Longs dominate" if summary['long_short_ratio'] > 1 else "Shorts dominate")

st.divider()

st.markdown("### Liquidation Heatmap (Last 24 Hours)")
try:
    hours = [h["hour"] for h in heatmap]
    liq_data = [[h["long_liq_m"] for h in heatmap], [h["short_liq_m"] for h in heatmap]]
    fig = plot_heatmap(liq_data, hours, ["Long", "Short"], "Liquidation Intensity")
    st.plotly_chart(fig, use_container_width=True)
except Exception:
    st.info("Heatmap unavailable")

st.divider()

st.markdown("### Top Liquidations (24h)")
liq_df = pd.DataFrame(top_liq)
liq_df["Side"] = liq_df["side"].apply(lambda x: f"🔴 {x}" if x == "Long" else f"🟢 {x}")
liq_df["Value"] = liq_df["value_m"].apply(lambda x: f"${x:.1f}M")
liq_df["Price"] = liq_df["price"].apply(lambda x: f"${x:,.2f}")
st.dataframe(liq_df[["symbol", "Value", "Side", "Price"]].rename(
    columns={"symbol": "Symbol", "Value": "Value", "Side": "Side", "Price": "Liquidation Price"}
), use_container_width=True, hide_index=True)
