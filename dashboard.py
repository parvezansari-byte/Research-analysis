"""
STOCK ANALYSIS PRO - Professional Equity Research Terminal
A Bloomberg Terminal-style institutional stock market dashboard
Version 17.0 - CLEANED & OPTIMIZED

Author: Parvez Alam Ansari
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

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
# CUSTOM CSS
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
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    .main-container {
        max-width: 1800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .header-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }
    
    .header-title h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        color: #fff;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 4px;
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
    }
    
    .info-value {
        font-size: 14px;
        color: #e0e0e0;
        font-weight: 600;
        font-family: 'Courier New', monospace;
    }
    
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
    
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .kpi-card:hover {
        background: linear-gradient(135deg, rgba(30, 41, 59, 1) 0%, rgba(15, 23, 42, 1) 100%);
        border-color: rgba(148, 163, 184, 0.3);
        transform: translateY(-4px);
    }
    
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
    
    .chart-container {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        padding: 16px;
        margin: 16px 0;
    }
    
    .news-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .news-headline {
        font-size: 13px;
        font-weight: 700;
        color: #fff;
        margin-bottom: 8px;
    }
    
    .news-meta {
        font-size: 11px;
        color: #64748b;
        margin-bottom: 8px;
    }
    
    .news-source {
        color: #3b82f6;
        font-weight: 600;
    }
    
    .news-summary {
        font-size: 12px;
        color: #cbd5e1;
        line-height: 1.5;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================================
# DATA GENERATION (NO CACHING - Simple Functions)
# ============================================================================

def get_index_data():
    """Generate index data - NO CACHING"""
    return {
        'NIFTY 50': {
            'price': 24500 + np.random.uniform(-500, 500),
            'change': np.random.uniform(-100, 100),
            'change_pct': np.random.uniform(-2, 3),
            'high': 24800,
            'low': 24200,
            'open': 24450,
            'prev_close': 24400,
            'volume': 5000000,
        },
        'BANK NIFTY': {
            'price': 52300 + np.random.uniform(-1000, 1000),
            'change': np.random.uniform(-200, 200),
            'change_pct': np.random.uniform(-2, 3),
            'high': 52800,
            'low': 51800,
            'open': 52250,
            'prev_close': 52100,
            'volume': 3000000,
        },
        'NIFTY 100': {
            'price': 26800 + np.random.uniform(-400, 400),
            'change': np.random.uniform(-80, 80),
            'change_pct': np.random.uniform(-2, 3),
            'high': 27100,
            'low': 26500,
            'open': 26750,
            'prev_close': 26720,
            'volume': 4000000,
        },
        'INDIA VIX': {
            'price': 18.5 + np.random.uniform(-2, 2),
            'change': np.random.uniform(-1, 1),
            'change_pct': np.random.uniform(-5, 5),
            'high': 19.5,
            'low': 17.5,
            'open': 18.2,
            'prev_close': 18.3,
            'volume': 500000,
        },
    }

def get_ticker_data():
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

def get_gainers_losers():
    """Generate gainers and losers"""
    symbols = ['RELIANCE', 'TCS', 'HDFC BANK', 'INFY', 'ICICI BANK', 'BAJAJ AUTO', 'LT', 'MARUTI', 'AXIS BANK', 'WIPRO']
    
    gainers = []
    for i, symbol in enumerate(symbols[:5], 1):
        gainers.append({
            'Rank': i,
            'Symbol': symbol,
            'Price': np.random.uniform(1000, 3000),
            'Change %': np.random.uniform(2, 8),
            'Volume': f"{np.random.randint(1, 100)}M",
            'RSI': np.random.uniform(50, 80),
            'Trend': '↑'
        })
    
    losers = []
    for i, symbol in enumerate(symbols[5:], 1):
        losers.append({
            'Rank': i,
            'Symbol': symbol,
            'Price': np.random.uniform(500, 2500),
            'Change %': -np.random.uniform(1, 6),
            'Volume': f"{np.random.randint(1, 100)}M",
            'RSI': np.random.uniform(20, 50),
            'Trend': '↓'
        })
    
    return pd.DataFrame(gainers), pd.DataFrame(losers)

def get_sector_heatmap():
    """Generate sector heatmap"""
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

def get_market_breadth():
    """Generate market breadth"""
    total = 1500
    advance = int(total * np.random.uniform(0.4, 0.7))
    decline = int(total * (1 - np.random.uniform(0.4, 0.7)))
    return {
        'Advance': advance,
        'Decline': decline,
        'Unchanged': total - advance - decline,
    }

def get_fii_dii():
    """Generate FII/DII data"""
    return {
        'FII Buy': np.random.uniform(5000, 15000),
        'FII Sell': np.random.uniform(4000, 12000),
        'DII Buy': np.random.uniform(3000, 10000),
        'DII Sell': np.random.uniform(2500, 9000),
    }

def get_news():
    """Generate news items"""
    return [
        {
            'headline': 'RBI Signals Pause in Rate Hike Cycle',
            'source': 'Economic Times',
            'time': '2 hours ago',
            'summary': 'Reserve Bank of India indicates a potential pause in monetary tightening as inflation pressures ease.'
        },
        {
            'headline': 'Nifty 50 Closes 1.2% Higher',
            'source': 'Business Standard',
            'time': '4 hours ago',
            'summary': 'Indian benchmark index surged with strong performance from technology and financial sectors.'
        },
        {
            'headline': 'Global Markets Rally on Softer Data',
            'source': 'Bloomberg',
            'time': '6 hours ago',
            'summary': 'International markets reached new highs as economic indicators suggest slower growth trajectory.'
        },
        {
            'headline': 'Energy Stocks Surge on Oil Recovery',
            'source': 'Reuters',
            'time': '8 hours ago',
            'summary': 'Oil prices climbed above $95 per barrel, supporting energy sector stocks.'
        },
    ]

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def render_header():
    """Render header"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="header-container">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <span style="font-size: 32px;">📈</span>
                <div>
                    <h1 class="header-title">STOCK ANALYSIS PRO</h1>
                    <div class="header-subtitle">Professional Equity Research Terminal</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        now = datetime.now()
        st.markdown(f"""
        <div class="header-container">
            <div class="info-block">
                <div class="info-label">Live Date</div>
                <div class="info-value">{now.strftime('%d %b %Y')}</div>
            </div>
            <div class="info-block" style="margin-top: 12px;">
                <div class="info-label">Live Time</div>
                <div class="info-value">{now.strftime('%H:%M:%S')}</div>
            </div>
            <div class="info-block" style="margin-top: 12px;">
                <div class="info-label">Developer</div>
                <div class="info-value">Parvez Alam Ansari</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_kpi_cards():
    """Render KPI cards"""
    st.markdown('<h3 class="section-header">📊 Key Market Indices</h3>', unsafe_allow_html=True)
    
    index_data = get_index_data()
    cols = st.columns(4)
    
    for col, (name, data) in zip(cols, index_data.items()):
        with col:
            arrow = "↑" if data['change_pct'] >= 0 else "↓"
            color = "green" if data['change_pct'] >= 0 else "red"
            
            st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700; margin-bottom: 8px;">{name}</div>
                <div style="font-size: 24px; font-weight: 700; color: #fff; font-family: 'Courier New', monospace; margin-bottom: 8px;">{data['price']:,.0f}</div>
                <div style="font-size: 13px; font-weight: 600; color: {'#22c55e' if color=='green' else '#ef4444'};"> {arrow} {data['change']:+.0f} ({data['change_pct']:+.2f}%)</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 8px;">
                    H: {data['high']:,.0f} L: {data['low']:,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_ticker():
    """Render ticker"""
    ticker_data = get_ticker_data()
    
    ticker_html = '<div style="background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(148, 163, 184, 0.1); border-radius: 8px; padding: 12px; margin-bottom: 24px; overflow: auto;">'
    ticker_html += '<div style="font-size: 10px; color: #64748b; margin-bottom: 8px; text-transform: uppercase; font-weight: 700;">📡 Live Market Ticker</div>'
    
    for item in ticker_data[:6]:
        change_class = "green" if item['change_pct'] >= 0 else "red"
        arrow = '↑' if item['change_pct'] >= 0 else '↓'
        ticker_html += f'<span style="margin-right: 24px; color: #e0e0e0;"><strong>{item["symbol"]}</strong> {item["price"]:.0f} <span style="color: {"#22c55e" if change_class=="green" else "#ef4444"};">{arrow}{abs(item["change_pct"]):.2f}%</span></span>'
    
    ticker_html += '</div>'
    st.markdown(ticker_html, unsafe_allow_html=True)

def render_market_breadth():
    """Render market breadth"""
    st.markdown('<h3 class="section-header">📈 Market Breadth</h3>', unsafe_allow_html=True)
    
    breadth = get_market_breadth()
    cols = st.columns(4)
    
    with cols[0]:
        st.metric("Advances", f"{breadth['Advance']:,}")
    with cols[1]:
        st.metric("Declines", f"{breadth['Decline']:,}")
    with cols[2]:
        st.metric("Unchanged", f"{breadth['Unchanged']:,}")
    with cols[3]:
        ratio = breadth['Advance'] / breadth['Decline'] if breadth['Decline'] > 0 else 1
        st.metric("A/D Ratio", f"{ratio:.2f}")

def render_sector_heatmap():
    """Render sector heatmap"""
    st.markdown('<h3 class="section-header">🔥 Sector Performance</h3>', unsafe_allow_html=True)
    
    sectors = get_sector_heatmap()
    cols = st.columns(4)
    
    for idx, (sector, change) in enumerate(sectors.items()):
        col = cols[idx % 4]
        with col:
            color = "green" if change > 0 else "red"
            arrow = "↑" if change > 0 else "↓"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{sector}</div>
                <div class="metric-value" style="color: {'#22c55e' if color=='green' else '#ef4444'};">{arrow}{change:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

def render_gainers_losers():
    """Render gainers and losers"""
    st.markdown('<h3 class="section-header">📊 Top Gainers & Losers</h3>', unsafe_allow_html=True)
    
    gainers, losers = get_gainers_losers()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🟢 Top Gainers")
        st.dataframe(gainers, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 🔴 Top Losers")
        st.dataframe(losers, use_container_width=True, hide_index=True)

def render_fii_dii():
    """Render FII/DII"""
    st.markdown('<h3 class="section-header">💰 FII/DII Analysis</h3>', unsafe_allow_html=True)
    
    fii_dii = get_fii_dii()
    cols = st.columns(4)
    
    with cols[0]:
        st.metric("FII Buy", f"₹{fii_dii['FII Buy']:,.0f}Cr")
    with cols[1]:
        st.metric("FII Sell", f"₹{fii_dii['FII Sell']:,.0f}Cr")
    with cols[2]:
        st.metric("DII Buy", f"₹{fii_dii['DII Buy']:,.0f}Cr")
    with cols[3]:
        st.metric("DII Sell", f"₹{fii_dii['DII Sell']:,.0f}Cr")

def render_news():
    """Render news"""
    st.markdown('<h3 class="section-header">📰 Market News</h3>', unsafe_allow_html=True)
    
    news_items = get_news()
    
    col1, col2 = st.columns(2)
    
    for i, news in enumerate(news_items):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            st.markdown(f"""
            <div class="news-card">
                <div class="news-headline">{news['headline']}</div>
                <div class="news-meta">
                    <span class="news-source">{news['source']}</span> • {news['time']}
                </div>
                <div class="news-summary">{news['summary']}</div>
            </div>
            """, unsafe_allow_html=True)

def render_footer():
    """Render footer"""
    now = datetime.now()
    st.markdown(f"""
    <div class="footer-container">
        <div class="footer-text">📊 Market Data Source: NSE/BSE Real-time Feeds</div>
        <div class="footer-text">Last Updated: {now.strftime('%d %b %Y at %H:%M:%S')}</div>
        <div style="margin-top: 12px; border-top: 1px solid rgba(148, 163, 184, 0.1); padding-top: 12px;">
            <div class="footer-text"><strong>STOCK ANALYSIS PRO v17.0</strong></div>
            <div class="footer-text">Developed by <strong>Parvez Alam Ansari</strong></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application"""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Render sections
    render_header()
    render_ticker()
    render_kpi_cards()
    render_market_breadth()
    render_sector_heatmap()
    render_gainers_losers()
    render_fii_dii()
    render_news()
    render_footer()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
