"""
ENHANCED STOCK SCREENER
100+ NSE Stocks with Advanced Filters and Detailed Analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
from stocks_indicators_db import (
    NSE_STOCKS, get_all_stocks, get_stocks_by_sector, 
    get_sector_performance, INDICATOR_DESCRIPTIONS
)
import yfinance as yf

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Enhanced Stock Screener",
    page_icon="📊",
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
        margin: 24px 0 16px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data(ttl=600)
def get_stock_screener_data(stocks):
    """Get data for multiple stocks"""
    results = []
    
    for stock in stocks:
        try:
            ticker = yf.Ticker(stock)
            data = ticker.history(period='1mo')
            info = ticker.info
            
            if len(data) > 0:
                current_price = data['Close'].iloc[-1]
                prev_close = data['Open'].iloc[0] if len(data) > 0 else current_price
                change = current_price - prev_close
                change_pct = (change / prev_close * 100) if prev_close != 0 else 0
                
                # Calculate RSI
                delta = data['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                
                results.append({
                    'Stock': stock.replace('.NS', ''),
                    'Price': current_price,
                    'Change %': change_pct,
                    'Volume': data['Volume'].iloc[-1],
                    'RSI': rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50,
                    '52W High': info.get('fiftyTwoWeekHigh', 'N/A'),
                    '52W Low': info.get('fiftyTwoWeekLow', 'N/A'),
                    'PE Ratio': info.get('trailingPE', 'N/A'),
                    'Market Cap': info.get('marketCap', 'N/A'),
                })
        except:
            pass
    
    return pd.DataFrame(results)

# ============================================================================
# MAIN PAGE
# ============================================================================

def main():
    """Main screener page"""
    
    # Header
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
        <span style="font-size: 32px;">📊</span>
        <div>
            <h1 class="header-title">Enhanced Stock Screener</h1>
            <div class="header-subtitle">100+ NSE Stocks with Advanced Filters</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    col1, col2, col3 = st.columns([8, 1, 1])
    with col3:
        if st.button("← BACK", use_container_width=True, key="back_btn"):
            st.switch_page("dashboard.py")
    
    st.divider()
    
    # Filters
    st.markdown('<h3 class="section-header">⚙️ Advanced Filters</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sector = st.selectbox(
            "Sector",
            ["All Sectors"] + list(NSE_STOCKS.keys()),
            key="sector_select"
        )
    
    with col2:
        rsi_filter = st.slider("RSI Range", 0, 100, (30, 70), key="rsi_slider")
    
    with col3:
        change_filter = st.slider("Change % Range", -20.0, 20.0, (-10.0, 10.0), key="change_slider")
    
    with col4:
        show_signals = st.checkbox("Show Buy/Sell Signals", value=True, key="signals_checkbox")
    
    st.divider()
    
    # Get stocks to screen
    if sector == "All Sectors":
        stocks_to_screen = get_all_stocks()
    else:
        stocks_to_screen = get_stocks_by_sector(sector)
    
    st.markdown(f'<h3 class="section-header">📊 Screening {len(stocks_to_screen)} Stocks...</h3>', unsafe_allow_html=True)
    
    # Fetch data
    with st.spinner(f"Analyzing {len(stocks_to_screen)} stocks..."):
        df = get_stock_screener_data(stocks_to_screen)
    
    if not df.empty:
        # Apply filters
        df_filtered = df[
            (df['RSI'] >= rsi_filter[0]) & (df['RSI'] <= rsi_filter[1]) &
            (df['Change %'] >= change_filter[0]) & (df['Change %'] <= change_filter[1])
        ]
        
        st.success(f"✅ Found {len(df_filtered)} stocks matching criteria (Total: {len(df)} screened)")
        
        # Add signals if requested
        if show_signals:
            st.markdown('<h3 class="section-header">🎯 Buy/Sell Signals</h3>', unsafe_allow_html=True)
            
            # Generate signals
            def get_signal(row):
                signals = []
                
                # RSI signals
                if row['RSI'] < 30:
                    signals.append("🟢 RSI Oversold")
                elif row['RSI'] > 70:
                    signals.append("🔴 RSI Overbought")
                
                # Price signals
                if row['Change %'] < -5:
                    signals.append("🟢 Down 5%+")
                elif row['Change %'] > 5:
                    signals.append("🔴 Up 5%+")
                
                return " | ".join(signals) if signals else "➡️ Neutral"
            
            df_filtered['Signals'] = df_filtered.apply(get_signal, axis=1)
        
        # Display results
        st.markdown('<h3 class="section-header">📈 Results</h3>', unsafe_allow_html=True)
        
        # Sort by various options
        col1, col2, col3 = st.columns(3)
        with col1:
            sort_by = st.selectbox(
                "Sort By",
                ["RSI", "Change %", "Price", "Volume"],
                key="sort_select"
            )
        
        # Sort dataframe
        if sort_by == "RSI":
            df_filtered = df_filtered.sort_values('RSI')
        elif sort_by == "Change %":
            df_filtered = df_filtered.sort_values('Change %', ascending=False)
        elif sort_by == "Price":
            df_filtered = df_filtered.sort_values('Price', ascending=False)
        else:
            df_filtered = df_filtered.sort_values('Volume', ascending=False)
        
        # Display table with formatting
        display_cols = ['Stock', 'Price', 'Change %', 'RSI', 'Volume', 'PE Ratio']
        if show_signals:
            display_cols.append('Signals')
        
        # Format dataframe for display
        df_display = df_filtered[display_cols].copy()
        df_display['Price'] = df_display['Price'].apply(lambda x: f"₹{x:.2f}")
        df_display['Change %'] = df_display['Change %'].apply(lambda x: f"{x:+.2f}%")
        df_display['RSI'] = df_display['RSI'].apply(lambda x: f"{x:.0f}")
        df_display['Volume'] = df_display['Volume'].apply(lambda x: f"{x/1e5:.1f}L" if x > 0 else "N/A")
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Statistics
        st.markdown('<h3 class="section-header">📊 Statistics</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            oversold = len(df_filtered[df_filtered['RSI'] < 30])
            st.metric("🟢 Oversold (RSI<30)", oversold)
        
        with col2:
            overbought = len(df_filtered[df_filtered['RSI'] > 70])
            st.metric("🔴 Overbought (RSI>70)", overbought)
        
        with col3:
            gainers = len(df_filtered[df_filtered['Change %'] > 0])
            st.metric("📈 Gainers", gainers)
        
        with col4:
            losers = len(df_filtered[df_filtered['Change %'] < 0])
            st.metric("📉 Losers", losers)
        
        with col5:
            avg_rsi = df_filtered['RSI'].mean()
            st.metric("Average RSI", f"{avg_rsi:.0f}")
        
        # Technical Indicators Info
        st.markdown('<h3 class="section-header">🔬 Technical Indicators Guide</h3>', unsafe_allow_html=True)
        
        with st.expander("📖 Learn About Indicators"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### RSI (Relative Strength Index)")
                st.info(INDICATOR_DESCRIPTIONS.get('RSI', ''))
                
                st.markdown("#### Volume")
                st.info("Higher volume = Stronger signal. Compare with 20-day average.")
            
            with col2:
                st.markdown("#### Price Change %")
                st.info("Percentage change from previous close. Identifies momentum.")
                
                st.markdown("#### PE Ratio")
                st.info("Price-to-Earnings ratio. Lower = Cheaper, Higher = Expensive")
    
    else:
        st.warning("No stocks found. Try adjusting your filters.")

if __name__ == "__main__":
    main()
