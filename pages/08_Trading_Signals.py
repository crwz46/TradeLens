import streamlit as st
from tradelens.analytics.market import MarketData
from tradelens.signals.conditions import MarketConditions
from tradelens.components import metric_card, section_header, status_badge

st.set_page_config(page_title="Trading Signals", page_icon="📡", layout="wide")

section_header("📡 Trading Signals", "Market condition analysis — research only, not financial advice")

market = MarketData()
conditions = MarketConditions(market)

try:
    signal = conditions.analyze()
except Exception:
    st.error("Signal engine unavailable")
    st.stop()

trend = signal["trend"]
sentiment = signal["sentiment"]

cols = st.columns(4)
with cols[0]:
    st.markdown(f"""
    <div style="background:#161b22; border:1px solid #30363d; border-radius:8px; padding:16px; text-align:center;">
        <div style="font-size:36px;">{trend['icon']}</div>
        <div style="color:#8b949e; font-size:13px;">Trend</div>
        <div style="color:#e6edf3; font-size:20px; font-weight:700;">{trend['label']}</div>
    </div>
    """, unsafe_allow_html=True)

with cols[1]:
    funding_status = signal["funding_status"]
    f_color = "#ef4444" if funding_status == "Overheated" else "#f59e0b" if funding_status == "Elevated" else "#3fb950" if funding_status == "Normal" else "#8b949e"
    st.markdown(f"""
    <div style="background:#161b22; border:1px solid #30363d; border-radius:8px; padding:16px; text-align:center;">
        <div style="font-size:36px;">💰</div>
        <div style="color:#8b949e; font-size:13px;">Funding</div>
        <div style="color:#e6edf3; font-size:20px; font-weight:700;">{funding_status}</div>
    </div>
    """, unsafe_allow_html=True)

with cols[2]:
    st.markdown(f"""
    <div style="background:#161b22; border:1px solid #30363d; border-radius:8px; padding:16px; text-align:center;">
        <div style="font-size:36px;">{sentiment['icon']}</div>
        <div style="color:#8b949e; font-size:13px;">Sentiment</div>
        <div style="color:#e6edf3; font-size:20px; font-weight:700;">{sentiment['label']}</div>
    </div>
    """, unsafe_allow_html=True)

with cols[3]:
    risk = signal["composite_risk"]
    r_color = "#3fb950" if risk == "Low" else "#f59e0b" if risk == "Medium" else "#ef4444"
    st.markdown(f"""
    <div style="background:#161b22; border:1px solid #30363d; border-radius:8px; padding:16px; text-align:center;">
        <div style="font-size:36px;">⚖️</div>
        <div style="color:#8b949e; font-size:13px;">Risk</div>
        <div style="color:#e6edf3; font-size:20px; font-weight:700;">{risk}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("### Detailed Analysis")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 📊 Market Conditions")
    ls_risk = signal["long_short_risk"]
    oi_risk = signal["open_interest_risk"]
    st.markdown(f"""
    - **Trend:** {trend['icon']} {trend['label']}
    - **Funding Status:** {funding_status}
    - **Sentiment:** {sentiment['icon']} {sentiment['label']} ({sentiment['value']}/100)
    - **Open Interest Risk:** {oi_risk}
    - **Long/Short Risk:** {ls_risk}
    """)

with col2:
    st.markdown("#### ⚠️ Risk Assessment")
    fng_val = sentiment["value"]
    if fng_val > 80:
        st.markdown("🔴 **Market is extremely greedy** — potential top, consider taking profits")
    elif fng_val < 20:
        st.markdown("🟢 **Market is extremely fearful** — potential bottom, accumulation zone")
    else:
        st.markdown("🟡 **Market sentiment is neutral** — no extreme signals detected")

    if "Overheated" in funding_status:
        st.markdown("🔴 **Funding rates are overheated** — long position costs are high, liquidation cascade risk")
    elif "Negative" in funding_status:
        st.markdown("🟢 **Funding rates are negative** — short sellers paying, potential short squeeze setup")

st.divider()
st.markdown("### 📝 Research Notes")
st.markdown("""
> **Disclaimer:** This is a research tool only. All signals are for educational purposes.
> The composite risk assessment combines funding rate analysis, Fear & Greed index,
> open interest trends, and long/short positioning to provide a holistic market view.
>
> **Quant professionals:** The sentiment scoring methodology is transparent and customizable
> in `tradelens/analytics/sentiment.py`.
""")
