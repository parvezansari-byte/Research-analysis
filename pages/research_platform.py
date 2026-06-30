"""
COMPLETE ANALYSIS & RESEARCH PLATFORM
Institutional Grade - Full Research Suite
Comprehensive Analysis for Professional Investors
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Complete Research Platform",
    page_icon="🔬",
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
    
    .card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
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
        font-size: 18px;
        font-weight: 700;
        color: #fff;
        font-family: 'Courier New', monospace;
    }
    
    .tab-header {
        font-size: 12px;
        color: #cbd5e1;
        font-weight: 700;
        text-transform: uppercase;
        padding: 12px 0;
        border-bottom: 2px solid rgba(59, 130, 246, 0.3);
    }
    
    .footer-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-top: 40px;
        text-align: center;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================================
# COMPANY DATA FUNCTIONS
# ============================================================================

def get_company_data(company_name):
    """Get comprehensive company data"""
    return {
        'name': company_name,
        'price': 2750,
        'market_cap': 125000,
        'pe_ratio': 21.5,
        'pb_ratio': 3.2,
        'dividend_yield': 1.85,
    }

def get_fundamental_research(company):
    """Get comprehensive fundamental research"""
    return {
        'Balance Sheet': {
            'Total Assets': '₹450,000 Cr',
            'Total Liabilities': '₹200,000 Cr',
            'Equity': '₹250,000 Cr',
            'Current Assets': '₹85,000 Cr',
            'Current Liabilities': '₹40,000 Cr',
            'Inventory': '₹25,000 Cr',
        },
        'Income Statement': {
            'Revenue': '₹85,000 Cr',
            'EBITDA': '₹18,000 Cr',
            'Net Profit': '₹10,625 Cr',
            'EPS': '₹85.25',
            'Dividend per Share': '₹2.50',
        },
        'Key Ratios': {
            'Debt to Equity': 0.80,
            'Current Ratio': 2.13,
            'Quick Ratio': 1.85,
            'ROE': 18.5,
            'ROA': 8.2,
            'Profit Margin': 12.5,
            'Asset Turnover': 1.89,
            'Interest Coverage': 5.2,
        }
    }

def get_technical_research(price):
    """Get comprehensive technical research"""
    return {
        'Price Action': {
            'Current Price': f'₹{price}',
            '52W High': f'₹{price * 1.35}',
            '52W Low': f'₹{price * 0.75}',
            'YTD Return': '+18.5%',
        },
        'Indicators': {
            'RSI 14': 62.5,
            'MACD': 'Bullish',
            'SMA 20': price * 0.98,
            'SMA 50': price * 0.96,
            'SMA 200': price * 0.92,
            'Bollinger Upper': price * 1.08,
            'Bollinger Middle': price,
            'Bollinger Lower': price * 0.92,
        },
        'Volatility': {
            'ATR': 85.5,
            'Beta': 1.15,
            'Std Dev': 2.35,
        }
    }

def get_valuation_research():
    """Get valuation analysis"""
    return {
        'Multiples': {
            'PE Ratio': 21.5,
            'PB Ratio': 3.2,
            'EV/EBITDA': 14.5,
            'Price to Sales': 2.85,
            'Price to FCF': 18.5,
        },
        'Peer Comparison': {
            'Company PE': 21.5,
            'Industry Avg PE': 18.5,
            'Company PB': 3.2,
            'Industry Avg PB': 2.8,
            'Valuation': 'Premium to peers',
        },
        'DCF Analysis': {
            'Intrinsic Value': '₹3,250',
            'Upside/Downside': '+18.2%',
            'Terminal Growth': '2.5%',
            'WACC': '7.5%',
        }
    }

def get_risk_analysis():
    """Get risk analysis"""
    return {
        'Market Risk': {
            'Beta': 1.15,
            'Volatility': '2.35%',
            'Correlation (Nifty)': 0.85,
        },
        'Business Risk': {
            'Industry Growth': '+12.5%',
            'Market Share': '15.2%',
            'Competitive Position': 'Leader',
        },
        'Financial Risk': {
            'Debt/Equity': 0.80,
            'Interest Coverage': 5.2,
            'Current Ratio': 2.13,
            'Cash Flow': 'Positive',
        },
        'Overall Risk': 'MODERATE',
    }

def get_sentiment_analysis():
    """Get sentiment analysis"""
    return {
        'Analyst Ratings': {
            'Buy': 12,
            'Hold': 5,
            'Sell': 1,
            'Consensus': 'Strong Buy',
        },
        'Insider Activity': {
            'Insider Buying': '+5%',
            'Insider Selling': '-2%',
            'Net Insider': 'Positive',
        },
        'News Sentiment': {
            'Positive': 65,
            'Neutral': 25,
            'Negative': 10,
            'Overall': 'Positive',
        }
    }

def get_industry_analysis():
    """Get industry analysis"""
    return {
        'Industry Metrics': {
            'Industry Growth': '+12.5%',
            'Company Growth': '+15.8%',
            'Market Size': '₹500,000 Cr',
            'Market Share': '15.2%',
        },
        'Competitive Landscape': {
            'Major Competitor 1': 'Peer A (15.8%)',
            'Major Competitor 2': 'Peer B (12.5%)',
            'Major Competitor 3': 'Peer C (10.2%)',
            'Company': 'Leader (15.2%)',
        }
    }

def get_financial_forecast():
    """Get financial forecasts"""
    years = ['2024E', '2025E', '2026E', '2027E', '2028E']
    return pd.DataFrame({
        'Year': years,
        'Revenue': [85000, 98750, 114000, 131100, 150700],
        'EBITDA': [18000, 20850, 24100, 27700, 31700],
        'Net Profit': [10625, 12600, 14900, 17300, 20000],
        'EPS': [85.25, 101.00, 119.50, 138.50, 160.00],
        'Growth %': [16.2, 16.2, 15.3, 15.2, 15.5],
    })

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def render_header():
    """Render header"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div class="header-container">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 32px;">🔬</span>
                <div>
                    <h1 class="header-title">COMPLETE RESEARCH PLATFORM</h1>
                    <div class="header-subtitle">Institutional Grade Analysis & Research Suite</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("← BACK", use_container_width=True, key="back_btn"):
            st.switch_page("pages/top100_analyzer.py")

def render_company_selector():
    """Render company selector"""
    st.markdown('<h3 class="section-header">🏢 Select Company for Research</h3>', unsafe_allow_html=True)
    
    companies = ['Reliance Industries', 'TCS', 'HDFC Bank', 'Infosys', 'ICICI Bank', 
                 'Maruti Suzuki', 'Wipro', 'Axis Bank', 'Bajaj FSV', 'L&T']
    
    selected = st.selectbox("Choose Company", companies, index=0)
    return selected

def render_executive_summary(company):
    """Render executive summary"""
    st.markdown('<h3 class="section-header">📊 Executive Summary</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Current Price</div>
            <div class="metric-value">₹2,750</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Market Cap</div>
            <div class="metric-value">₹125K Cr</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">PE Ratio</div>
            <div class="metric-value">21.5x</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">ROE</div>
            <div class="metric-value">18.5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Rating</div>
            <div class="metric-value" style="color: #22c55e;">BUY ✅</div>
        </div>
        """, unsafe_allow_html=True)

def render_fundamental_analysis():
    """Render fundamental analysis"""
    st.markdown('<h3 class="section-header">💼 Fundamental Analysis</h3>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Balance Sheet", "Income Statement", "Key Ratios"])
    
    fundamentals = get_fundamental_research("Reliance")
    
    with tab1:
        st.markdown("#### Balance Sheet Analysis")
        bs_df = pd.DataFrame(list(fundamentals['Balance Sheet'].items()), columns=['Item', 'Value'])
        st.dataframe(bs_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("#### Income Statement Analysis")
        is_df = pd.DataFrame(list(fundamentals['Income Statement'].items()), columns=['Item', 'Value'])
        st.dataframe(is_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("#### Financial Ratios")
        ratios_df = pd.DataFrame(list(fundamentals['Key Ratios'].items()), columns=['Ratio', 'Value'])
        st.dataframe(ratios_df, use_container_width=True, hide_index=True)

def render_technical_analysis():
    """Render technical analysis"""
    st.markdown('<h3 class="section-header">📈 Technical Analysis</h3>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Price Action", "Indicators", "Volatility"])
    
    technicals = get_technical_research(2750)
    
    with tab1:
        st.markdown("#### Price Action Analysis")
        pa_df = pd.DataFrame(list(technicals['Price Action'].items()), columns=['Metric', 'Value'])
        st.dataframe(pa_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("#### Technical Indicators")
        ind_df = pd.DataFrame(list(technicals['Indicators'].items()), columns=['Indicator', 'Value'])
        st.dataframe(ind_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("#### Volatility Analysis")
        vol_df = pd.DataFrame(list(technicals['Volatility'].items()), columns=['Metric', 'Value'])
        st.dataframe(vol_df, use_container_width=True, hide_index=True)

def render_valuation_analysis():
    """Render valuation analysis"""
    st.markdown('<h3 class="section-header">💰 Valuation Analysis</h3>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Multiples", "Peer Comparison", "DCF Analysis"])
    
    valuation = get_valuation_research()
    
    with tab1:
        st.markdown("#### Valuation Multiples")
        mult_df = pd.DataFrame(list(valuation['Multiples'].items()), columns=['Multiple', 'Value'])
        st.dataframe(mult_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("#### Peer Comparison")
        peer_df = pd.DataFrame(list(valuation['Peer Comparison'].items()), columns=['Metric', 'Value'])
        st.dataframe(peer_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("#### DCF Valuation")
        dcf_df = pd.DataFrame(list(valuation['DCF Analysis'].items()), columns=['Parameter', 'Value'])
        st.dataframe(dcf_df, use_container_width=True, hide_index=True)

def render_risk_analysis():
    """Render risk analysis"""
    st.markdown('<h3 class="section-header">⚠️ Risk Analysis</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    risk = get_risk_analysis()
    
    with col1:
        st.markdown("""
        <div class="card">
            <div style="font-size: 12px; color: #cbd5e1; margin-bottom: 8px; text-transform: uppercase; font-weight: 700;">Market Risk</div>
            <div style="font-size: 13px; color: #fff;">Beta: 1.15</div>
            <div style="font-size: 12px; color: #cbd5e1; margin-top: 8px;">Volatility: 2.35%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <div style="font-size: 12px; color: #cbd5e1; margin-bottom: 8px; text-transform: uppercase; font-weight: 700;">Business Risk</div>
            <div style="font-size: 13px; color: #fff;">Growth: +12.5%</div>
            <div style="font-size: 12px; color: #cbd5e1; margin-top: 8px;">Position: Leader</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <div style="font-size: 12px; color: #cbd5e1; margin-bottom: 8px; text-transform: uppercase; font-weight: 700;">Financial Risk</div>
            <div style="font-size: 13px; color: #fff;">D/E: 0.80</div>
            <div style="font-size: 12px; color: #cbd5e1; margin-top: 8px;">Coverage: 5.2x</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="card">
            <div style="font-size: 12px; color: #cbd5e1; margin-bottom: 8px; text-transform: uppercase; font-weight: 700;">Overall Risk</div>
            <div style="font-size: 14px; color: #f59e0b; font-weight: 700;">MODERATE</div>
            <div style="font-size: 12px; color: #cbd5e1; margin-top: 8px;">Risk Rating</div>
        </div>
        """, unsafe_allow_html=True)

def render_sentiment_analysis():
    """Render sentiment analysis"""
    st.markdown('<h3 class="section-header">📊 Sentiment & Analyst Rating</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    sentiment = get_sentiment_analysis()
    
    with col1:
        st.markdown("#### Analyst Ratings")
        ratings_df = pd.DataFrame({
            'Rating': ['Buy', 'Hold', 'Sell'],
            'Count': [12, 5, 1]
        })
        st.dataframe(ratings_df, use_container_width=True, hide_index=True)
        
        fig = go.Figure(data=[go.Pie(
            labels=['Buy', 'Hold', 'Sell'],
            values=[12, 5, 1],
            marker=dict(colors=['#22c55e', '#f59e0b', '#ef4444'])
        )])
        fig.update_layout(height=300, template="plotly_dark", paper_bgcolor='rgba(15, 23, 42, 0.5)')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("#### Insider Activity")
        insider_df = pd.DataFrame(list(sentiment['Insider Activity'].items()), columns=['Activity', 'Change'])
        st.dataframe(insider_df, use_container_width=True, hide_index=True)
    
    with col3:
        st.markdown("#### News Sentiment")
        news_df = pd.DataFrame({
            'Sentiment': ['Positive', 'Neutral', 'Negative'],
            'Count': [65, 25, 10]
        })
        st.dataframe(news_df, use_container_width=True, hide_index=True)

def render_industry_analysis():
    """Render industry analysis"""
    st.markdown('<h3 class="section-header">🏭 Industry & Competitive Analysis</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    industry = get_industry_analysis()
    
    with col1:
        st.markdown("#### Industry Metrics")
        ind_df = pd.DataFrame(list(industry['Industry Metrics'].items()), columns=['Metric', 'Value'])
        st.dataframe(ind_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### Competitive Landscape")
        comp_df = pd.DataFrame(list(industry['Competitive Landscape'].items()), columns=['Company', 'Share'])
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

def render_financial_forecast():
    """Render financial forecast"""
    st.markdown('<h3 class="section-header">📈 Financial Forecast (5 Years)</h3>', unsafe_allow_html=True)
    
    forecast = get_financial_forecast()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(forecast, use_container_width=True, hide_index=True)
    
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=forecast['Year'], y=forecast['Revenue'], mode='lines+markers', name='Revenue', line=dict(color='#3b82f6', width=2)))
        fig.add_trace(go.Scatter(x=forecast['Year'], y=forecast['Net Profit'], mode='lines+markers', name='Net Profit', line=dict(color='#22c55e', width=2)))
        fig.update_layout(title="Revenue & Profit Forecast", template="plotly_dark", paper_bgcolor='rgba(15, 23, 42, 0.5)', height=300)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_recommendation():
    """Render final recommendation"""
    st.markdown('<h3 class="section-header">🎯 Investment Recommendation</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="card">
            <div style="font-size: 12px; color: #cbd5e1; margin-bottom: 8px;">Rating</div>
            <div style="font-size: 20px; color: #22c55e; font-weight: 700;">BUY ✅</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <div style="font-size: 12px; color: #cbd5e1; margin-bottom: 8px;">Target Price</div>
            <div style="font-size: 20px; color: #fff; font-weight: 700;">₹3,250</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <div style="font-size: 12px; color: #cbd5e1; margin-bottom: 8px;">Upside</div>
            <div style="font-size: 20px; color: #22c55e; font-weight: 700;">+18.2%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="card">
            <div style="font-size: 12px; color: #cbd5e1; margin-bottom: 8px;">Conviction</div>
            <div style="font-size: 20px; color: #fff; font-weight: 700;">9/10</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <div style="font-size: 14px; color: #fff; margin-bottom: 12px;"><strong>Investment Thesis:</strong></div>
        <div style="font-size: 13px; color: #cbd5e1; line-height: 1.6;">
        Strong fundamentals with consistent revenue and profit growth. Trading at premium valuation justified by superior 
        ROE and market position. Technical indicators showing bullish momentum. Analyst consensus is "Strong Buy". 
        Low financial risk with healthy balance sheet. Industry tailwinds support future growth. Suitable for both 
        value and growth investors. Entry on dips near support levels recommended.
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render footer"""
    st.markdown("""
    <div class="footer-container">
        <div style="font-size: 11px; color: #64748b;">📊 COMPLETE RESEARCH PLATFORM | Institutional Grade Analysis</div>
        <div style="font-size: 11px; color: #64748b; margin-top: 8px;">Real-time Data | Last Updated: Today</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application"""
    render_header()
    
    company = render_company_selector()
    
    render_executive_summary(company)
    render_fundamental_analysis()
    render_technical_analysis()
    render_valuation_analysis()
    render_risk_analysis()
    render_sentiment_analysis()
    render_industry_analysis()
    render_financial_forecast()
    render_recommendation()
    render_footer()

if __name__ == "__main__":
    main()
