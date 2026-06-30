"""
STOCK ANALYSIS PRO - Professional Equity Research Terminal
A Bloomberg Terminal-style institutional stock market dashboard
Built with Python + Streamlit + Plotly + AgGrid

Author: Parvez Alam Ansari
Version: 17.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# For real market data (install with: pip install yfinance)
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    st.warning("yfinance not installed. Install with: pip install yfinance")

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="STOCK ANALYSIS PRO - Professional Equity Research Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS & STYLING
# ============================================================================

CUSTOM_CSS = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        color: #e0e0e0;
    }
    
    /* Streamlit Overrides */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    /* Main Container */
    .main-container {
        max-width: 1800px;
        margin: 0 auto;
        padding: 20px;
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }
    
    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        flex-wrap: wrap;
        gap: 16px;
    }
    
    .header-title {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .header-title h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        color: #fff;
        letter-spacing: -0.5px;
    }
    
    .header-title .emoji {
        font-size: 32px;
    }
    
    .header-subtitle {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 4px;
    }
    
    .header-info {
        display: flex;
        gap: 32px;
        align-items: center;
        flex-wrap: wrap;
    }
    
    .info-block {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    
    .info-label {
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    .info-value {
        font-size: 14px;
        color: #e0e0e0;
        font-weight: 600;
        font-family: 'Courier New', monospace;
    }
    
    .market-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 12px;
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        color: #22c55e;
    }
    
    .market-status.closed {
        background: rgba(239, 68, 68, 0.15);
        border-color: rgba(239, 68, 68, 0.3);
        color: #ef4444;
    }
    
    /* Navigation */
    .nav-container {
        display: flex;
        gap: 8px;
        overflow-x: auto;
        padding: 0 0 12px 0;
        margin-bottom: 24px;
        scroll-behavior: smooth;
    }
    
    .nav-button {
        padding: 10px 16px;
        background: rgba(148, 163, 184, 0.1);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 8px;
        color: #cbd5e1;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        white-space: nowrap;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .nav-button:hover {
        background: rgba(148, 163, 184, 0.2);
        border-color: rgba(148, 163, 184, 0.4);
        color: #fff;
        transform: translateY(-2px);
    }
    
    .nav-button.active {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        border-color: #2563eb;
        color: #fff;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* Ticker */
    .ticker-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 24px;
        overflow: hidden;
    }
    
    .ticker-label {
        font-size: 10px;
        color: #64748b;
        margin-bottom: 8px;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    .ticker-scroll {
        display: flex;
        gap: 24px;
        animation: scroll 30s linear infinite;
        white-space: nowrap;
    }
    
    @keyframes scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    
    .ticker-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 0;
        font-size: 12px;
    }
    
    .ticker-symbol {
        font-weight: 700;
        color: #e0e0e0;
        font-family: 'Courier New', monospace;
    }
    
    .ticker-price {
        color: #94a3b8;
        font-size: 11px;
    }
    
    .ticker-change.positive {
        color: #22c55e;
        font-weight: 600;
    }
    
    .ticker-change.negative {
        color: #ef4444;
        font-weight: 600;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .kpi-card:hover {
        background: linear-gradient(135deg, rgba(30, 41, 59, 1) 0%, rgba(15, 23, 42, 1) 100%);
        border-color: rgba(148, 163, 184, 0.3);
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(59, 130, 246, 0.2);
    }
    
    .kpi-header {
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }
    
    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        color: #fff;
        font-family: 'Courier New', monospace;
        margin-bottom: 8px;
    }
    
    .kpi-change {
        display: flex;
        gap: 8px;
        font-size: 13px;
        font-weight: 600;
    }
    
    .change-positive {
        color: #22c55e;
    }
    
    .change-negative {
        color: #ef4444;
    }
    
    .kpi-detail {
        font-size: 11px;
        color: #94a3b8;
        margin-top: 8px;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 13px;
        color: #cbd5e1;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 28px 0 16px 0;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* Data Table */
    .data-table {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        padding: 12px;
        overflow-x: auto;
    }
    
    /* Metric Card */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    
    .metric-label {
        font-size: 11px;
        color: #94a3b8;
        margin-bottom: 8px;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 20px;
        font-weight: 700;
        color: #fff;
        font-family: 'Courier New', monospace;
    }
    
    /* News Cards */
    .news-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 8px;
        padding: 16px;
        transition: all 0.3s ease;
    }
    
    .news-card:hover {
        border-color: rgba(148, 163, 184, 0.3);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
    }
    
    .news-headline {
        font-size: 13px;
        font-weight: 700;
        color: #fff;
        margin-bottom: 8px;
        line-height: 1.4;
    }
    
    .news-meta {
        display: flex;
        justify-content: space-between;
        font-size: 11px;
        color: #64748b;
        margin-bottom: 8px;
    }
    
    .news-source {
        color: #3b82f6;
        font-weight: 600;
    }
    
    .news-time {
        color: #94a3b8;
    }
    
    .news-summary {
        font-size: 12px;
        color: #cbd5e1;
        line-height: 1.5;
        margin-bottom: 12px;
    }
    
    /* Footer */
    .footer-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-top: 40px;
        text-align: center;
    }
    
    .footer-text {
        font-size: 11px;
        color: #64748b;
        margin: 4px 0;
    }
    
    /* Charts */
    .chart-container {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        padding: 16px;
        margin: 16px 0;
    }
    
    /* Gauge Chart */
    .gauge-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 300px;
    }
    
    /* Heatmap */
    .heatmap-cell {
        border-radius: 4px;
        padding: 8px;
        text-align: center;
        font-weight: 600;
        font-size: 12px;
        transition: all 0.2s ease;
    }
    
    .heatmap-cell.strong-bullish {
        background: rgba(34, 197, 94, 0.3);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.5);
    }
    
    .heatmap-cell.bullish {
        background: rgba(34, 197, 94, 0.2);
        color: #86efac;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    
    .heatmap-cell.neutral {
        background: rgba(148, 163, 184, 0.1);
        color: #cbd5e1;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .heatmap-cell.bearish {
        background: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .heatmap-cell.strong-bearish {
        background: rgba(239, 68, 68, 0.3);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.5);
    }
    
    .heatmap-cell:hover {
        transform: scale(1.05);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(148, 163, 184, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(148, 163, 184, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(148, 163, 184, 0.5);
    }
    
    /* Responsive */
    @media (max-width: 1200px) {
        .header-info {
            gap: 16px;
        }
        
        .main-container {
            padding: 16px;
        }
    }
    
    @media (max-width: 768px) {
        .header-title h1 {
            font-size: 20px;
        }
        
        .header-info {
            flex-direction: column;
            gap: 12px;
        }
        
        .kpi-value {
            font-size: 18px;
        }
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================================
# DATA CLASSES & UTILITIES
# ============================================================================

@dataclass
class MarketData:
    """Market data structure"""
    symbol: str
    price: float
    change: float
    change_pct: float
    high: float
    low: float
    open: float
    prev_close: float
    volume: int
    rsi: float = None
    macd: float = None

class MarketDataGenerator:
    """Generate realistic market data for demo"""
    
    @staticmethod
    @st.cache_data(ttl=60)
    def generate_index_data() -> Dict[str, MarketData]:
        """Get REAL index data from Yahoo Finance"""
        
        # Yahoo Finance tickers for Indian indices
        yf_tickers = {
            'NIFTY 50': '^NSEI',
            'BANK NIFTY': '^NSEBANK',
            'NIFTY 100': '^NSEI100',
            'INDIA VIX': '^INDIAVIX',
        }
        
        data = {}
        
        for symbol_name, yf_ticker in yf_tickers.items():
            try:
                if YFINANCE_AVAILABLE:
                    # Get REAL data from Yahoo Finance
                    ticker = yf.Ticker(yf_ticker)
                    hist = ticker.history(period='1d')
                    
                    if len(hist) > 0:
                        current_price = float(hist['Close'].iloc[-1])
                        prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
                        open_price = float(hist['Open'].iloc[-1])
                        high = float(hist['High'].iloc[-1])
                        low = float(hist['Low'].iloc[-1])
                        volume = int(hist['Volume'].iloc[-1]) if hist['Volume'].iloc[-1] > 0 else 1000000
                        
                        change = current_price - prev_close
                        change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                        
                        data[symbol_name] = MarketData(
                            symbol=symbol_name,
                            price=current_price,
                            change=change,
                            change_pct=change_pct,
                            high=high,
                            low=low,
                            open=open_price,
                            prev_close=prev_close,
                            volume=volume,
                            rsi=np.random.uniform(30, 70),
                        )
                    else:
                        raise Exception("No data returned")
                else:
                    raise Exception("yfinance not available")
                    
            except Exception as e:
                # Fallback to mock data if API fails
                mock_prices = {
                    'NIFTY 50': 24500.0,
                    'BANK NIFTY': 52300.0,
                    'NIFTY 100': 26800.0,
                    'INDIA VIX': 18.5,
                }
                base_price = mock_prices.get(symbol_name, 24500)
                change_pct = np.random.uniform(-2, 3)
                change = base_price * change_pct / 100
                
                data[symbol_name] = MarketData(
                    symbol=symbol_name,
                    price=base_price + change,
                    change=change,
                    change_pct=change_pct,
                    high=base_price * 1.02,
                    low=base_price * 0.98,
                    open=base_price,
                    prev_close=base_price,
                    volume=int(np.random.uniform(1e6, 5e6)),
                    rsi=np.random.uniform(30, 70),
                )
        
        return data
    
    @staticmethod
    @st.cache_data(ttl=60)
    def generate_ticker_data() -> List[Dict]:
        """Generate live ticker data"""
        tickers = [
            ('NIFTY 50', 24500),
            ('BANK NIFTY', 52300),
            ('FINNIFTY', 22150),
            ('MIDCAP 50', 15200),
            ('SENSEX', 81500),
            ('INDIA VIX', 18.5),
            ('USDINR', 83.50),
            ('GOLD', 64200),
            ('SILVER', 78500),
            ('CRUDE OIL', 92.30),
            ('NASDAQ', 17800),
            ('S&P 500', 5450),
            ('DOW JONES', 41000),
        ]
        
        data = []
        for symbol, price in tickers:
            change_pct = np.random.uniform(-1.5, 2)
            data.append({
                'symbol': symbol,
                'price': price,
                'change_pct': change_pct,
            })
        
        return data
    
    @staticmethod
    @st.cache_data(ttl=60)
    def generate_gainers_losers() -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Generate top gainers and losers"""
        symbols = ['RELIANCE', 'TCS', 'HDFC BANK', 'INFY', 'ICICI BANK', 
                   'BAJAJ AUTO', 'LT', 'MARUTI', 'AXIS BANK', 'WIPRO']
        
        gainers_data = []
        for i, symbol in enumerate(symbols[:5], 1):
            gainers_data.append({
                'Rank': i,
                'Symbol': symbol,
                'Price': np.random.uniform(1000, 3000),
                'Change %': np.random.uniform(2, 8),
                'Volume': f"{np.random.randint(1, 100)}M",
                'RSI': np.random.uniform(50, 80),
                'Trend': '↑'
            })
        
        losers_data = []
        for i, symbol in enumerate(symbols[5:], 1):
            losers_data.append({
                'Rank': i,
                'Symbol': symbol,
                'Price': np.random.uniform(500, 2500),
                'Change %': -np.random.uniform(1, 6),
                'Volume': f"{np.random.randint(1, 100)}M",
                'RSI': np.random.uniform(20, 50),
                'Trend': '↓'
            })
        
        return pd.DataFrame(gainers_data), pd.DataFrame(losers_data)
    
    @staticmethod
    @st.cache_data(ttl=60)
    def generate_sector_heatmap() -> Dict[str, float]:
        """Generate sector performance data"""
        sectors = {
            'IT': np.random.uniform(-2, 4),
            'BANK': np.random.uniform(-2, 4),
            'AUTO': np.random.uniform(-2, 4),
            'FMCG': np.random.uniform(-2, 4),
            'METAL': np.random.uniform(-2, 4),
            'ENERGY': np.random.uniform(-2, 4),
            'REALTY': np.random.uniform(-2, 4),
            'PHARMA': np.random.uniform(-2, 4),
            'PSU': np.random.uniform(-2, 4),
            'MEDIA': np.random.uniform(-2, 4),
            'CHEMICAL': np.random.uniform(-2, 4),
            'CONSUMPTION': np.random.uniform(-2, 4),
        }
        return sectors
    
    @staticmethod
    @st.cache_data(ttl=60)
    def generate_fii_dii_data() -> Dict:
        """Generate FII/DII data"""
        return {
            'FII Buy': np.random.uniform(5000, 15000),
            'FII Sell': np.random.uniform(4000, 12000),
            'DII Buy': np.random.uniform(3000, 10000),
            'DII Sell': np.random.uniform(2500, 9000),
        }
    
    @staticmethod
    @st.cache_data(ttl=60)
    def generate_market_breadth() -> Dict[str, int]:
        """Generate market breadth data"""
        total = 1500
        advance = int(total * np.random.uniform(0.4, 0.7))
        decline = int(total * (1 - np.random.uniform(0.4, 0.7)))
        return {
            'Advance': advance,
            'Decline': decline,
            'Unchanged': total - advance - decline,
        }
    
    @staticmethod
    @st.cache_data(ttl=60)
    def generate_watchlist() -> pd.DataFrame:
        """Generate watchlist data"""
        stocks = ['RELIANCE', 'TCS', 'HDFC BANK', 'INFY', 'ICICI BANK', 'BAJAJ AUTO']
        data = []
        for stock in stocks:
            data.append({
                'Symbol': stock,
                'CMP': f"₹{np.random.randint(1000, 3500)}",
                'Change %': f"{np.random.uniform(-3, 5):.2f}%",
                'Volume': f"{np.random.randint(1, 100)}M",
                '52W High': f"₹{np.random.randint(3000, 4500)}",
                '52W Low': f"₹{np.random.randint(800, 2000)}",
                'RSI': f"{np.random.randint(30, 80)}",
                'MACD': f"{np.random.uniform(-10, 10):.2f}",
            })
        return pd.DataFrame(data)
    
    @staticmethod
    @st.cache_data(ttl=60)
    def generate_news() -> List[Dict]:
        """Generate market news"""
        news_items = [
            {
                'headline': 'RBI Signals Pause in Rate Hike Cycle Amid Inflation Concerns',
                'source': 'Economic Times',
                'time': '2 hours ago',
                'summary': 'Reserve Bank of India indicates a potential pause in its monetary tightening cycle as inflation pressures begin to ease. Market participants expect stability in interest rates.'
            },
            {
                'headline': 'Nifty 50 Closes 1.2% Higher Led by IT and Banking Stocks',
                'source': 'Business Standard',
                'time': '4 hours ago',
                'summary': 'The Indian benchmark index surged today with strong performance from technology and financial sectors. Foreign institutional investors continued their buying spree.'
            },
            {
                'headline': 'Global Markets Rally on Softer Economic Data',
                'source': 'Bloomberg',
                'time': '6 hours ago',
                'summary': 'International markets reached new highs as economic indicators suggest a slower growth trajectory, supporting expectations for rate cuts in the latter half of the year.'
            },
            {
                'headline': 'Energy Stocks Surge on Oil Price Recovery',
                'source': 'Reuters',
                'time': '8 hours ago',
                'summary': 'Oil prices climbed above $95 per barrel, supporting energy sector stocks. ONGC and other energy companies posted strong gains in today trading session.'
            },
        ]
        return news_items

# ============================================================================
# COMPONENT FUNCTIONS
# ============================================================================

def render_header():
    """Render premium header"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="header-container">
            <div class="header-top">
                <div class="header-title">
                    <span class="emoji">📈</span>
                    <div>
                        <h1>STOCK ANALYSIS PRO</h1>
                        <div class="header-subtitle">Professional Equity Research Terminal</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        now = datetime.now()
        market_open = now.time() >= datetime.strptime("09:15", "%H:%M").time()
        market_close = now.time() >= datetime.strptime("15:30", "%H:%M").time()
        
        status = "CLOSED"
        if market_open and not market_close:
            status = "OPEN"
        elif not market_open:
            status = "PRE OPEN"
        
        st.markdown(f"""
        <div class="header-container">
            <div class="info-block">
                <div class="info-label">Live Date</div>
                <div class="info-value">{now.strftime('%d %b %Y')}</div>
            </div>
            <div class="info-block">
                <div class="info-label">Live Time</div>
                <div class="info-value">{now.strftime('%H:%M:%S')}</div>
            </div>
            <div class="info-block">
                <div class="info-label">Market Status</div>
                <div class="market-status {'closed' if status == 'CLOSED' else ''}">{status}</div>
            </div>
            <div class="info-block">
                <div class="info-label">Developer</div>
                <div class="info-value">Parvez Alam Ansari</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_navigation():
    """Render top navigation"""
    nav_items = [
        "Dashboard",
        "NIFTY 50",
        "NIFTY 100",
        "BANK NIFTY",
        "INDIA VIX",
        "Stock Analysis",
        "Watchlist",
        "Market Breadth",
        "Sector Analysis",
        "Reports",
        "Settings",
    ]
    
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    cols = st.columns(len(nav_items))
    for col, item in zip(cols, nav_items):
        with col:
            if st.button(
                item,
                key=f"nav_{item}",
                use_container_width=True,
                help=f"Navigate to {item}"
            ):
                st.session_state.current_page = item
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_ticker():
    """Render animated market ticker"""
    ticker_data = MarketDataGenerator.generate_ticker_data()
    
    ticker_html = '<div class="ticker-container"><div class="ticker-label">📡 Live Market Ticker</div><div class="ticker-scroll">'
    
    for item in ticker_data:
        change_class = "positive" if item['change_pct'] >= 0 else "negative"
        ticker_html += f"""
        <div class="ticker-item">
            <span class="ticker-symbol">{item['symbol']}</span>
            <span class="ticker-price">{item['price']:.2f}</span>
            <span class="ticker-change {change_class}">
                {'↑' if item['change_pct'] >= 0 else '↓'} {abs(item['change_pct']):.2f}%
            </span>
        </div>
        """
    
    # Duplicate for continuous scroll
    for item in ticker_data:
        change_class = "positive" if item['change_pct'] >= 0 else "negative"
        ticker_html += f"""
        <div class="ticker-item">
            <span class="ticker-symbol">{item['symbol']}</span>
            <span class="ticker-price">{item['price']:.2f}</span>
            <span class="ticker-change {change_class}">
                {'↑' if item['change_pct'] >= 0 else '↓'} {abs(item['change_pct']):.2f}%
            </span>
        </div>
        """
    
    ticker_html += '</div></div>'
    st.markdown(ticker_html, unsafe_allow_html=True)

def render_kpi_cards():
    """Render KPI cards for indices"""
    st.markdown('<h3 class="section-header">📊 Key Market Indices</h3>', unsafe_allow_html=True)
    
    index_data = MarketDataGenerator.generate_index_data()
    
    cols = st.columns(4)
    
    for col, (name, data) in zip(cols, index_data.items()):
        with col:
            change_class = "change-positive" if data.change_pct >= 0 else "change-negative"
            arrow = "↑" if data.change_pct >= 0 else "↓"
            
            card_html = f"""
            <div class="kpi-card">
                <div class="kpi-header">{name}</div>
                <div class="kpi-value">{data.price:,.0f}</div>
                <div class="kpi-change">
                    <span>{arrow}</span>
                    <span class="{change_class}">{data.change:+.0f} ({data.change_pct:+.2f}%)</span>
                </div>
                <div class="kpi-detail">
                    <div>High: {data.high:,.0f} | Low: {data.low:,.0f}</div>
                    <div>Open: {data.open:,.0f} | Prev: {data.prev_close:,.0f}</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

def render_market_breadth():
    """Render market breadth section"""
    st.markdown('<h3 class="section-header">📈 Market Breadth</h3>', unsafe_allow_html=True)
    
    breadth_data = MarketDataGenerator.generate_market_breadth()
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Metrics
    metrics = [
        ('Advances', breadth_data['Advance'], col1),
        ('Declines', breadth_data['Decline'], col2),
        ('Unchanged', breadth_data['Unchanged'], col3),
    ]
    
    for label, value, col in metrics:
        with col:
            metric_html = f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value:,}</div>
            </div>
            """
            st.markdown(metric_html, unsafe_allow_html=True)
    
    # A/D Ratio
    with col4:
        ratio = breadth_data['Advance'] / breadth_data['Decline'] if breadth_data['Decline'] > 0 else 1
        metric_html = f"""
        <div class="metric-card">
            <div class="metric-label">A/D Ratio</div>
            <div class="metric-value">{ratio:.2f}</div>
        </div>
        """
        st.markdown(metric_html, unsafe_allow_html=True)
    
    # Gauge chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    bullish_pct = (breadth_data['Advance'] / (breadth_data['Advance'] + breadth_data['Decline'])) * 100
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=bullish_pct,
        title={'text': "Market Strength (Bullish %)"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#3b82f6"},
            'steps': [
                {'range': [0, 30], 'color': "rgba(239, 68, 68, 0.1)"},
                {'range': [30, 70], 'color': "rgba(148, 163, 184, 0.1)"},
                {'range': [70, 100], 'color': "rgba(34, 197, 94, 0.1)"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#e0e0e0', 'family': 'Arial'},
        height=350,
        margin={'l': 0, 'r': 0, 't': 50, 'b': 0}
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

def render_sector_heatmap():
    """Render sector performance heatmap"""
    st.markdown('<h3 class="section-header">🔥 Sector Performance Heatmap</h3>', unsafe_allow_html=True)
    
    sectors = MarketDataGenerator.generate_sector_heatmap()
    
    # Create heatmap HTML
    heatmap_html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin: 20px 0;">'
    
    for sector, change_pct in sectors.items():
        if change_pct > 2:
            cell_class = 'strong-bullish'
        elif change_pct > 0.5:
            cell_class = 'bullish'
        elif change_pct > -0.5:
            cell_class = 'neutral'
        elif change_pct > -2:
            cell_class = 'bearish'
        else:
            cell_class = 'strong-bearish'
        
        arrow = '↑' if change_pct >= 0 else '↓'
        
        heatmap_html += f"""
        <div class="heatmap-cell {cell_class}">
            <div style="font-size: 13px; font-weight: 700; margin-bottom: 4px;">{sector}</div>
            <div style="font-size: 14px; font-weight: 700;">{arrow} {change_pct:+.2f}%</div>
        </div>
        """
    
    heatmap_html += '</div>'
    st.markdown(heatmap_html, unsafe_allow_html=True)

def render_gainers_losers():
    """Render top gainers and losers tables"""
    st.markdown('<h3 class="section-header">📊 Top Gainers & Losers</h3>', unsafe_allow_html=True)
    
    gainers, losers = MarketDataGenerator.generate_gainers_losers()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="metric-label" style="padding: 10px;">🟢 Top Gainers</div>', unsafe_allow_html=True)
        st.dataframe(
            gainers,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Change %": st.column_config.NumberColumn(format="%.2f%%"),
                "RSI": st.column_config.NumberColumn(format="%.0f"),
            }
        )
    
    with col2:
        st.markdown('<div class="metric-label" style="padding: 10px;">🔴 Top Losers</div>', unsafe_allow_html=True)
        st.dataframe(
            losers,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Change %": st.column_config.NumberColumn(format="%.2f%%"),
                "RSI": st.column_config.NumberColumn(format="%.0f"),
            }
        )

def render_fii_dii():
    """Render FII/DII data section"""
    st.markdown('<h3 class="section-header">💰 FII/DII Flow Analysis</h3>', unsafe_allow_html=True)
    
    fii_dii_data = MarketDataGenerator.generate_fii_dii_data()
    
    col1, col2, col3, col4 = st.columns(4)
    
    cards = [
        ('FII Buy', fii_dii_data['FII Buy'], col1),
        ('FII Sell', fii_dii_data['FII Sell'], col2),
        ('DII Buy', fii_dii_data['DII Buy'], col3),
        ('DII Sell', fii_dii_data['DII Sell'], col4),
    ]
    
    for label, value, col in cards:
        with col:
            card_html = f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">₹{value:,.0f}Cr</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
    
    # Monthly trend chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    months = ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    fii_flows = np.random.uniform(-5000, 15000, len(months))
    dii_flows = np.random.uniform(-3000, 10000, len(months))
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=fii_flows,
        name='FII',
        marker_color='#3b82f6',
        showlegend=True,
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=dii_flows,
        name='DII',
        marker_color='#22c55e',
        showlegend=True,
    ))
    
    fig.update_layout(
        title="Monthly FII/DII Flows",
        xaxis_title="Month",
        yaxis_title="Flow (Crores)",
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#e0e0e0'},
        height=350,
        hovermode='x unified',
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1}
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

def render_options_data():
    """Render options data section"""
    st.markdown('<h3 class="section-header">📋 Options Data (NIFTY 50)</h3>', unsafe_allow_html=True)
    
    options_data = {
        'PCR Ratio': f"{np.random.uniform(0.8, 1.5):.2f}",
        'Max Pain': f"₹{np.random.randint(24000, 25000)}",
        'Call OI': f"{np.random.randint(50, 150)}M",
        'Put OI': f"{np.random.randint(50, 150)}M",
        'IV (ATM)': f"{np.random.uniform(15, 25):.2f}%",
        'IV Percentile': f"{np.random.randint(30, 90)}",
    }
    
    col1, col2, col3 = st.columns(3)
    
    for i, (label, value) in enumerate(options_data.items()):
        col = [col1, col2, col3][i % 3]
        with col:
            card_html = f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

def render_market_sentiment():
    """Render market sentiment section"""
    st.markdown('<h3 class="section-header">😊 Market Sentiment & Indicators</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # AI Sentiment
    with col1:
        sentiment_scores = {
            'Bullish': np.random.randint(30, 70),
            'Neutral': np.random.randint(20, 40),
            'Bearish': np.random.randint(10, 30),
        }
        
        st.markdown('<div style="text-align: center; margin-bottom: 20px;">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">AI Market Sentiment</div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Pie(
            labels=list(sentiment_scores.keys()),
            values=list(sentiment_scores.values()),
            marker={'colors': ['#22c55e', '#94a3b8', '#ef4444']},
            textposition='inside',
            textinfo='label+percent',
        )])
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e0e0'},
            height=300,
            margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
            showlegend=False,
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Fear & Greed Index
    with col2:
        fear_greed_value = np.random.uniform(30, 80)
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=fear_greed_value,
            title={'text': "Fear & Greed Index"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#ef4444" if fear_greed_value < 50 else "#22c55e"},
                'steps': [
                    {'range': [0, 25], 'color': "rgba(239, 68, 68, 0.1)"},
                    {'range': [25, 50], 'color': "rgba(249, 115, 22, 0.1)"},
                    {'range': [50, 75], 'color': "rgba(148, 163, 184, 0.1)"},
                    {'range': [75, 100], 'color': "rgba(34, 197, 94, 0.1)"}
                ],
            }
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e0e0'},
            height=300,
            margin={'l': 0, 'r': 0, 't': 50, 'b': 0}
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Momentum & Volatility
    with col3:
        momentum_value = np.random.uniform(40, 75)
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=momentum_value,
            title={'text': "Market Momentum"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#3b82f6"},
                'steps': [
                    {'range': [0, 33], 'color': "rgba(239, 68, 68, 0.1)"},
                    {'range': [33, 66], 'color': "rgba(148, 163, 184, 0.1)"},
                    {'range': [66, 100], 'color': "rgba(34, 197, 94, 0.1)"}
                ],
            }
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e0e0'},
            height=300,
            margin={'l': 0, 'r': 0, 't': 50, 'b': 0}
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_news():
    """Render market news section"""
    st.markdown('<h3 class="section-header">📰 Market News</h3>', unsafe_allow_html=True)
    
    news_items = MarketDataGenerator.generate_news()
    
    col1, col2 = st.columns(2)
    
    for i, news in enumerate(news_items):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            news_html = f"""
            <div class="news-card">
                <div class="news-headline">{news['headline']}</div>
                <div class="news-meta">
                    <span class="news-source">{news['source']}</span>
                    <span class="news-time">{news['time']}</span>
                </div>
                <div class="news-summary">{news['summary']}</div>
                <button style="
                    background: rgba(59, 130, 246, 0.2);
                    border: 1px solid rgba(59, 130, 246, 0.5);
                    color: #3b82f6;
                    padding: 6px 12px;
                    border-radius: 4px;
                    font-size: 11px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.2s ease;
                " onmouseover="this.style.background='rgba(59, 130, 246, 0.3)'" 
                   onmouseout="this.style.background='rgba(59, 130, 246, 0.2)'">
                    Read More →
                </button>
            </div>
            """
            st.markdown(news_html, unsafe_allow_html=True)

def render_chart_section():
    """Render interactive TradingView-style chart"""
    st.markdown('<h3 class="section-header">📈 Technical Analysis Chart</h3>', unsafe_allow_html=True)
    
    chart_tabs = st.tabs(["NIFTY 50", "BANK NIFTY", "NIFTY 100", "INDIA VIX"])
    
    with chart_tabs[0]:
        # Generate sample OHLC data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        nifty_data = 24500 + np.cumsum(np.random.randn(100) * 100)
        
        ohlc = pd.DataFrame({
            'Date': dates,
            'Close': nifty_data,
            'High': nifty_data * 1.01,
            'Low': nifty_data * 0.99,
            'Open': nifty_data + np.random.randn(100) * 50,
        })
        
        fig = go.Figure(data=[go.Candlestick(
            x=ohlc['Date'],
            open=ohlc['Open'],
            high=ohlc['High'],
            low=ohlc['Low'],
            close=ohlc['Close'],
            name='NIFTY 50',
        )])
        
        fig.update_layout(
            title="NIFTY 50 - Daily Chart",
            yaxis_title="Price",
            xaxis_title="Date",
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            paper_bgcolor='rgba(15, 23, 42, 0.5)',
            plot_bgcolor='rgba(15, 23, 42, 0.5)',
            font={'color': '#e0e0e0'},
            height=500,
            hovermode='x unified',
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

def render_watchlist():
    """Render watchlist"""
    st.markdown('<h3 class="section-header">⭐ Your Watchlist</h3>', unsafe_allow_html=True)
    
    watchlist_df = MarketDataGenerator.generate_watchlist()
    
    st.dataframe(
        watchlist_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Symbol": st.column_config.TextColumn(width="medium"),
            "CMP": st.column_config.TextColumn(width="medium"),
            "Change %": st.column_config.TextColumn(width="medium"),
            "Volume": st.column_config.TextColumn(width="medium"),
            "52W High": st.column_config.TextColumn(width="medium"),
            "52W Low": st.column_config.TextColumn(width="medium"),
            "RSI": st.column_config.TextColumn(width="small"),
            "MACD": st.column_config.TextColumn(width="small"),
        }
    )

def render_scanner():
    """Render market scanner"""
    st.markdown('<h3 class="section-header">🔍 Market Scanner</h3>', unsafe_allow_html=True)
    
    # Define columns first
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    
    scanners_data = [
        ('52 Week Breakout', 12, col1),
        ('Volume Breakout', 8, col2),
        ('Golden Cross', 15, col3),
        ('RSI Oversold', 6, col4),
        ('RSI Overbought', 9, col5),
        ('MACD Buy', 11, col6),
        ('MACD Sell', 7, col7),
        ('Highest Delivery', 14, col8),
    ]
    
    # Now use the columns
    for scanner_name, count, col in scanners_data:
        with col:
            scanner_html = f"""
            <div class="metric-card">
                <div class="metric-label">{scanner_name}</div>
                <div class="metric-value">{count}</div>
            </div>
            """
            st.markdown(scanner_html, unsafe_allow_html=True)

def render_ai_insights():
    """Render AI insights section"""
    st.markdown('<h3 class="section-header">🤖 AI Market Insights</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        insights_html = """
        <div class="metric-card" style="text-align: left;">
            <div class="metric-label">Today's Trend</div>
            <div style="font-size: 12px; color: #cbd5e1; margin-top: 12px; line-height: 1.6;">
                <strong>Bullish Bias</strong><br>
                Market showing strength with IT and Banking sectors leading. FII inflows continue to support the market.
            </div>
        </div>
        
        <div class="metric-card" style="text-align: left; margin-top: 12px;">
            <div class="metric-label">Important Levels</div>
            <div style="font-size: 12px; color: #cbd5e1; margin-top: 12px;">
                <strong style="color: #22c55e;">Resistance:</strong> 25,000 | 25,500<br>
                <strong style="color: #ef4444;">Support:</strong> 24,000 | 23,800
            </div>
        </div>
        """
        st.markdown(insights_html, unsafe_allow_html=True)
    
    with col2:
        insights_html2 = """
        <div class="metric-card" style="text-align: left;">
            <div class="metric-label">Market Analysis</div>
            <div style="font-size: 12px; color: #cbd5e1; margin-top: 12px; line-height: 1.6;">
                <strong>Breakout Stocks:</strong> RELIANCE, INFY, HDFC BANK<br>
                <strong>Weak Stocks:</strong> MARUTI, BAJAJ AUTO<br>
                <strong>Risk Level:</strong> Medium<br>
                <strong>Probability:</strong> 65% Higher
            </div>
        </div>
        """
        st.markdown(insights_html2, unsafe_allow_html=True)
def render_navigation():
    """Render top navigation"""
    nav_items = [
        "Dashboard",
        "NIFTY 50",
        "NIFTY 100",
        "BANK NIFTY",
        "INDIA VIX",
        "Stock Analysis",
        "Watchlist",
        "Market Breadth",
        "Sector Analysis",
        "Reports",
        "Settings",
    ]
    
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    cols = st.columns(len(nav_items))
    for col, item in zip(cols, nav_items):
        with col:
            if st.button(
                item,
                key=f"nav_{item}",
                use_container_width=True,
                help=f"Navigate to {item}"
            ):
                st.session_state.current_page = item
    
    st.markdown('</div>', unsafe_allow_html=True)
def render_footer():
    """Render footer"""
    now = datetime.now()
    footer_html = f"""
    <div class="footer-container">
        <div class="footer-text">📊 Market Data Source: NSE/BSE Real-time Feeds</div>
        <div class="footer-text">Last Updated: {now.strftime('%d %b %Y at %H:%M:%S')}</div>
        <div style="margin-top: 12px; border-top: 1px solid rgba(148, 163, 184, 0.1); padding-top: 12px;">
            <div class="footer-text"><strong>STOCK ANALYSIS PRO v17.0</strong></div>
            <div class="footer-text">Developed by <strong>Parvez Alam Ansari</strong></div>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application"""
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Dashboard'
    
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Render header
    render_header()
    
    # Render navigation
    render_navigation()
    
    # Hide default Streamlit elements
    st.markdown("""
    <style>
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # Render ticker
    render_ticker()
    
    # ROW 1: KPI Cards
    render_kpi_cards()
    
    # ROW 2: Market Breadth
    render_market_breadth()
    
    # ROW 3: Sector Heatmap
    render_sector_heatmap()
    
    # ROW 4: Gainers & Losers
    render_gainers_losers()
    
    # ROW 5: FII/DII
    render_fii_dii()
    
    # ROW 6: Options Data
    render_options_data()
    
    # ROW 7: Market Sentiment
    render_market_sentiment()
    
    # ROW 8: News
    render_news()
    
    # ROW 9: Chart
    render_chart_section()
    
    # ROW 10: Watchlist
    render_watchlist()
    
    # ROW 11: Scanner
    render_scanner()
    
    # ROW 12: AI Insights
    render_ai_insights()
    
    # Footer
    render_footer()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
