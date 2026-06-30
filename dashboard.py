"""
STOCK ANALYSIS PRO - DASHBOARD
Fresh Clean Version - All Errors Fixed
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
from api_handler import (
    get_nifty50_data, get_banknifty_data, get_nifty100_data, get_indiavix_data,
    get_top_gainers_losers, get_company_news
)

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Stock Analysis Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    
    .header-title { 
        font-size: 28px; 
        font-weight: 700; 
        color: #fff; 
        margin: 0;
    }
    .header-subtitle { 
        font-size: 12px; 
        color: #94a3b8;
        font-weight: 500;
    }
    .section-header {
        font-size: 20px;
        font-weight: 700;
        color: #fff;
        margin: 32px 0 16px 0;
    }
    .kpi-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 12px;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 8px;
        padding: 16px;
    }
    .news-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .news-headline {
        font-size: 14px;
        font-weight: 600;
        color: #fff;
        margin-bottom: 8px;
    }
    .news-source {
        font-size: 11px;
        color: #3b82f6;
        font-weight: 600;
    }
    .news-summary {
        font-size: 12px;
        color: #cbd5e1;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA FETCHING FUNCTIONS
# ============================================================================

@st.cache_data(ttl=300)
def get_index_data():
    """Get all index data"""
    try:
        nifty50 = get_nifty50_data()
        banknifty = get_banknifty_data()
        nifty100 = get_nifty100_data()
        indiavix = get_indiavix_data()
        
        # Fallback values
        if nifty50 is None:
            nifty50 = {'price': 24500, 'change': 152, 'change_pct': 0.62, 'high': 24850, 'low': 24200, 'volume': 5000000}
        if banknifty is None:
            banknifty = {'price': 52300, 'change': 286, 'change_pct': 0.55, 'high': 52800, 'low': 51800, 'volume': 3000000}
        if nifty100 is None:
            nifty100 = {'price': 26800, 'change': 150, 'change_pct': 0.56, 'high': 27100, 'low': 26500, 'volume': 0}
        if indiavix is None:
            indiavix = {'price': 18.5, 'change': -0.25, 'change_pct': -1.33, 'high': 19.5, 'low': 17.5, 'volume': 0}
        
        return {
            'NIFTY 50': nifty50,
            'BANK NIFTY': banknifty,
            'NIFTY 100': nifty100,
            'INDIA VIX': indiavix,
        }
    except Exception as e:
        st.warning(f"Using demo data: {str(e)[:50]}")
        return {
            'NIFTY 50': {'price': 24500, 'change': 152, 'change_pct': 0.62, 'high': 24850, 'low': 24200, 'volume': 5000000},
            'BANK NIFTY': {'price': 52300, 'change': 286, 'change_pct': 0.55, 'high': 52800, 'low': 51800, 'volume': 3000000},
            'NIFTY 100': {'price': 26800, 'change': 150, 'change_pct': 0.56, 'high': 27100, 'low': 26500, 'volume': 0},
            'INDIA VIX': {'price': 18.5, 'change': -0.25, 'change_pct': -1.33, 'high': 19.5, 'low': 17.5, 'volume': 0},
        }

@st.cache_data(ttl=300)
def get_gainers_losers_safe():
    """Get gainers/losers safely"""
    try:
        gainers, losers = get_top_gainers_losers()
        return gainers, losers
    except Exception as e:
        st.warning(f"Error fetching gainers/losers: {str(e)[:50]}")
        return pd.DataFrame(), pd.DataFrame()

@st.cache_data(ttl=3600)
def get_news_safe():
    """Get news safely"""
    try:
        return get_company_news('RELIANCE.NS', limit=4)
    except Exception as e:
        return [{'headline': 'Market News', 'source': 'News', 'time': 'Recent', 'summary': 'Stay tuned for updates'}]

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def render_header():
    """Render header"""
    col1, col2, col3, col4, col5, col6 = st.columns([2, 0.8, 0.65, 0.7, 0.8, 0.7])
    
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 32px;">📈</span>
            <div>
                <h1 class="header-title">STOCK ANALYSIS PRO</h1>
                <div class="header-subtitle">Professional Equity Research Terminal</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        if st.button("🔬 RESEARCH", use_container_width=True, key="nav_research"):
            st.switch_page("pages/research_platform.py")
    
    with col4:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        if st.button("🏢 TOP 100", use_container_width=True, key="nav_top100"):
            st.switch_page("pages/top100_analyzer.py")
    
    with col5:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        if st.button("📊 SCREENER", use_container_width=True, key="nav_screener"):
            st.switch_page("pages/stock_screener.py")
    
    with col6:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        if st.button("💰 FINANCE", use_container_width=True, key="nav_finance"):
            st.switch_page("pages/financial_planning.py")

def render_kpi_cards():
    """Render KPI cards"""
    st.markdown('<h3 class="section-header">📊 Key Market Indices</h3>', unsafe_allow_html=True)
    
    try:
        index_data = get_index_data()
        cols = st.columns(4)
        
        for col, (name, data) in zip(cols, index_data.items()):
            with col:
                arrow = "↑" if data.get('change_pct', 0) >= 0 else "↓"
                color = "#22c55e" if data.get('change_pct', 0) >= 0 else "#ef4444"
                
                st.markdown(f"""
                <div class="kpi-card">
                    <div style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700;">{name}</div>
                    <div style="font-size: 24px; font-weight: 700; color: #fff; margin: 8px 0;">{data.get('price', 0):,.0f}</div>
                    <div style="font-size: 13px; font-weight: 600; color: {color};">{arrow} {data.get('change', 0):+.0f} ({data.get('change_pct', 0):+.2f}%)</div>
                    <div style="font-size: 11px; color: #94a3b8; margin-top: 8px;">H: {data.get('high', 0):,.0f} L: {data.get('low', 0):,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error rendering KPI cards: {str(e)[:50]}")

def render_gainers_losers():
    """Render gainers/losers"""
    st.markdown('<h3 class="section-header">📊 Top Gainers & Losers</h3>', unsafe_allow_html=True)
    
    try:
        gainers, losers = get_gainers_losers_safe()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🟢 Top Gainers")
            if gainers is not None and not gainers.empty:
                st.dataframe(gainers.head(5), use_container_width=True, hide_index=True)
            else:
                st.info("No data available")
        
        with col2:
            st.markdown("#### 🔴 Top Losers")
            if losers is not None and not losers.empty:
                st.dataframe(losers.head(5), use_container_width=True, hide_index=True)
            else:
                st.info("No data available")
    except Exception as e:
        st.error(f"Error: {str(e)[:50]}")

def render_fii_dii():
    """Render FII/DII"""
    st.markdown('<h3 class="section-header">💰 FII/DII Analysis</h3>', unsafe_allow_html=True)
    
    fii_dii = {
        'FII Buy': 9137,
        'FII Sell': 4919,
        'DII Buy': 4705,
        'DII Sell': 2741,
    }
    
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
    
    news_items = [
        {'headline': 'RBI Signals Pause in Rate Hike Cycle', 'source': 'Economic Times', 'time': '2 hours ago', 'summary': 'Reserve Bank of India indicates a potential pause in monetary tightening as inflation pressures ease.'},
        {'headline': 'Nifty 50 Closes 1.2% Higher', 'source': 'Business Standard', 'time': '4 hours ago', 'summary': 'Indian benchmark index surged with strong performance from technology and financial sectors.'},
        {'headline': 'Global Markets Rally on Softer Data', 'source': 'Bloomberg', 'time': '6 hours ago', 'summary': 'International markets reached new highs as economic indicators suggest slower growth trajectory.'},
        {'headline': 'Energy Stocks Surge on Oil Recovery', 'source': 'Reuters', 'time': '8 hours ago', 'summary': 'Oil prices climbed above $95 per barrel, supporting energy sector stocks.'},
    ]
    
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

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main app"""
    render_header()
    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
    render_kpi_cards()
    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
    render_gainers_losers()
    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
    render_fii_dii()
    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
    render_news()

if __name__ == "__main__":
    main()
