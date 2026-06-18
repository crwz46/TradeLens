# TradeLens[![CI](https://github.com/crwz46/TradeLens/actions/workflows/test.yml/badge.svg)](https://github.com/crwz46/TradeLens/actions/workflows/test.yml)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)](https://fastapi.tiangolo.com)

**Professional Crypto Market Intelligence Dashboard** — 8 integrated modules covering market data, futures analytics, liquidation monitoring, sentiment scoring, portfolio tracking, risk engine, on-chain intelligence, and trading signals.

```
┌─────────────────────────────────────────────────────────────┐
│                     📊 TradeLens                             │
│  Professional Crypto Market Intelligence Dashboard          │
├─────────────────────────────────────────────────────────────┤
│  🔵 Market Overview    📈 Futures Analytics   💦 Liq Monitor│
│  🧠 Sentiment Engine   💼 Portfolio Tracker   ⚡ Risk Engine│
│  🔗 On-Chain Intel     📡 Trading Signals                   │
└─────────────────────────────────────────────────────────────┘
```

## Architecture

```
┌──────────────┐     ┌───────────────────┐     ┌──────────────┐
│  Streamlit    │────▶│   FastAPI Backend  │────▶│  CoinGecko   │
│  Dashboard    │     │   (8 endpoints)    │     │  Alternative  │
│  (8 pages)    │◀────│   localhost:8000   │◀────│  Simulated   │
└──────────────┘     └───────────────────┘     └──────────────┘
                            │
                    ┌───────┴───────┐
                    │   SQLite DB    │
                    │  (Portfolio)   │
                    └───────────────┘
```

## 8 Modules

### 🔵 Module 1 — Market Overview
Live crypto market data from CoinGecko:
- BTC, ETH, SOL prices
- Total market cap & BTC dominance
- 24h volume & active cryptos
- Fear & Greed Index (Alternative.me)
- Interactive price charts (7/30/90 day)

### 📈 Module 2 — Futures Analytics
Per-asset derivatives data:
- **Funding Rate** — Current + annualized, status indicator
- **Open Interest** — Total OI + 24h change
- **Long/Short Ratio** — Bias detection, gauge visualization
- Cross-asset comparison table

### 💦 Module 3 — Liquidation Monitor
Track market stress:
- **Summary** — Long/Short liquidation totals
- **Heatmap** — 24h liquidation intensity visualization
- **Top Liquidations** — Largest single events
- L/S ratio and dominance indicators

### 🧠 Module 4 — Sentiment Engine
Custom market sentiment scoring:
```
sentiment = fear_greed(30%) + funding_rate(25%) + OI_trend(20%) + L/S_ratio(25%)
```
- Score 0–100 with status (BULLISH / NEUTRAL / BEARISH)
- Component breakdown with raw values
- Transparent, customizable formula

### 💼 Module 5 — Portfolio Tracker
Track your crypto holdings:
- Input amounts + entry prices for BTC/ETH/SOL
- Real-time PnL calculation
- Allocation pie chart
- Cost basis tracking
- Persisted to JSON file / SQLite

### ⚡ Module 6 — Risk Engine
Quantitative portfolio risk analysis:

| Metric | Formula | Interpretation |
|--------|---------|---------------|
| **Sharpe Ratio** | `(Rₚ - R_f) / σₚ` | Risk-adjusted return |
| **Volatility** | `σ(daily_returns) × √252` | Annualized price risk |
| **Max Drawdown** | `min(return / peak - 1)` | Worst historical loss |
| **Risk Score** | Composite (0–100) | Overall portfolio risk |

### 🔗 Module 7 — On-Chain Intelligence
Whale and holder analytics:
- **Whale Transfers** — Recent large transactions
- **Top Holder Concentration** — HHI, Gini, Top-N%
- Risk assessment based on distribution metrics
- Integrates concepts from [TokenVision](https://github.com/crwz46/TokenVision) + [WallTrack](https://github.com/crwz46/WallTrack)

### 📡 Module 8 — Trading Signals (Research Only)
Market condition synthesis:
- **Trend Analysis** — Bullish/Neutral/Bearish
- **Funding Assessment** — Normal/Elevated/Overheated
- **Risk Level** — Low/Medium/High
- **Disclaimer** — Educational research tool

---

## Quick Start

```bash
pip install -r requirements.txt

# Start Streamlit Dashboard
streamlit run main.py

# Start FastAPI Backend (optional, for API access)
uvicorn tradelens.api.server:app --reload --port 8000
```

### Docker

```bash
docker-compose up -d
# → Dashboard: http://localhost:8501
# → API: http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service info |
| GET | `/market/overview` | Full market overview |
| GET | `/market/prices` | Live BTC/ETH/SOL prices |
| GET | `/market/fear-greed` | Fear & Greed Index |
| GET | `/market/chart/{coin}` | OHLC/price chart data |
| GET | `/futures/{symbol}` | Funding, OI, L/S for asset |
| GET | `/futures/all` | Cross-asset comparison |
| GET | `/liquidations/summary` | Liquidation totals |
| GET | `/liquidations/heatmap` | 24h heatmap data |
| GET | `/liquidations/top` | Top liquidation events |
| GET | `/sentiment` | Sentiment engine score |
| GET | `/onchain/whales` | Recent whale transfers |
| GET | `/onchain/holders/{symbol}` | Holder concentration |
| GET | `/portfolio/value` | Portfolio value & PnL |
| GET | `/risk` | Risk metrics (Sharpe, Vol, DD) |
| GET | `/signals` | Market conditions |
| GET | `/health` | Health check |

## Project Structure

```
TradeLens/
├── main.py                          # Streamlit entry point
├── pages/                           # 8 dashboard pages
│   ├── 01_Market_Overview.py
│   ├── 02_Futures_Analytics.py
│   ├── 03_Liquidation_Monitor.py
│   ├── 04_Sentiment_Engine.py
│   ├── 05_Portfolio_Tracker.py
│   ├── 06_Risk_Engine.py
│   ├── 07_Onchain_Intelligence.py
│   └── 08_Trading_Signals.py
├── tradelens/                       # Core package
│   ├── components.py                # Shared UI (dark theme)
│   ├── config.py                    # API keys & settings
│   ├── analytics/                   # Data layer
│   │   ├── market.py                # CoinGecko API
│   │   ├── futures.py               # Derivatives data
│   │   ├── liquidations.py          # Liquidation tracking
│   │   ├── sentiment.py             # Sentiment engine
│   │   └── onchain.py               # Whale & holder data
│   ├── portfolio/                   # Portfolio management
│   │   ├── tracker.py               # Holdings, value, allocation
│   │   └── pnl.py                   # PnL calculations
│   ├── risk/                        # Risk analytics
│   │   ├── engine.py                # Risk computation
│   │   └── metrics.py               # Sharpe, Vol, Drawdown
│   ├── signals/                     # Trading signals
│   │   └── conditions.py            # Market condition analysis
│   ├── data/                        # Database layer
│   │   ├── database.py              # SQLite connection
│   │   └── models.py                # ORM models
│   └── api/                         # FastAPI backend
│       ├── server.py                # FastAPI app
│       └── routes.py                # 16 API endpoints
├── tests/
│   └── test_tradelens.py            # 25+ tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Streamlit, Plotly, Dark Theme CSS |
| **Backend** | FastAPI, Uvicorn |
| **Data** | CoinGecko API, Alternative.me API, SQLite |
| **Analytics** | NumPy, Pandas |
| **Visualization** | Plotly (pie, bar, line, gauge, heatmap) |
| **Deployment** | Docker, Docker Compose |
| **Testing** | pytest (25+ tests) |

## Data Sources

- **CoinGecko API** — Prices, market cap, dominance, historical data
- **Alternative.me** — Fear & Greed Index
- **Simulated Data** — Futures, liquidations, on-chain (seeded, deterministic)

## Tests

```bash
pytest tests/ -v
```

## Why Recruiters Love This

| Skill | Demonstrated |
|-------|--------------|
| **Quant Finance** | Sharpe Ratio, Volatility, Max Drawdown |
| **Risk Management** | Portfolio risk scoring, drawdown analysis |
| **Data Engineering** | Multi-API integration, caching, error handling |
| **Full-Stack** | Streamlit + FastAPI + SQLite + Docker |
| **UI/UX** | Professional dark theme, interactive charts |
| **System Design** | 8-module architecture, clean separation |
| **Crypto Domain** | Market microstructure, futures, liquidations |

## Ecosystem

TradeLens is part of a **3-repo crypto analytics ecosystem**:

| Repo | Focus |
|------|-------|
| [WallTrack](https://github.com/crwz46/WallTrack) | Multi-chain wallet tracking, gas alerts, flash loans |
| [TokenVision](https://github.com/crwz46/TokenVision) | Token holder concentration, HHI/Gini, whale detection |
| **TradeLens** | Market intelligence, risk engine, portfolio tracker |

---

*Built for educational and portfolio purposes. Not financial advice.*
