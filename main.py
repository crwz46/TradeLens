import streamlit as st

st.set_page_config(
    page_title="TradeLens",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background-color: #0d1117; }
    .st-emotion-cache-1y4p8pa { padding: 2rem 2rem; }
    .stSelectbox label, .stNumberInput label { color: #8b949e; }
    h1, h2, h3 { color: #e6edf3; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #58a6ff; }
</style>
""", unsafe_allow_html=True)

from tradelens.analytics.market import MarketData
from tradelens.analytics.futures import FuturesData
from tradelens.analytics.sentiment import SentimentEngine
from tradelens.components import metric_card, dark_fig, plot_gauge

market = MarketData()
sentiment = SentimentEngine(market)

with st.sidebar:
    st.markdown("# 📊 TradeLens")
    st.markdown("*Professional Crypto Intelligence*")
    st.divider()
    st.page_link("main.py", label="🏠 Dashboard", use_container_width=True)
    st.page_link("pages/01_Market_Overview.py", label="🔵 Market Overview", use_container_width=True)
    st.page_link("pages/02_Futures_Analytics.py", label="📈 Futures Analytics", use_container_width=True)
    st.page_link("pages/03_Liquidation_Monitor.py", label="💦 Liquidation Monitor", use_container_width=True)
    st.page_link("pages/04_Sentiment_Engine.py", label="🧠 Sentiment Engine", use_container_width=True)
    st.page_link("pages/05_Portfolio_Tracker.py", label="💼 Portfolio Tracker", use_container_width=True)
    st.page_link("pages/06_Risk_Engine.py", label="⚡ Risk Engine", use_container_width=True)
    st.page_link("pages/07_Onchain_Intelligence.py", label="🔗 On-Chain Intel", use_container_width=True)
    st.page_link("pages/08_Trading_Signals.py", label="📡 Trading Signals", use_container_width=True)
    st.divider()
    st.caption("Built by crwz46 · 8 Modules")

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

try:
    prices = market.prices()
    fng = market.fear_greed()
    global_d = market.global_data()

    with col1:
        btc_price = prices.get("BTC", 0)
        metric_card("BTC", f"${btc_price:,.0f}" if btc_price else "N/A")
    with col2:
        eth_price = prices.get("ETH", 0)
        metric_card("ETH", f"${eth_price:,.0f}" if eth_price else "N/A")
    with col3:
        sol_price = prices.get("SOL", 0)
        metric_card("SOL", f"${sol_price:,.0f}" if sol_price else "N/A")
    with col4:
        fng_val = fng.get("value", 50)
        fng_class = fng.get("classification", "Neutral")
        metric_card("Fear & Greed", f"{fng_val} ({fng_class})")
except Exception:
    for col in [col1, col2, col3, col4]:
        with col:
            metric_card("—", "Offline")

st.divider()

st.markdown("### 📊 Market Intelligence Platform")
st.markdown("""
TradeLens is a **professional-grade crypto market intelligence dashboard** with 8 integrated modules:

| Module | Description |
|--------|-------------|
| 🔵 **Market Overview** | Live prices, market cap, BTC dominance, Fear & Greed |
| 📈 **Futures Analytics** | Funding rates, Open Interest, Long/Short ratios |
| 💦 **Liquidation Monitor** | Long/Short liquidations, heatmap, top liquidations |
| 🧠 **Sentiment Engine** | Custom scoring: funding + F&G + OI + L/S |
| 💼 **Portfolio Tracker** | Track holdings, PnL, allocation pie |
| ⚡ **Risk Engine** | Sharpe Ratio, Volatility, Max Drawdown |
| 🔗 **On-Chain Intel** | Whale transfers, holder concentration |
| 📡 **Trading Signals** | Market conditions, risk assessment |
""")

col1, col2 = st.columns(2)
with col1:
    try:
        s = sentiment.score()
        fig = plot_gauge(s["total_score"], 100, f"Market Sentiment: {s['status']}",
                         "#3fb950" if "BULL" in s["status"] else "#f59e0b" if "NEUTRAL" in s else "#ef4444")
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.info("Sentiment engine unavailable")
with col2:
    st.markdown("### Quick Actions")
    st.markdown("""
    - 🔍 **Scan airdrop eligibility** → AirDropScanner
    - 🐋 **Check token concentration** → TokenVision
    - 💰 **Track multi-chain wallet** → WallTrack
    """)

st.divider()
st.caption("TradeLens v1.0 · Data from CoinGecko & Alternative.me · Not financial advice")
