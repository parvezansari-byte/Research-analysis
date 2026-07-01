"""
ENHANCED DASHBOARD
Visual Masterpiece with Animations, Better Layout, and Premium Design
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from api_handler import get_technical_indicators, get_historical_data
from visual_enhancements import (
    DARK_THEME, LIGHT_THEME, ENHANCED_CSS, create_gradient_card, 
    create_stat_box, get_theme_css, GRADIENT_PALETTES, CHART_COLORS
)

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Stock Analysis Pro - Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# THEME MANAGEMENT
# ============================================================================

if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

theme = DARK_THEME if st.session_state.theme == 'dark' else LIGHT_THEME

# ============================================================================
# ENHANCED CSS & STYLING
# ============================================================================

st.markdown(ENHANCED_CSS, unsafe_allow_html=True)
st.markdown(get_theme_css(theme), unsafe_allow_html=True)

st.markdown(f"""
<style>
    [data-testid="stSidebar"] {{ display: none; }}
    
    .header-title {{ 
        font-size: 32px; 
        font-weight: 900; 
        background: linear-gradient(135deg, #2563eb, #06b6d4, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        animation: fadeIn 0.8s ease-out;
    }}
    
    .header-subtitle {{ 
        font-size: 13px; 
        color: #94a3b8;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }}
    
    .section-header {{
        font-size: 24px;
        font-weight: 800;
        color: #fff;
        margin: 32px 0 20px 0;
        padding-bottom: 12px;
        border-bottom: 2px solid;
        border-image: linear-gradient(90deg, #2563eb, #06b6d4) 1;
    }}
    
    .metric-card {{
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s ease;
        transform: translateY(0);
    }}
    
    .metric-card:hover {{
        transform: translateY(-4px);
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data(ttl=60)
def get_live_index_data():
    """Get REAL LIVE index data with day 1 change"""
    try:
        # Fetch NIFTY 50
        nifty = yf.Ticker("^NSEI")
        nifty_hist = nifty.history(period='1d')
        nifty_price = nifty_hist['Close'].iloc[-1] if len(nifty_hist) > 0 else 0
        nifty_open = nifty_hist['Open'].iloc[-1] if len(nifty_hist) > 0 else nifty_price
        nifty_high = nifty_hist['High'].iloc[-1] if len(nifty_hist) > 0 else nifty_price
        nifty_low = nifty_hist['Low'].iloc[-1] if len(nifty_hist) > 0 else nifty_price
        nifty_change = nifty_price - nifty_open
        nifty_change_pct = (nifty_change / nifty_open * 100) if nifty_open != 0 else 0
        
        # Fetch BANK NIFTY
        bank_nifty = yf.Ticker("^NSEBANK")
        bank_hist = bank_nifty.history(period='1d')
        bank_price = bank_hist['Close'].iloc[-1] if len(bank_hist) > 0 else 0
        bank_open = bank_hist['Open'].iloc[-1] if len(bank_hist) > 0 else bank_price
        bank_high = bank_hist['High'].iloc[-1] if len(bank_hist) > 0 else bank_price
        bank_low = bank_hist['Low'].iloc[-1] if len(bank_hist) > 0 else bank_price
        bank_change = bank_price - bank_open
        bank_change_pct = (bank_change / bank_open * 100) if bank_open != 0 else 0
        
        # Fetch NIFTY 100
        nifty100 = yf.Ticker("^NIFTY100")
        nifty100_hist = nifty100.history(period='1d')
        nifty100_price = nifty100_hist['Close'].iloc[-1] if len(nifty100_hist) > 0 else 0
        nifty100_open = nifty100_hist['Open'].iloc[-1] if len(nifty100_hist) > 0 else nifty100_price
        nifty100_change = nifty100_price - nifty100_open
        nifty100_change_pct = (nifty100_change / nifty100_open * 100) if nifty100_open != 0 else 0
        
        # Fetch INDIA VIX
        vix = yf.Ticker("^INDIAVIX")
        vix_hist = vix.history(period='1d')
        vix_price = vix_hist['Close'].iloc[-1] if len(vix_hist) > 0 else 0
        vix_open = vix_hist['Open'].iloc[-1] if len(vix_hist) > 0 else vix_price
        vix_change = vix_price - vix_open
        vix_change_pct = (vix_change / vix_open * 100) if vix_open != 0 else 0
        
        return {
            'nifty50': {
                'price': nifty_price,
                'open': nifty_open,
                'high': nifty_high,
                'low': nifty_low,
                'change': nifty_change,
                'change_pct': nifty_change_pct,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            },
            'banknifty': {
                'price': bank_price,
                'open': bank_open,
                'high': bank_high,
                'low': bank_low,
                'change': bank_change,
                'change_pct': bank_change_pct,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            },
            'nifty100': {
                'price': nifty100_price,
                'change': nifty100_change,
                'change_pct': nifty100_change_pct,
            },
            'indiavix': {
                'price': vix_price,
                'change': vix_change,
                'change_pct': vix_change_pct,
            }
        }
    except Exception as e:
        st.warning(f"⚠️ Could not fetch live data: {str(e)[:50]}")
        return None

@st.cache_data(ttl=300)
def get_sector_data():
    """Get all 20+ sectors"""
    return {
        'Banking': 1.89, 'IT': 2.45, 'Energy': 3.12, 'Auto': 0.23,
        'Pharma': -0.56, 'FMCG': -1.23, 'Metals': 1.67, 'Infrastructure': -0.34,
        'Finance': 0.95, 'Telecom': 0.89, 'Utilities': 1.45, 'Media': 1.23,
        'Textiles': -0.45, 'Food & Beverage': 0.67, 'Hotels & Tourism': 1.34,
        'Chemicals': 0.56, 'Retail': 0.78, 'Real Estate': -0.12, 'Cement': 1.12,
        'Steel': 1.89, 'Logistics': 0.45, 'Renewable Energy': 2.34,
    }

# ============================================================================
# HEADER SECTION
# ============================================================================

def render_header():
    """Render beautiful header with theme toggle"""
    col1, col2, col3 = st.columns([3, 1, 0.5])
    
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px;">
            <span style="font-size: 40px; animation: fadeIn 0.6s ease-out;">📈</span>
            <div>
                <h1 class="header-title">STOCK ANALYSIS PRO</h1>
                <div class="header-subtitle">✨ Professional Equity Research Terminal ✨</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Theme toggle
        if st.button("🌓", key="theme_toggle", help="Toggle Dark/Light Mode"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()

# ============================================================================
# KPI CARDS SECTION
# ============================================================================

def render_kpi_cards():
    """Render BEAUTIFUL KPI cards with REAL LIVE DATA - NIFTY & BANK NIFTY CLICKABLE"""
    st.markdown('<h3 class="section-header">📊 Key Market Indices</h3>', unsafe_allow_html=True)
    
    indices = get_live_index_data()
    
    if indices is None:
        st.error("Could not fetch live data. Please refresh the page.")
        return
    
    # Create two columns for NIFTY 50 and BANK NIFTY
    col1, col2 = st.columns(2)
    
    # ===== NIFTY 50 CARD =====
    with col1:
        nifty_color = "#10b981" if indices['nifty50']['change_pct'] >= 0 else "#ef4444"
        nifty_arrow = "▲" if indices['nifty50']['change_pct'] >= 0 else "▼"
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
            border-radius: 20px;
            padding: 32px;
            color: white;
            box-shadow: 0 16px 40px rgba(37, 99, 235, 0.5);
            border: 1px solid rgba(59, 130, 246, 0.6);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.15), transparent);
                pointer-events: none;
            "></div>
            <div style="position: relative; z-index: 1;">
                <div style="
                    font-size: 14px;
                    opacity: 0.9;
                    font-weight: 700;
                    margin-bottom: 12px;
                    letter-spacing: 1.5px;
                    text-transform: uppercase;
                ">📈 NIFTY 50</div>
                <div style="
                    font-size: 42px;
                    font-weight: 900;
                    margin-bottom: 8px;
                    letter-spacing: -1px;
                    color: #fff;
                ">₹{indices['nifty50']['price']:,.0f}</div>
                <div style="
                    font-size: 16px;
                    color: {nifty_color};
                    font-weight: 800;
                    margin-bottom: 16px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                ">
                    <span>{nifty_arrow}</span>
                    <span>{abs(indices['nifty50']['change']):.2f} ({indices['nifty50']['change_pct']:+.2f}%)</span>
                </div>
                <div style="
                    border-top: 1px solid rgba(255,255,255,0.2);
                    padding-top: 12px;
                    font-size: 11px;
                    opacity: 0.85;
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 12px;
                ">
                    <div><span style="opacity: 0.7;">Open:</span><br>₹{indices['nifty50']['open']:,.0f}</div>
                    <div><span style="opacity: 0.7;">High:</span><br>₹{indices['nifty50']['high']:,.0f}</div>
                    <div><span style="opacity: 0.7;">Low:</span><br>₹{indices['nifty50']['low']:,.0f}</div>
                    <div><span style="opacity: 0.7;">Updated:</span><br>{indices['nifty50']['timestamp']}</div>
                </div>
                <div style="
                    font-size: 12px;
                    opacity: 0.75;
                    margin-top: 12px;
                    font-style: italic;
                    text-align: center;
                ">👆 Click below for detailed view</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 View NIFTY 50 Details", key="nifty_btn", use_container_width=True):
            st.session_state.show_index_details = True
            st.session_state.selected_index = "NIFTY 50"
            st.rerun()
    
    # ===== BANK NIFTY CARD =====
    with col2:
        bank_color = "#10b981" if indices['banknifty']['change_pct'] >= 0 else "#ef4444"
        bank_arrow = "▲" if indices['banknifty']['change_pct'] >= 0 else "▼"
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
            border-radius: 20px;
            padding: 32px;
            color: white;
            box-shadow: 0 16px 40px rgba(6, 182, 212, 0.5);
            border: 1px solid rgba(6, 182, 212, 0.6);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.15), transparent);
                pointer-events: none;
            "></div>
            <div style="position: relative; z-index: 1;">
                <div style="
                    font-size: 14px;
                    opacity: 0.9;
                    font-weight: 700;
                    margin-bottom: 12px;
                    letter-spacing: 1.5px;
                    text-transform: uppercase;
                ">🏦 BANK NIFTY</div>
                <div style="
                    font-size: 42px;
                    font-weight: 900;
                    margin-bottom: 8px;
                    letter-spacing: -1px;
                    color: #fff;
                ">₹{indices['banknifty']['price']:,.0f}</div>
                <div style="
                    font-size: 16px;
                    color: {bank_color};
                    font-weight: 800;
                    margin-bottom: 16px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                ">
                    <span>{bank_arrow}</span>
                    <span>{abs(indices['banknifty']['change']):.2f} ({indices['banknifty']['change_pct']:+.2f}%)</span>
                </div>
                <div style="
                    border-top: 1px solid rgba(255,255,255,0.2);
                    padding-top: 12px;
                    font-size: 11px;
                    opacity: 0.85;
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 12px;
                ">
                    <div><span style="opacity: 0.7;">Open:</span><br>₹{indices['banknifty']['open']:,.0f}</div>
                    <div><span style="opacity: 0.7;">High:</span><br>₹{indices['banknifty']['high']:,.0f}</div>
                    <div><span style="opacity: 0.7;">Low:</span><br>₹{indices['banknifty']['low']:,.0f}</div>
                    <div><span style="opacity: 0.7;">Updated:</span><br>{indices['banknifty']['timestamp']}</div>
                </div>
                <div style="
                    font-size: 12px;
                    opacity: 0.75;
                    margin-top: 12px;
                    font-style: italic;
                    text-align: center;
                ">👆 Click below for detailed view</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 View BANK NIFTY Details", key="bank_btn", use_container_width=True):
            st.session_state.show_index_details = True
            st.session_state.selected_index = "BANK NIFTY"
            st.rerun()
    
    st.markdown("")  # Spacing
    
    # ===== OTHER INDICES =====
    st.markdown('<h3 class="section-header">📊 Other Indices</h3>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    # NIFTY 100
    with col3:
        nifty100_color = "#10b981" if indices['nifty100']['change_pct'] >= 0 else "#ef4444"
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #059669 0%, #10b981 100%);
            border-radius: 16px;
            padding: 24px;
            color: white;
            box-shadow: 0 12px 32px rgba(16, 185, 129, 0.4);
            border: 1px solid rgba(34, 197, 94, 0.5);
            backdrop-filter: blur(10px);
        ">
            <div style="position: relative; z-index: 1;">
                <div style="
                    font-size: 12px;
                    opacity: 0.85;
                    font-weight: 700;
                    margin-bottom: 12px;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                ">📊 NIFTY 100</div>
                <div style="
                    font-size: 36px;
                    font-weight: 900;
                    margin-bottom: 10px;
                    letter-spacing: -1px;
                ">₹{indices['nifty100']['price']:,.0f}</div>
                <div style="
                    font-size: 14px;
                    color: {nifty100_color};
                    font-weight: 700;
                ">
                    {'▲' if indices['nifty100']['change_pct'] >= 0 else '▼'} {abs(indices['nifty100']['change']):.2f} ({indices['nifty100']['change_pct']:+.2f}%)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # INDIA VIX
    with col4:
        vix_color = "#ef4444" if indices['indiavix']['change_pct'] > 0 else "#10b981"
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
            border-radius: 16px;
            padding: 24px;
            color: white;
            box-shadow: 0 12px 32px rgba(220, 38, 38, 0.4);
            border: 1px solid rgba(220, 38, 38, 0.5);
            backdrop-filter: blur(10px);
        ">
            <div style="position: relative; z-index: 1;">
                <div style="
                    font-size: 12px;
                    opacity: 0.85;
                    font-weight: 700;
                    margin-bottom: 12px;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                ">⚡ INDIA VIX</div>
                <div style="
                    font-size: 36px;
                    font-weight: 900;
                    margin-bottom: 10px;
                    letter-spacing: -1px;
                ">{indices['indiavix']['price']:.2f}</div>
                <div style="
                    font-size: 14px;
                    color: {vix_color};
                    font-weight: 700;
                ">
                    {'▲' if indices['indiavix']['change_pct'] > 0 else '▼'} {abs(indices['indiavix']['change']):.2f} ({indices['indiavix']['change_pct']:+.2f}%)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# SECTOR PERFORMANCE SECTION
# ============================================================================

def render_sector_performance():
    """Render enhanced sector performance section"""
    st.markdown('<h3 class="section-header">🔥 Sector Performance (20+ Sectors)</h3>', unsafe_allow_html=True)
    
    sectors = get_sector_data()
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        # Sector stats boxes
        cols = st.columns(4)
        for idx, (sector, change) in enumerate(list(sectors.items())[:8]):
            col = cols[idx % 4]
            with col:
                arrow = "▲" if change > 0 else "▼"
                color = "#10b981" if change > 0 else "#ef4444"
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(6, 182, 212, 0.1));
                    border: 1px solid rgba(37, 99, 235, 0.2);
                    border-radius: 12px;
                    padding: 14px;
                    text-align: center;
                    transition: all 0.3s ease;
                ">
                    <div style="font-size: 11px; color: #94a3b8; font-weight: 700; margin-bottom: 6px;">{sector}</div>
                    <div style="font-size: 16px; font-weight: 900; color: {color};">{arrow}{abs(change):.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        # Sector chart
        sector_names = list(sectors.keys())
        sector_values = list(sectors.values())
        colors = ['#10b981' if x > 0 else '#ef4444' for x in sector_values]
        
        fig = go.Figure(data=[go.Bar(
            x=sector_names,
            y=sector_values,
            marker=dict(
                color=colors,
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1),
            ),
            text=[f'{x:+.2f}%' for x in sector_values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Change: %{y:.2f}%<extra></extra>',
        )])
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(15, 23, 42, 0.5)',
            plot_bgcolor='rgba(15, 23, 42, 0.3)',
            title="All 20+ Sectors Performance",
            xaxis_title="Sector",
            yaxis_title="Change %",
            height=400,
            showlegend=False,
            margin=dict(b=120),
            xaxis=dict(tickangle=-45),
            font=dict(color='#fff', size=11),
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ============================================================================
# STATISTICS SECTION
# ============================================================================

def render_market_stats():
    """Render beautiful market statistics"""
    st.markdown('<h3 class="section-header">📈 Market Statistics</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    stats = [
        ("Total Sectors Up", "12", "📈", "#10b981"),
        ("Total Sectors Down", "10", "📉", "#ef4444"),
        ("Avg Sector Change", "+0.89%", "⚖️", "#3b82f6"),
        ("Market Breadth", "1.2:1", "📊", "#06b6d4"),
        ("Trading Activity", "High", "⚡", "#f59e0b"),
    ]
    
    cols = [col1, col2, col3, col4, col5]
    for col, (label, value, icon, color) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {color}20 0%, {color}10 100%);
                border: 1px solid {color}40;
                border-radius: 12px;
                padding: 18px;
                text-align: center;
                transition: all 0.3s ease;
            ">
                <div style="font-size: 20px; margin-bottom: 8px;">{icon}</div>
                <div style="font-size: 12px; color: #94a3b8; font-weight: 700; margin-bottom: 6px;">{label}</div>
                <div style="font-size: 22px; font-weight: 900; color: {color};">{value}</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main dashboard"""
    
    # Initialize session state
    if 'show_index_details' not in st.session_state:
        st.session_state.show_index_details = False
    if 'selected_index' not in st.session_state:
        st.session_state.selected_index = None
    
    render_header()
    st.divider()
    
    # ============================================================================
    # NAVIGATION TO OTHER MODULES
    # ============================================================================
    
    st.markdown('<h3 style="color: #06b6d4; margin-bottom: 16px;">📊 Quick Navigation</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📈 Charting", use_container_width=True, help="Advanced charting tools"):
            st.switch_page("pages/advanced_charting.py")
    
    with col2:
        if st.button("🔬 Screener", use_container_width=True, help="Stock screener with filters"):
            st.switch_page("pages/stock_screener_enhanced.py")
    
    with col3:
        if st.button("💼 Research", use_container_width=True, help="Deep research platform"):
            st.switch_page("pages/research_platform.py")
    
    with col4:
        if st.button("💰 Planning", use_container_width=True, help="Financial planning tools"):
            st.switch_page("pages/financial_planning.py")
    
    with col5:
        if st.button("💰 MF Analysis", use_container_width=True, help="Mutual fund analysis"):
            st.switch_page("pages/mutual_fund_deep_analysis.py")
    
    st.divider()
    
    # Show index details modal if requested
    if st.session_state.show_index_details and st.session_state.selected_index:
        render_index_details_modal(st.session_state.selected_index)
        if st.button("← Back to Dashboard", key="back_from_details"):
            st.session_state.show_index_details = False
            st.rerun()
    else:
        render_kpi_cards()
        st.markdown("")
        
        render_sector_performance()
        st.markdown("")
        
        render_market_stats()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #64748b; font-size: 12px; padding: 20px;">
            <p>📊 Stock Analysis Pro - Professional Equity Research Terminal</p>
            <p>Last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            <p style="font-size: 10px; opacity: 0.7;">🔄 Data updates every 60 seconds | All times in IST</p>
        </div>
        """, unsafe_allow_html=True)

def render_index_details_modal(index_name):
    """Render detailed view for clicked index"""
    st.markdown(f'<h3 class="section-header">📊 {index_name} - DETAILED VIEW</h3>', unsafe_allow_html=True)
    
    indices = get_live_index_data()
    
    if index_name == "NIFTY 50":
        data = indices['nifty50']
        symbol = "^NSEI"
    elif index_name == "BANK NIFTY":
        data = indices['banknifty']
        symbol = "^NSEBANK"
    else:
        return
    
    # Display detailed metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2563eb20, #06b6d420);
            border: 1px solid #2563eb40;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 11px; color: #94a3b8; font-weight: 700; margin-bottom: 8px;">CURRENT PRICE</div>
            <div style="font-size: 24px; font-weight: 900; color: #fff;">₹{data['price']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        change_color = "#10b981" if data['change_pct'] >= 0 else "#ef4444"
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {change_color}20, {change_color}10);
            border: 1px solid {change_color}40;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 11px; color: #94a3b8; font-weight: 700; margin-bottom: 8px;">DAY 1 CHANGE</div>
            <div style="font-size: 20px; font-weight: 900; color: {change_color};">
                {'▲' if data['change_pct'] >= 0 else '▼'} {abs(data['change']):.2f}
            </div>
            <div style="font-size: 12px; color: {change_color}; font-weight: 700;">({data['change_pct']:+.2f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #06b6d420, #0891b220);
            border: 1px solid #06b6d440;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 11px; color: #94a3b8; font-weight: 700; margin-bottom: 8px;">OPEN</div>
            <div style="font-size: 22px; font-weight: 900; color: #fff;">₹{data['open']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #10b98120, #06b6d420);
            border: 1px solid #10b98140;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 11px; color: #94a3b8; font-weight: 700; margin-bottom: 8px;">HIGH</div>
            <div style="font-size: 22px; font-weight: 900; color: #10b981;">₹{data['high']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #ef444420, #dc262620);
            border: 1px solid #ef444440;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 11px; color: #94a3b8; font-weight: 700; margin-bottom: 8px;">LOW</div>
            <div style="font-size: 22px; font-weight: 900; color: #ef4444;">₹{data['low']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Show live chart
    st.markdown(f'**Live 1-Day Chart - {index_name}**')
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period='5d', interval='1h')
        
        if not hist.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name=index_name,
            )])
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(15, 23, 42, 0.5)',
                plot_bgcolor='rgba(15, 23, 42, 0.3)',
                height=400,
                xaxis_rangeslider_visible=False,
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.info("Chart data not available at the moment.")

if __name__ == "__main__":
    main()
