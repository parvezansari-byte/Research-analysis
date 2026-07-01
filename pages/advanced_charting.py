"""
ADVANCED CHARTING PAGE
Professional Trading Terminal with Multiple Chart Types
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from api_handler import get_technical_indicators, get_historical_data

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Advanced Charting",
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
        margin: 24px 0 16px 0;
    }
    .control-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .chart-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 16px;
        margin: 16px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CACHING FUNCTIONS (Rate Limiting Protection)
# ============================================================================

@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_chart_data(symbol, timeframe):
    """Get chart data with caching and error handling"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=timeframe)
        
        if data.empty:
            return None
        
        return data
    except Exception as e:
        if "Too Many Requests" in str(e) or "Rate limit" in str(e):
            return None
        return None

@st.cache_data(ttl=600)
def get_stock_info_cached(symbol):
    """Get stock info with caching"""
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info
    except Exception as e:
        return {}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_fibonacci_levels(high, low):
    """Calculate Fibonacci retracement levels"""
    diff = high - low
    level_236 = high - (diff * 0.236)
    level_382 = high - (diff * 0.382)
    level_500 = high - (diff * 0.500)
    level_618 = high - (diff * 0.618)
    level_786 = high - (diff * 0.786)
    
    return {
        '0%': high,
        '23.6%': level_236,
        '38.2%': level_382,
        '50%': level_500,
        '61.8%': level_618,
        '78.6%': level_786,
        '100%': low,
    }

def calculate_support_resistance(data, window=20):
    """Calculate support and resistance levels"""
    high = data['High'].rolling(window=window).max()
    low = data['Low'].rolling(window=window).min()
    
    return high.iloc[-1], low.iloc[-1]

def add_bollinger_bands(fig, data, period=20):
    """Add Bollinger Bands to figure"""
    close = data['Close']
    sma = close.rolling(window=period).mean()
    std = close.rolling(window=period).std()
    
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)
    
    fig.add_trace(go.Scatter(
        x=data.index, y=upper_band,
        fill=None, mode='lines', name='BB Upper',
        line=dict(color='rgba(59, 130, 246, 0.3)', width=1),
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=data.index, y=lower_band,
        fill='tonexty', mode='lines', name='BB Lower',
        line=dict(color='rgba(59, 130, 246, 0.3)', width=1),
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=data.index, y=sma,
        mode='lines', name='SMA 20',
        line=dict(color='rgba(251, 146, 60, 0.7)', width=1, dash='dash'),
        hoverinfo='skip'
    ))

def create_candlestick_chart(data, title="Candlestick Chart"):
    """Create candlestick chart with volume"""
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.2],
        subplot_titles=(title, "Volume")
    )
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='OHLC',
            increasing_line_color='#22c55e',
            decreasing_line_color='#ef4444',
        ),
        row=1, col=1
    )
    
    # Volume
    colors = ['#22c55e' if close >= open_ else '#ef4444' 
              for close, open_ in zip(data['Close'], data['Open'])]
    
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['Volume'],
            name='Volume',
            marker_color=colors,
            showlegend=False,
            hoverinfo='x+y'
        ),
        row=2, col=1
    )
    
    # Add Bollinger Bands
    add_bollinger_bands(fig, data)
    
    # Layout
    fig.update_layout(
        title=title,
        template="plotly_dark",
        paper_bgcolor='rgba(15, 23, 42, 0.5)',
        plot_bgcolor='rgba(15, 23, 42, 0.5)',
        height=700,
        hovermode='x unified',
        xaxis_rangeslider_visible=False,
        font=dict(family="Arial, sans-serif", color="#fff"),
    )
    
    fig.update_yaxes(title_text="Price (₹)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    return fig

def create_rsi_chart(data, period=14):
    """Create RSI chart"""
    
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data.index, y=rsi,
        mode='lines', name='RSI 14',
        line=dict(color='#3b82f6', width=2)
    ))
    
    fig.add_hline(y=70, line_dash="dash", line_color="#ef4444", 
                  annotation_text="Overbought (70)")
    fig.add_hline(y=30, line_dash="dash", line_color="#22c55e", 
                  annotation_text="Oversold (30)")
    
    fig.update_layout(
        title="Relative Strength Index (RSI)",
        template="plotly_dark",
        paper_bgcolor='rgba(15, 23, 42, 0.5)',
        plot_bgcolor='rgba(15, 23, 42, 0.5)',
        height=400,
        hovermode='x',
        yaxis_range=[0, 100]
    )
    
    return fig

def create_macd_chart(data):
    """Create MACD chart"""
    
    close = data['Close']
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()
    histogram = macd - signal
    
    fig = go.Figure()
    
    # Histogram
    colors = ['#22c55e' if h > 0 else '#ef4444' for h in histogram]
    fig.add_trace(go.Bar(
        x=data.index, y=histogram,
        name='Histogram',
        marker_color=colors,
        showlegend=True
    ))
    
    # MACD
    fig.add_trace(go.Scatter(
        x=data.index, y=macd,
        mode='lines', name='MACD',
        line=dict(color='#3b82f6', width=2)
    ))
    
    # Signal
    fig.add_trace(go.Scatter(
        x=data.index, y=signal,
        mode='lines', name='Signal',
        line=dict(color='#f59e0b', width=2)
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="#64748b")
    
    fig.update_layout(
        title="MACD (Moving Average Convergence Divergence)",
        template="plotly_dark",
        paper_bgcolor='rgba(15, 23, 42, 0.5)',
        plot_bgcolor='rgba(15, 23, 42, 0.5)',
        height=400,
        hovermode='x'
    )
    
    return fig

def create_atr_chart(data, period=14):
    """Create ATR (Average True Range) chart"""
    
    high_low = data['High'] - data['Low']
    high_close = abs(data['High'] - data['Close'].shift(1))
    low_close = abs(data['Low'] - data['Close'].shift(1))
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data.index, y=atr,
        mode='lines', name='ATR 14',
        line=dict(color='#10b981', width=2),
        fill='tozeroy'
    ))
    
    fig.update_layout(
        title="Average True Range (ATR)",
        template="plotly_dark",
        paper_bgcolor='rgba(15, 23, 42, 0.5)',
        plot_bgcolor='rgba(15, 23, 42, 0.5)',
        height=400,
        hovermode='x',
        yaxis_title="ATR Value (₹)"
    )
    
    return fig

def create_moving_averages_chart(data):
    """Create moving averages chart"""
    
    sma20 = data['Close'].rolling(window=20).mean()
    sma50 = data['Close'].rolling(window=50).mean()
    sma200 = data['Close'].rolling(window=200).mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data.index, y=data['Close'],
        mode='lines', name='Close Price',
        line=dict(color='#fff', width=1)
    ))
    
    fig.add_trace(go.Scatter(
        x=data.index, y=sma20,
        mode='lines', name='SMA 20',
        line=dict(color='#3b82f6', width=2, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=data.index, y=sma50,
        mode='lines', name='SMA 50',
        line=dict(color='#f59e0b', width=2, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=data.index, y=sma200,
        mode='lines', name='SMA 200',
        line=dict(color='#ef4444', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="Moving Averages (SMA 20, 50, 200)",
        template="plotly_dark",
        paper_bgcolor='rgba(15, 23, 42, 0.5)',
        plot_bgcolor='rgba(15, 23, 42, 0.5)',
        height=400,
        hovermode='x',
        yaxis_title="Price (₹)"
    )
    
    return fig

def create_fibonacci_chart(data):
    """Create Fibonacci retracement chart"""
    
    high = data['High'].max()
    low = data['Low'].min()
    fib_levels = get_fibonacci_levels(high, low)
    
    fig = go.Figure()
    
    # Price line
    fig.add_trace(go.Scatter(
        x=data.index, y=data['Close'],
        mode='lines', name='Close Price',
        line=dict(color='#fff', width=1)
    ))
    
    # Fibonacci levels
    colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#06b6d4', '#ef4444']
    
    for (level_name, level_value), color in zip(fib_levels.items(), colors):
        fig.add_hline(
            y=level_value,
            line_dash="dash",
            line_color=color,
            annotation_text=f"{level_name}: ₹{level_value:.2f}",
            annotation_position="right"
        )
    
    fig.update_layout(
        title="Fibonacci Retracement Levels",
        template="plotly_dark",
        paper_bgcolor='rgba(15, 23, 42, 0.5)',
        plot_bgcolor='rgba(15, 23, 42, 0.5)',
        height=500,
        hovermode='x',
        yaxis_title="Price (₹)"
    )
    
    return fig

# ============================================================================
# MAIN PAGE
# ============================================================================

def main():
    """Main charting page"""
    
    # Header
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
        <span style="font-size: 32px;">📈</span>
        <div>
            <h1 class="header-title">Advanced Charting</h1>
            <div class="header-subtitle">Professional Trading Terminal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    col1, col2, col3 = st.columns([8, 1, 1])
    with col3:
        if st.button("← BACK", use_container_width=True, key="back_btn"):
            st.switch_page("dashboard.py")
    
    st.divider()
    
    # Controls
    st.markdown('<h3 class="section-header">⚙️ Chart Controls</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        symbol = st.text_input("Stock Symbol", "RELIANCE.NS", key="symbol_input")
    
    with col2:
        timeframe = st.selectbox(
            "Timeframe",
            ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
            key="timeframe_select"
        )
    
    with col3:
        chart_type = st.selectbox(
            "Chart Type",
            ["Candlestick", "RSI", "MACD", "ATR", "Moving Averages", "Fibonacci"],
            key="chart_type_select"
        )
    
    with col4:
        show_bb = st.checkbox("Show Bollinger Bands", value=True, key="bb_checkbox")
    
    st.divider()
    
    # Fetch data
    try:
        with st.spinner("Loading chart data..."):
            # Use cached function to avoid rate limiting
            data = get_chart_data(symbol, timeframe)
            
            if data is None:
                st.error("⏳ **API Rate Limited** - The market data API is temporarily limiting requests. Please:")
                st.info("""
                1. **Wait 2-3 minutes** before trying again
                2. **Try a different stock** to test the feature
                3. **Use shorter timeframe** (1mo instead of 5y)
                4. **Check back later** during off-peak hours
                
                This is a normal API limitation from Yahoo Finance (yfinance).
                """)
                return
            
            if data.empty:
                st.error(f"No data found for {symbol}")
                return
            
            # Get stock info (cached)
            info = get_stock_info_cached(symbol)
            current_price = data['Close'].iloc[-1]
            change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
            change_pct = (change / data['Close'].iloc[-2]) * 100
            
            # Display stock info
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Current Price", f"₹{current_price:.2f}", f"{change:+.2f} ({change_pct:+.2f}%)")
            with col2:
                st.metric("52W High", f"₹{info.get('fiftyTwoWeekHigh', 'N/A')}")
            with col3:
                st.metric("52W Low", f"₹{info.get('fiftyTwoWeekLow', 'N/A')}")
            with col4:
                st.metric("Volume", f"{data['Volume'].iloc[-1]:,.0f}")
            
            st.divider()
            
            # Display chart based on selection
            st.markdown(f'<h3 class="section-header">📊 {chart_type} Chart</h3>', unsafe_allow_html=True)
            
            if chart_type == "Candlestick":
                fig = create_candlestick_chart(data, f"{symbol} - {timeframe}")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
            
            elif chart_type == "RSI":
                fig = create_rsi_chart(data)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
            
            elif chart_type == "MACD":
                fig = create_macd_chart(data)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
            
            elif chart_type == "ATR":
                fig = create_atr_chart(data)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
            
            elif chart_type == "Moving Averages":
                fig = create_moving_averages_chart(data)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
            
            elif chart_type == "Fibonacci":
                fig = create_fibonacci_chart(data)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
            
            # Support and Resistance
            st.markdown('<h3 class="section-header">📍 Support & Resistance</h3>', unsafe_allow_html=True)
            
            resistance, support = calculate_support_resistance(data, window=20)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Resistance", f"₹{resistance:.2f}", "High level")
            with col2:
                st.metric("Current", f"₹{current_price:.2f}", "Current price")
            with col3:
                st.metric("Support", f"₹{support:.2f}", "Low level")
            
            # Fibonacci levels
            st.markdown('<h3 class="section-header">🔢 Fibonacci Levels</h3>', unsafe_allow_html=True)
            
            high = data['High'].max()
            low = data['Low'].min()
            fib_levels = get_fibonacci_levels(high, low)
            
            fib_cols = st.columns(len(fib_levels))
            for col, (level_name, level_value) in zip(fib_cols, fib_levels.items()):
                with col:
                    st.metric(level_name, f"₹{level_value:.2f}")
            
            # Technical Indicators Summary
            st.markdown('<h3 class="section-header">🔬 Technical Indicators</h3>', unsafe_allow_html=True)
            
            indicators = get_technical_indicators(symbol)
            
            if indicators:
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("RSI 14", f"{indicators.get('RSI 14', 'N/A'):.0f}" if isinstance(indicators.get('RSI 14'), (int, float)) else "N/A")
                with col2:
                    st.metric("MACD", indicators.get('MACD', 'N/A'))
                with col3:
                    st.metric("SMA 20", f"₹{indicators.get('SMA 20', 'N/A'):.2f}" if isinstance(indicators.get('SMA 20'), (int, float)) else "N/A")
                with col4:
                    st.metric("SMA 50", f"₹{indicators.get('SMA 50', 'N/A'):.2f}" if isinstance(indicators.get('SMA 50'), (int, float)) else "N/A")
                with col5:
                    st.metric("ATR", f"₹{indicators.get('ATR', 'N/A'):.2f}" if isinstance(indicators.get('ATR'), (int, float)) else "N/A")
    
    except Exception as e:
        st.error(f"Error loading chart: {str(e)[:100]}")

if __name__ == "__main__":
    main()
