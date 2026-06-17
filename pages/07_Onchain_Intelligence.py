import streamlit as st
import pandas as pd
from tradelens.analytics.onchain import OnChainData
from tradelens.components import metric_card, section_header, dark_fig, plot_gauge

st.set_page_config(page_title="On-Chain Intelligence", page_icon="🔗", layout="wide")

section_header("🔗 On-Chain Intelligence", "Whale activity monitoring and top holder concentration analysis")

try:
    whale = OnChainData.large_transaction_summary()
    holders = OnChainData.holder_concentration("UNI")
except Exception:
    st.error("On-chain data unavailable")
    st.stop()

cols = st.columns(3)
with cols[0]:
    metric_card("Large Transfers (24h)", f"{whale['total_large_transfers']}")
with cols[1]:
    metric_card("Total Value", f"${whale['total_value_m']:.2f}M")
with cols[2]:
    metric_card("Largest TX", f"${whale['largest_tx_m']:.2f}M")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🐋 Recent Whale Transfers")
    transfers_df = pd.DataFrame(whale["transfers"])
    transfers_df["Value"] = transfers_df["value_usd"].apply(lambda x: f"${x/1e6:.2f}M")
    transfers_df["From"] = transfers_df["from"].apply(lambda x: f"{x[:6]}...{x[-4:]}")
    transfers_df["To"] = transfers_df["to"].apply(lambda x: f"{x[:6]}...{x[-4:]}")
    st.dataframe(transfers_df[["symbol", "Value", "type", "From", "To"]].rename(
        columns={"symbol": "Asset", "Value": "Value", "type": "Type", "From": "From", "To": "To"}
    ), use_container_width=True, hide_index=True)

with col2:
    st.markdown("### 🏦 Top Holder Concentration")
    h = holders
    st.markdown(f"""
    | Metric | Value |
    |---|---|
    | **Token** | {h['symbol']} |
    | **Top 1 Hold %** | {h['top1_pct']:.2f}% |
    | **Top 10 Hold %** | {h['top10_pct']:.2f}% |
    | **HHI Index** | {h['hhi']:.4f} |
    | **Gini Coefficient** | {h['gini']:.4f} |
    | **Risk Level** | {h['icon']} {h['risk']} |
    """)
    fig = plot_gauge(h['top10_pct'], 100, f"Top 10 Concentration: {h['risk']}",
                     "#ef4444" if h['risk'] == "HIGH" else "#f59e0b" if h['risk'] == "MODERATE" else "#3fb950")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("### 🔗 Connected Projects")
st.markdown("""
This module integrates concepts from:
- **[WallTrack](https://github.com/crwz46/WallTrack)** — Multi-chain wallet tracking & whale alerts
- **[TokenVision](https://github.com/crwz46/TokenVision)** — Token holder concentration analysis with HHI & Gini

Both are standalone repos in the same crypto analytics ecosystem.
""")
