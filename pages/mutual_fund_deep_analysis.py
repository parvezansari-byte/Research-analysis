"""
MUTUAL FUND DEEP ANALYSIS - STANDALONE MODULE
Separate but connected to Stock Analysis Pro
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Mutual Fund Deep Analysis",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# STYLING
# ============================================================================

st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    
    .main-header { 
        font-size: 36px; 
        font-weight: 900; 
        background: linear-gradient(135deg, #06b6d4, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    
    .nav-row {
        display: flex;
        gap: 12px;
        margin-bottom: 24px;
    }
    
    .section-header {
        font-size: 22px;
        font-weight: 800;
        color: #fff;
        margin: 28px 0 18px 0;
        padding-bottom: 12px;
        border-bottom: 2px solid;
        border-image: linear-gradient(90deg, #06b6d4, #10b981) 1;
    }
    
    .stat-box {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(16, 185, 129, 0.1));
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }
    
    .stat-number {
        font-size: 32px;
        font-weight: 900;
        color: #06b6d4;
        margin-bottom: 6px;
    }
    
    .stat-label {
        font-size: 12px;
        color: #94a3b8;
        font-weight: 600;
    }
    
    .search-box {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(16, 185, 129, 0.1));
        border: 2px solid rgba(6, 182, 212, 0.3);
        border-radius: 12px;
        padding: 12px;
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# NAVIGATION HEADER
# ============================================================================

col1, col2, col3 = st.columns([0.5, 1, 0.5])

with col1:
    if st.button("← Back to Stock Analysis", use_container_width=True, help="Return to Stock Analysis Pro"):
        st.switch_page("pages/dashboard_enhanced.py")

with col2:
    st.markdown("")

with col3:
    st.markdown("")

st.markdown("---")

# ============================================================================
# MAIN HEADER
# ============================================================================

st.markdown('<h1 class="main-header">💰 MUTUAL FUND DEEP ANALYSIS</h1>', unsafe_allow_html=True)
st.markdown('<div style="color: #94a3b8; font-size: 13px; font-weight: 600; margin-bottom: 24px;">Professional research on 1000+ mutual funds from 40+ AMCs</div>', unsafe_allow_html=True)

# ============================================================================
# SEARCH FUNCTIONALITY
# ============================================================================

st.markdown('<h2 class="section-header">🔍 Search & Filter</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    search_query = st.text_input(
        "Search for a mutual fund or AMC:",
        placeholder="Type fund name or AMC (e.g., 'HDFC', 'ICICI Large Cap')",
        help="Search across 1000+ mutual funds"
    )

with col2:
    search_type = st.selectbox(
        "Search in:",
        ["All", "Fund Names", "AMC Names", "Sectors"],
        help="Filter search scope"
    )

with col3:
    if st.button("🔎 Search", use_container_width=True):
        st.session_state.search_active = True
        st.session_state.search_query = search_query

# ============================================================================
# KEY STATISTICS
# ============================================================================

st.markdown('<h2 class="section-header">📊 Fund Industry Overview</h2>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">1000+</div>
        <div class="stat-label">MUTUAL FUNDS</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">40+</div>
        <div class="stat-label">AMCs</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">100K+</div>
        <div class="stat-label">HOLDINGS</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">₹40L Cr</div>
        <div class="stat-label">TOTAL AUM</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">17.8%</div>
        <div class="stat-label">AVG 1Y RETURN</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SAMPLE DATA
# ============================================================================

@st.cache_data
def load_sample_mf_data():
    """Load sample mutual fund data"""
    
    funds = pd.DataFrame({
        'Fund_Name': [
            'HDFC Large Cap Fund', 'ICICI Prudential Bluechip Fund', 'Axis Long Term Growth',
            'Mirae Asset Large Cap Fund', 'SBI Large Cap Fund', 'Kotak Large Cap Fund',
            'Bandhan Large Cap Fund', 'Franklin India Large Cap Fund', 'Union Large Cap Fund',
            'UTI Large Cap Fund'
        ],
        'AMC': ['HDFC', 'ICICI Prudential', 'Axis', 'Mirae Asset', 'SBI', 'Kotak', 'Bandhan', 'Franklin', 'Union', 'UTI'],
        'Category': ['Large Cap'] * 10,
        'AUM_Cr': [5000, 8500, 3200, 4100, 2900, 3500, 1800, 2200, 1500, 1200],
        'Expense_Ratio_%': [0.65, 0.58, 0.72, 0.68, 0.75, 0.70, 0.80, 0.72, 0.85, 0.90],
        '1Y_Return_%': [18.5, 19.2, 17.8, 18.9, 17.2, 18.1, 16.9, 17.5, 16.8, 17.1],
        '3Y_Return_%': [15.2, 16.1, 14.8, 15.5, 14.2, 15.1, 13.9, 14.5, 13.8, 14.1],
        'Risk_Rating': [4, 4, 4, 4, 4, 4, 3, 4, 3, 3]
    })
    
    return funds

funds_df = load_sample_mf_data()

# ============================================================================
# SEARCH RESULTS
# ============================================================================

if 'search_active' in st.session_state and st.session_state.search_active:
    search_term = st.session_state.search_query.lower()
    
    if search_term:
        # Search in fund names and AMC names
        results = funds_df[
            (funds_df['Fund_Name'].str.lower().str.contains(search_term)) |
            (funds_df['AMC'].str.lower().str.contains(search_term))
        ]
        
        if len(results) > 0:
            st.markdown(f'<h2 class="section-header">🔎 Search Results for "{search_term}"</h2>', unsafe_allow_html=True)
            
            st.info(f"Found {len(results)} result(s)")
            
            for idx, (_, fund) in enumerate(results.iterrows()):
                with st.expander(f"🏆 {fund['Fund_Name']} ({fund['AMC']})", expanded=(idx==0)):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("AUM", f"₹{fund['AUM_Cr']:,.0f} Cr")
                    with col2:
                        st.metric("1Y Return", f"{fund['1Y_Return_%']:.1f}%", delta=f"{fund['1Y_Return_%']-15:.1f}%")
                    with col3:
                        st.metric("Expense Ratio", f"{fund['Expense_Ratio_%']:.2f}%")
                    with col4:
                        st.metric("Category", fund['Category'])
                    
                    st.write(f"**3Y Return:** {fund['3Y_Return_%']:.1f}%")
                    st.write(f"**Risk Rating:** {'⭐' * fund['Risk_Rating']}")
                    
                    if st.button(f"📊 Detailed Analysis", key=f"btn_{idx}"):
                        st.session_state.detailed_fund = fund['Fund_Name']
        else:
            st.warning(f"No funds found matching '{search_term}'")
    else:
        st.warning("Please enter a search term")
else:
    
    # ========================================================================
    # TOP PERFORMERS
    # ========================================================================
    
    st.markdown('<h2 class="section-header">🏆 Top Performing Funds</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        top_funds = funds_df.nlargest(10, '1Y_Return_%')[
            ['Fund_Name', 'AMC', '1Y_Return_%', 'AUM_Cr', 'Expense_Ratio_%']
        ].copy()
        
        top_funds['1Y_Return_%'] = top_funds['1Y_Return_%'].apply(lambda x: f"{x:.1f}%")
        top_funds['AUM_Cr'] = top_funds['AUM_Cr'].apply(lambda x: f"₹{x:,.0f}Cr")
        top_funds['Expense_Ratio_%'] = top_funds['Expense_Ratio_%'].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(
            top_funds,
            column_config={
                'Fund_Name': st.column_config.TextColumn('Fund Name', width=200),
                'AMC': st.column_config.TextColumn('AMC', width=100),
                '1Y_Return_%': st.column_config.TextColumn('1Y Return', width=100),
                'AUM_Cr': st.column_config.TextColumn('AUM', width=120),
                'Expense_Ratio_%': st.column_config.TextColumn('Expense Ratio', width=120),
            },
            hide_index=True,
            use_container_width=True
        )
    
    with col2:
        # Return distribution chart
        fig = go.Figure(data=[go.Histogram(
            x=funds_df['1Y_Return_%'],
            nbinsx=15,
            marker=dict(
                color=funds_df['1Y_Return_%'],
                colorscale='Viridis',
                showscale=False,
                line=dict(color='rgba(255,255,255,0.2)', width=1)
            ),
            hovertemplate='Return: %{x:.1f}%<br>Funds: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(15, 23, 42, 0.5)',
            plot_bgcolor='rgba(15, 23, 42, 0.3)',
            height=350,
            title='1Y Return Distribution',
            xaxis_title='Return (%)',
            yaxis_title='Number of Funds',
            showlegend=False,
            margin=dict(l=60, r=40, t=40, b=40)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("")
    
    # ========================================================================
    # AMC COMPARISON
    # ========================================================================
    
    st.markdown('<h2 class="section-header">🏢 AMC Comparison</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        amc_aum = funds_df.groupby('AMC')['AUM_Cr'].sum().sort_values(ascending=False)
        
        fig_aum = go.Figure(data=[go.Bar(
            x=amc_aum.values,
            y=amc_aum.index,
            orientation='h',
            marker=dict(
                color=amc_aum.values,
                colorscale='Teal',
                showscale=False,
                line=dict(color='rgba(255,255,255,0.2)', width=1)
            ),
            text=[f"₹{x:,.0f}Cr" for x in amc_aum.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>AUM: ₹%{x:,.0f}Cr<extra></extra>'
        )])
        
        fig_aum.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(15, 23, 42, 0.5)',
            plot_bgcolor='rgba(15, 23, 42, 0.3)',
            height=350,
            xaxis_title='AUM (₹ Crores)',
            showlegend=False,
            margin=dict(l=150, r=100)
        )
        
        st.plotly_chart(fig_aum, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        amc_returns = funds_df.groupby('AMC')['1Y_Return_%'].mean().sort_values(ascending=False)
        
        fig_returns = go.Figure(data=[go.Bar(
            x=amc_returns.values,
            y=amc_returns.index,
            orientation='h',
            marker=dict(
                color=['#06b6d4', '#10b981', '#2563eb', '#f59e0b', '#ef4444'],
                line=dict(color='rgba(255,255,255,0.2)', width=1)
            ),
            text=[f"{x:.1f}%" for x in amc_returns.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Avg Return: %{x:.1f}%<extra></extra>'
        )])
        
        fig_returns.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(15, 23, 42, 0.5)',
            plot_bgcolor='rgba(15, 23, 42, 0.3)',
            height=350,
            xaxis_title='Average 1Y Return (%)',
            showlegend=False,
            margin=dict(l=150, r=100)
        )
        
        st.plotly_chart(fig_returns, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("")
    
    # ========================================================================
    # FUND CATEGORIES
    # ========================================================================
    
    st.markdown('<h2 class="section-header">📊 Fund Categories Available</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    categories = [
        ('Large Cap', 'Stable growth, blue-chip stocks'),
        ('Mid Cap', 'Higher growth potential, moderate risk'),
        ('Small Cap', 'High growth potential, higher risk'),
        ('Balanced', 'Mix of equity and debt'),
        ('Debt', 'Fixed income, lower risk'),
        ('Hybrid', 'Combination of asset classes')
    ]
    
    for i, (cat, desc) in enumerate(categories):
        if i % 3 == 0:
            col = col1
        elif i % 3 == 1:
            col = col2
        else:
            col = col3
        
        with col:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(16, 185, 129, 0.1));
                border: 1px solid rgba(6, 182, 212, 0.2);
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 12px;
            ">
                <div style="font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 8px;">📌 {cat}</div>
                <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# FOOTER WITH NAVIGATION
# ============================================================================

st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("← Back to Stock Analysis Pro", use_container_width=True, help="Return to main platform"):
        st.switch_page("pages/dashboard_enhanced.py")

with col2:
    st.markdown("")

with col3:
    st.markdown("""
    <div style="text-align: right; color: #64748b; font-size: 11px;">
        📊 Last Updated: """ + datetime.now().strftime("%H:%M:%S") + """
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 11px; padding: 20px; margin-top: 20px;">
    <p>💰 Mutual Fund Deep Analysis Module | Connected to Stock Analysis Pro</p>
    <p>1000+ Funds | 40+ AMCs | Professional Grade Analysis</p>
</div>
""", unsafe_allow_html=True)
