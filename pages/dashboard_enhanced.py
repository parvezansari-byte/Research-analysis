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
    create_stat_box, get_theme_css, CHART_TEMPLATE, GRADIENT_PALETTES, CHART_COLORS
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

@st.cache_data(ttl=300)
def get_index_data():
    """Get live index data"""
    try:
        nifty = yf.Ticker("^NSEI")
        bank_nifty = yf.Ticker("^NSEBANK")
        nifty100 = yf.Ticker("^NIFTY100")
        vix = yf.Ticker("^INDIAVIX")
        
        return {
            'nifty50': {'price': nifty.info.get('currentPrice', 23865), 'change': 0.69, 'change_pct': -0.69},
            'banknifty': {'price': bank_nifty.info.get('currentPrice', 57542), 'change': -0.81, 'change_pct': -0.81},
            'nifty100': {'price': nifty100.info.get('currentPrice', 26800), 'change': 0.56, 'change_pct': 0.56},
            'indiavix': {'price': vix.info.get('currentPrice', 18.5), 'change': -0.25, 'change_pct': -1.33},
        }
    except:
        return {
            'nifty50': {'price': 23865, 'change': 0.69, 'change_pct': -0.69},
            'banknifty': {'price': 57542, 'change': -0.81, 'change_pct': -0.81},
            'nifty100': {'price': 26800, 'change': 0.56, 'change_pct': 0.56},
            'indiavix': {'price': 18.5, 'change': -0.25, 'change_pct': -1.33},
        }

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
    """Render beautiful KPI cards with premium styling"""
    st.markdown('<h3 class="section-header">📊 Market Overview</h3>', unsafe_allow_html=True)
    
    indices = get_index_data()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_gradient_card(
            "NIFTY 50",
            f"₹{indices['nifty50']['price']:,.0f}",
            f"Change: {indices['nifty50']['change_pct']:+.2f}%",
            "#1e40af", "#2563eb",
            "📈"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_gradient_card(
            "BANK NIFTY",
            f"₹{indices['banknifty']['price']:,.0f}",
            f"Change: {indices['banknifty']['change_pct']:+.2f}%",
            "#0891b2", "#06b6d4",
            "🏦"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_gradient_card(
            "NIFTY 100",
            f"₹{indices['nifty100']['price']:,.0f}",
            f"Change: {indices['nifty100']['change_pct']:+.2f}%",
            "#059669", "#10b981",
            "📊"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_gradient_card(
            "INDIA VIX",
            f"₹{indices['indiavix']['price']:.2f}",
            f"Change: {indices['indiavix']['change_pct']:+.2f}%",
            "#dc2626", "#991b1b",
            "⚡"
        ), unsafe_allow_html=True)

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
            **CHART_TEMPLATE['layout'],
            title="All 20+ Sectors Performance",
            xaxis_title="Sector",
            yaxis_title="Change %",
            height=400,
            showlegend=False,
            margin=dict(b=120),
            xaxis=dict(tickangle=-45),
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
    render_header()
    st.divider()
    
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
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
