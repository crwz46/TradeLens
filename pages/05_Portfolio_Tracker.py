import streamlit as st
import pandas as pd
from tradelens.analytics.market import MarketData
from tradelens.portfolio.tracker import Portfolio
from tradelens.components import metric_card, section_header, dark_fig, plot_pie

st.set_page_config(page_title="Portfolio Tracker", page_icon="💼", layout="wide")

section_header("💼 Portfolio Tracker", "Track your holdings, view allocation, and analyze PnL")

market = MarketData()

if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio.load()

portfolio = st.session_state.portfolio

with st.expander("✏️ Edit Holdings", expanded=True):
    st.markdown("Enter your holdings and average entry price:")
    cols = st.columns(3)
    btc_amt = cols[0].number_input("BTC", 0.0, 1000.0, portfolio.holdings.get("BTC", 0.0), 0.01, format="%.4f")
    btc_cost = cols[0].number_input("BTC Entry Price ($)", 0.0, 500000.0, portfolio.cost_basis.get("BTC", 0.0), 100.0)
    eth_amt = cols[1].number_input("ETH", 0.0, 100000.0, portfolio.holdings.get("ETH", 0.0), 0.1, format="%.2f")
    eth_cost = cols[1].number_input("ETH Entry Price ($)", 0.0, 50000.0, portfolio.cost_basis.get("ETH", 0.0), 10.0)
    sol_amt = cols[2].number_input("SOL", 0.0, 1000000.0, portfolio.holdings.get("SOL", 0.0), 1.0, format="%.0f")
    sol_cost = cols[2].number_input("SOL Entry Price ($)", 0.0, 1000.0, portfolio.cost_basis.get("SOL", 0.0), 1.0)

    if st.button("💾 Save Portfolio", use_container_width=True):
        portfolio.holdings = {}
        portfolio.cost_basis = {}
        if btc_amt > 0:
            portfolio.set_holding("BTC", btc_amt, btc_cost)
        if eth_amt > 0:
            portfolio.set_holding("ETH", eth_amt, eth_cost)
        if sol_amt > 0:
            portfolio.set_holding("SOL", sol_amt, sol_cost)
        portfolio.save()
        st.success("Portfolio saved!")

st.divider()

try:
    prices = market.prices()
except Exception:
    st.error("Could not fetch prices")
    st.stop()

if not portfolio.holdings:
    st.info("Add holdings above to see your portfolio")
    st.stop()

total_value = portfolio.total_value(prices)
allocation = portfolio.allocation(prices)
pnl_data = portfolio.pnl(prices)

cols = st.columns(4)
with cols[0]:
    metric_card("Total Value", f"${total_value:,.2f}")
with cols[1]:
    metric_card("Total PnL", f"${pnl_data['total_pnl']:+,.2f}",
                f"{pnl_data['total_pnl_pct']:+.1f}%" if pnl_data['total_pnl'] != 0 else None)
with cols[2]:
    metric_card("Assets", f"{len(portfolio.holdings)}")
with cols[3]:
    cost = pnl_data["total_cost"]
    metric_card("Cost Basis", f"${cost:,.2f}" if cost else "N/A")

st.divider()

col1, col2 = st.columns(2)
with col1:
    labels = [a["symbol"] for a in allocation]
    values = [a["value_usd"] for a in allocation]
    if labels and values:
        fig = plot_pie(labels, values, "Portfolio Allocation")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### PnL Breakdown")
    pnl_df = pd.DataFrame(pnl_data["details"])
    pnl_df["PnL"] = pnl_df["pnl_usd"].apply(lambda x: f"${x:+,.2f}")
    pnl_df["Return"] = pnl_df["pnl_pct"].apply(lambda x: f"{x:+.1f}%")
    pnl_df["Value"] = pnl_df["value_usd"].apply(lambda x: f"${x:,.2f}")
    st.dataframe(pnl_df[["symbol", "amount", "Value", "PnL", "Return"]].rename(
        columns={"symbol": "Asset", "amount": "Holdings", "Value": "Value", "PnL": "PnL", "Return": "Return"}
    ), use_container_width=True, hide_index=True)
