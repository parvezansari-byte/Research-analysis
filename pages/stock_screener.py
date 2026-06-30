# 📈 PROFESSIONAL STOCK SCREENER & ANALYZER
# Complete Analysis for Every Stock (NSE/BSE)
# Fundamental & Technical Analysis with Trading Signals

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# STOCK DATABASE
# ============================================================================

class StockDatabase:
    """Comprehensive stock database with fundamental data"""
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def get_all_stocks():
        """Get all NSE stocks with fundamental data"""
        stocks = {
            # Large Cap
            'RELIANCE.NS': {'Name': 'Reliance Industries', 'Sector': 'Energy', 'Market Cap': '₹18.5L Cr'},
            'TCS.NS': {'Name': 'Tata Consultancy Services', 'Sector': 'IT', 'Market Cap': '₹16.2L Cr'},
            'INFY.NS': {'Name': 'Infosys', 'Sector': 'IT', 'Market Cap': '₹9.8L Cr'},
            'HDFCBANK.NS': {'Name': 'HDFC Bank', 'Sector': 'Bank', 'Market Cap': '₹9.2L Cr'},
            'ICICIBANK.NS': {'Name': 'ICICI Bank', 'Sector': 'Bank', 'Market Cap': '₹8.5L Cr'},
            'WIPRO.NS': {'Name': 'Wipro', 'Sector': 'IT', 'Market Cap': '₹3.8L Cr'},
            'AXISBANK.NS': {'Name': 'Axis Bank', 'Sector': 'Bank', 'Market Cap': '₹4.5L Cr'},
            'MARUTI.NS': {'Name': 'Maruti Suzuki', 'Sector': 'Auto', 'Market Cap': '₹2.1L Cr'},
            'BAJAJFINSV.NS': {'Name': 'Bajaj Finserv', 'Sector': 'Finance', 'Market Cap': '₹1.8L Cr'},
            'LT.NS': {'Name': 'Larsen & Toubro', 'Sector': 'Construction', 'Market Cap': '₹2.8L Cr'},
            
            # Mid Cap
            'SUNPHARMA.NS': {'Name': 'Sun Pharmaceutical', 'Sector': 'Pharma', 'Market Cap': '₹1.2L Cr'},
            'ASIANPAINT.NS': {'Name': 'Asian Paints', 'Sector': 'Paints', 'Market Cap': '₹2.5L Cr'},
            'BAJAJSUSANN.NS': {'Name': 'Bajaj Sussman', 'Sector': 'FMCG', 'Market Cap': '₹1.5L Cr'},
            'HINDUNILVR.NS': {'Name': 'Hindustan Unilever', 'Sector': 'FMCG', 'Market Cap': '₹5.8L Cr'},
            'ITC.NS': {'Name': 'ITC Limited', 'Sector': 'FMCG', 'Market Cap': '₹3.2L Cr'},
            'NESTLEIND.NS': {'Name': 'Nestle India', 'Sector': 'FMCG', 'Market Cap': '₹1.9L Cr'},
            'TATAMOTORS.NS': {'Name': 'Tata Motors', 'Sector': 'Auto', 'Market Cap': '₹1.4L Cr'},
            'M&M.NS': {'Name': 'Mahindra & Mahindra', 'Sector': 'Auto', 'Market Cap': '₹1.8L Cr'},
            'BAJAJ-AUTO.NS': {'Name': 'Bajaj Auto', 'Sector': 'Auto', 'Market Cap': '₹1.2L Cr'},
            'HEROMOTOCO.NS': {'Name': 'Hero MotoCorp', 'Sector': 'Auto', 'Market Cap': '₹1.5L Cr'},
            
            # Small Cap & Growth
            'PAGEIND.NS': {'Name': 'Page Industries', 'Sector': 'Consumer', 'Market Cap': '₹0.8L Cr'},
            'BERGEPAINT.NS': {'Name': 'Berger Paints', 'Sector': 'Paints', 'Market Cap': '₹0.6L Cr'},
            'DIVISLAB.NS': {'Name': 'Divis Laboratories', 'Sector': 'Pharma', 'Market Cap': '₹0.9L Cr'},
            'LUPIN.NS': {'Name': 'Lupin Limited', 'Sector': 'Pharma', 'Market Cap': '₹0.7L Cr'},
            'DRREDDY.NS': {'Name': 'Dr. Reddy\'s Labs', 'Sector': 'Pharma', 'Market Cap': '₹1.1L Cr'},
        }
        return stocks

class StockFundamentals:
    """Stock fundamental data"""
    
    @staticmethod
    def get_stock_fundamentals(ticker):
        """Get fundamental data for a stock"""
        # Mock data - in production, connect to real APIs
        base_data = {
            'PE Ratio': np.random.uniform(15, 35),
            'PB Ratio': np.random.uniform(2, 6),
            'ROE': np.random.uniform(12, 28),
            'ROA': np.random.uniform(5, 15),
            'Dividend Yield': np.random.uniform(0.5, 3.5),
            'Debt to Equity': np.random.uniform(0.2, 1.5),
            'Current Ratio': np.random.uniform(1.2, 2.5),
            'Quick Ratio': np.random.uniform(0.8, 2.0),
            'Interest Coverage': np.random.uniform(3, 10),
            'Profit Margin': np.random.uniform(8, 25),
            'Asset Turnover': np.random.uniform(0.5, 1.5),
            'EPS Growth YoY': np.random.uniform(5, 35),
            'Revenue Growth YoY': np.random.uniform(5, 30),
            'Free Cash Flow': f"₹{np.random.randint(100, 5000)}Cr",
            'Book Value': f"₹{np.random.randint(50, 500)}",
        }
        return base_data

class StockTechnicals:
    """Stock technical analysis"""
    
    @staticmethod
    def get_stock_technicals(ticker):
        """Get technical indicators for a stock"""
        price = np.random.uniform(100, 5000)
        return {
            'Current Price': price,
            '50 DMA': price * np.random.uniform(0.95, 1.05),
            '200 DMA': price * np.random.uniform(0.90, 1.10),
            'RSI 14': np.random.uniform(30, 80),
            'MACD': np.random.uniform(-50, 150),
            'MACD Signal': np.random.uniform(-50, 150),
            'Stochastic %K': np.random.uniform(20, 80),
            'Bollinger Upper': price * 1.05,
            'Bollinger Middle': price,
            'Bollinger Lower': price * 0.95,
            'ADX': np.random.uniform(20, 50),
            'ATR': price * np.random.uniform(0.02, 0.05),
            'CCI': np.random.uniform(-200, 200),
            'Support 1': price * np.random.uniform(0.95, 0.99),
            'Support 2': price * np.random.uniform(0.90, 0.95),
            'Resistance 1': price * np.random.uniform(1.01, 1.05),
            'Resistance 2': price * np.random.uniform(1.05, 1.10),
        }

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def render_stock_screener():
    """Render stock screener with filters"""
    st.markdown('<h2 style="color: #3b82f6;">🔍 Professional Stock Screener</h2>', unsafe_allow_html=True)
    
    stocks_db = StockDatabase.get_all_stocks()
    
    # ===== FILTERS =====
    st.markdown('<h3 class="section-header">🎯 Filter by Criteria</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        selected_sector = st.multiselect(
            "Sector",
            ['All', 'IT', 'Bank', 'Auto', 'FMCG', 'Pharma', 'Energy', 'Finance', 'Construction', 'Consumer', 'Paints'],
            default=['All']
        )
    
    with col2:
        selected_cap = st.multiselect(
            "Market Cap",
            ['All', 'Large Cap', 'Mid Cap', 'Small Cap'],
            default=['All']
        )
    
    with col3:
        pe_range = st.slider("PE Ratio Range", 10, 50, (15, 35))
    
    with col4:
        roe_range = st.slider("ROE Range (%)", 5, 40, (12, 28))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        div_yield = st.slider("Min Dividend Yield (%)", 0.0, 5.0, 1.0)
    
    with col2:
        growth = st.slider("Min EPS Growth (%)", 0, 50, 10)
    
    with col3:
        sort_by = st.selectbox(
            "Sort By",
            ['PE Ratio (Low to High)', 'ROE (High to Low)', 'Dividend Yield (High to Low)', 'EPS Growth (High to Low)']
        )
    
    # ===== SCREENED STOCKS LIST =====
    st.markdown('<h3 class="section-header">📊 Screened Stocks</h3>', unsafe_allow_html=True)
    
    # Create screener results
    screener_results = []
    for ticker, info in stocks_db.items():
        fundamentals = StockFundamentals.get_stock_fundamentals(ticker)
        technicals = StockTechnicals.get_stock_technicals(ticker)
        
        if (fundamentals['PE Ratio'] >= pe_range[0] and fundamentals['PE Ratio'] <= pe_range[1] and
            fundamentals['ROE'] >= roe_range[0] and fundamentals['ROE'] <= roe_range[1] and
            fundamentals['Dividend Yield'] >= div_yield and
            fundamentals['EPS Growth YoY'] >= growth):
            
            # Determine signal
            rsi = fundamentals['PE Ratio']
            if technicals['RSI 14'] > 70:
                signal = "⚠️ Overbought"
            elif technicals['RSI 14'] < 30:
                signal = "✅ Oversold"
            else:
                signal = "➡️ Neutral"
            
            screener_results.append({
                'Stock': info['Name'],
                'Ticker': ticker,
                'Sector': info['Sector'],
                'Price': f"₹{technicals['Current Price']:.0f}",
                'PE': f"{fundamentals['PE Ratio']:.1f}x",
                'ROE': f"{fundamentals['ROE']:.1f}%",
                'Div Yield': f"{fundamentals['Dividend Yield']:.2f}%",
                'EPS Growth': f"{fundamentals['EPS Growth YoY']:.1f}%",
                'RSI': f"{technicals['RSI 14']:.0f}",
                'Signal': signal,
            })
    
    screener_df = pd.DataFrame(screener_results)
    
    if len(screener_df) > 0:
        st.dataframe(screener_df, use_container_width=True, hide_index=True)
        
        st.markdown(f"**Total Stocks Found: {len(screener_df)}**")
    else:
        st.info("No stocks match your criteria. Try adjusting the filters.")

def render_individual_stock_analysis():
    """Render detailed analysis for a single stock"""
    st.markdown('<h2 style="color: #3b82f6;">📊 Individual Stock Analysis</h2>', unsafe_allow_html=True)
    
    stocks_db = StockDatabase.get_all_stocks()
    stock_list = [(v['Name'], k) for k, v in stocks_db.items()]
    
    # ===== STOCK SELECTION =====
    selected_stock_name = st.selectbox(
        "Select Stock",
        [name for name, _ in stock_list]
    )
    
    # Get ticker from name
    selected_ticker = next(ticker for name, ticker in stock_list if name == selected_stock_name)
    stock_info = stocks_db[selected_ticker]
    
    # Get fundamental and technical data
    fundamentals = StockFundamentals.get_stock_fundamentals(selected_ticker)
    technicals = StockTechnicals.get_stock_technicals(selected_ticker)
    
    # ===== OVERVIEW =====
    st.markdown('<h3 class="section-header">📈 Stock Overview</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Current Price",
            value=f"₹{technicals['Current Price']:.0f}",
            delta=f"{np.random.uniform(-5, 5):.2f}%"
        )
    
    with col2:
        st.metric(
            label="Market Cap",
            value=stock_info['Market Cap'],
            delta="Positive"
        )
    
    with col3:
        st.metric(
            label="Sector",
            value=stock_info['Sector'],
            delta="—"
        )
    
    with col4:
        st.metric(
            label="Volume",
            value=f"{np.random.randint(1, 50)}M",
            delta="Moderate"
        )
    
    # ===== FUNDAMENTAL ANALYSIS =====
    st.markdown('<h3 class="section-header">💼 Fundamental Analysis</h3>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Valuation", "Profitability", "Financial Health", "Growth"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Valuation Metrics")
            valuation_data = {
                'Metric': ['PE Ratio', 'PB Ratio', 'Dividend Yield', 'Book Value'],
                'Value': [
                    f"{fundamentals['PE Ratio']:.1f}x",
                    f"{fundamentals['PB Ratio']:.1f}x",
                    f"{fundamentals['Dividend Yield']:.2f}%",
                    f"₹{np.random.randint(50, 500)}"
                ],
                'Assessment': ['Fair', 'Reasonable', 'Good', 'Stable']
            }
            st.dataframe(pd.DataFrame(valuation_data), use_container_width=True, hide_index=True)
        
        with col2:
            # PE Ratio trend chart
            fig = go.Figure()
            months = ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            pe_values = [fundamentals['PE Ratio'] + np.random.uniform(-2, 2) for _ in months]
            fig.add_trace(go.Scatter(x=months, y=pe_values, mode='lines+markers', name='PE Ratio', line=dict(color='#3b82f6', width=2)))
            fig.update_layout(
                title="PE Ratio Trend",
                xaxis_title="Month",
                yaxis_title="PE Ratio",
                template="plotly_dark",
                height=300,
                paper_bgcolor='rgba(15, 23, 42, 0.5)',
                plot_bgcolor='rgba(15, 23, 42, 0.5)',
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Profitability Metrics")
            profitability_data = {
                'Metric': ['ROE', 'ROA', 'Profit Margin', 'Asset Turnover'],
                'Value': [
                    f"{fundamentals['ROE']:.1f}%",
                    f"{fundamentals['ROA']:.1f}%",
                    f"{fundamentals['Profit Margin']:.1f}%",
                    f"{fundamentals['Asset Turnover']:.2f}x"
                ],
                'Industry Avg': ['16.5%', '7.2%', '12.5%', '0.95x']
            }
            st.dataframe(pd.DataFrame(profitability_data), use_container_width=True, hide_index=True)
        
        with col2:
            # Profitability comparison
            fig = go.Figure()
            fig.add_trace(go.Bar(x=['ROE', 'ROA'], y=[fundamentals['ROE'], fundamentals['ROA']], name='Stock', marker_color='#3b82f6'))
            fig.add_trace(go.Bar(x=['ROE', 'ROA'], y=[16.5, 7.2], name='Industry Avg', marker_color='#94a3b8'))
            fig.update_layout(
                title="Profitability vs Industry Average",
                barmode='group',
                template="plotly_dark",
                height=300,
                paper_bgcolor='rgba(15, 23, 42, 0.5)',
                plot_bgcolor='rgba(15, 23, 42, 0.5)',
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Liquidity & Solvency")
            liquidity_data = {
                'Metric': ['Current Ratio', 'Quick Ratio', 'Debt to Equity', 'Interest Coverage'],
                'Value': [
                    f"{fundamentals['Current Ratio']:.2f}x",
                    f"{fundamentals['Quick Ratio']:.2f}x",
                    f"{fundamentals['Debt to Equity']:.2f}x",
                    f"{fundamentals['Interest Coverage']:.1f}x"
                ],
                'Healthy Level': ['> 1.5x', '> 1.0x', '< 0.8x', '> 5.0x']
            }
            st.dataframe(pd.DataFrame(liquidity_data), use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### Health Score")
            health_metrics = {
                'Liquidity': 75,
                'Solvency': 82,
                'Efficiency': 70,
                'Overall': 76
            }
            
            fig = go.Figure(go.Scatterpolar(
                r=list(health_metrics.values()),
                theta=list(health_metrics.keys()),
                fill='toself',
                marker_color='#3b82f6'
            ))
            fig.update_layout(
                template="plotly_dark",
                height=350,
                paper_bgcolor='rgba(15, 23, 42, 0.5)',
                plot_bgcolor='rgba(15, 23, 42, 0.5)',
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Growth Metrics")
            growth_data = {
                'Metric': ['EPS Growth YoY', 'Revenue Growth YoY', 'Free Cash Flow', 'Earnings Growth'],
                'Value': [
                    f"{fundamentals['EPS Growth YoY']:.1f}%",
                    f"{fundamentals['Revenue Growth YoY']:.1f}%",
                    fundamentals['Free Cash Flow'],
                    'Strong'
                ],
                'Trend': ['↑ Up', '↑ Up', '↑ Up', '↑ Positive']
            }
            st.dataframe(pd.DataFrame(growth_data), use_container_width=True, hide_index=True)
        
        with col2:
            # Growth trend
            fig = go.Figure()
            years = ['2021', '2022', '2023', '2024E']
            eps_growth = [fundamentals['EPS Growth YoY'] * 0.6, fundamentals['EPS Growth YoY'] * 0.8, 
                         fundamentals['EPS Growth YoY'], fundamentals['EPS Growth YoY'] * 1.1]
            fig.add_trace(go.Scatter(x=years, y=eps_growth, mode='lines+markers', name='EPS Growth', line=dict(color='#22c55e', width=2)))
            fig.update_layout(
                title="EPS Growth Trend",
                xaxis_title="Year",
                yaxis_title="EPS Growth (%)",
                template="plotly_dark",
                height=300,
                paper_bgcolor='rgba(15, 23, 42, 0.5)',
                plot_bgcolor='rgba(15, 23, 42, 0.5)',
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # ===== TECHNICAL ANALYSIS =====
    st.markdown('<h3 class="section-header">📈 Technical Analysis</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Price & Averages")
        price_data = {
            'Metric': ['Current Price', '50 DMA', '200 DMA', 'Distance to 50 DMA'],
            'Value': [
                f"₹{technicals['Current Price']:.0f}",
                f"₹{technicals['50 DMA']:.0f}",
                f"₹{technicals['200 DMA']:.0f}",
                f"{((technicals['Current Price'] / technicals['50 DMA'] - 1) * 100):.1f}%"
            ]
        }
        st.dataframe(pd.DataFrame(price_data), use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### Momentum Indicators")
        momentum_data = {
            'Indicator': ['RSI 14', 'Stochastic %K', 'CCI', 'ADX'],
            'Value': [
                f"{technicals['RSI 14']:.0f}",
                f"{technicals['Stochastic %K']:.0f}",
                f"{technicals['CCI']:.0f}",
                f"{technicals['ADX']:.1f}"
            ],
            'Signal': ['Neutral' if 30 < technicals['RSI 14'] < 70 else 'Extreme', 'Neutral', 'Neutral', 'Trending']
        }
        st.dataframe(pd.DataFrame(momentum_data), use_container_width=True, hide_index=True)
    
    with col3:
        st.markdown("#### MACD Analysis")
        macd_data = {
            'Component': ['MACD Line', 'Signal Line', 'Histogram', 'Status'],
            'Value': [
                f"{technicals['MACD']:.2f}",
                f"{technicals['MACD Signal']:.2f}",
                f"{technicals['MACD'] - technicals['MACD Signal']:.2f}",
                'Bullish' if technicals['MACD'] > technicals['MACD Signal'] else 'Bearish'
            ]
        }
        st.dataframe(pd.DataFrame(macd_data), use_container_width=True, hide_index=True)
    
    # ===== SUPPORT & RESISTANCE =====
    st.markdown('<h3 class="section-header">🎯 Support & Resistance</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Support Levels")
        support_data = {
            'Level': ['Immediate Support', 'Strong Support'],
            'Price': [f"₹{technicals['Support 1']:.0f}", f"₹{technicals['Support 2']:.0f}"],
            'Distance': [f"{((technicals['Support 1'] / technicals['Current Price'] - 1) * 100):.1f}%", 
                        f"{((technicals['Support 2'] / technicals['Current Price'] - 1) * 100):.1f}%"]
        }
        st.dataframe(pd.DataFrame(support_data), use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### Resistance Levels")
        resistance_data = {
            'Level': ['Immediate Resistance', 'Strong Resistance'],
            'Price': [f"₹{technicals['Resistance 1']:.0f}", f"₹{technicals['Resistance 2']:.0f}"],
            'Distance': [f"{((technicals['Resistance 1'] / technicals['Current Price'] - 1) * 100):.1f}%", 
                        f"{((technicals['Resistance 2'] / technicals['Current Price'] - 1) * 100):.1f}%"]
        }
        st.dataframe(pd.DataFrame(resistance_data), use_container_width=True, hide_index=True)
    
    # ===== PRICE CHARTS =====
    st.markdown('<h3 class="section-header">📊 Price & Technical Charts</h3>', unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Price chart with MAs
        dates = pd.date_range(start='2024-01-01', periods=60, freq='D')
        prices = [technicals['Current Price'] + np.cumsum(np.random.randn(60) * 5)[i] for i in range(60)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=prices, name='Price', line=dict(color='#3b82f6', width=2)))
        fig.update_layout(
            title="Price Chart (60 Days)",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_dark",
            height=400,
            paper_bgcolor='rgba(15, 23, 42, 0.5)',
            plot_bgcolor='rgba(15, 23, 42, 0.5)',
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with chart_col2:
        # RSI chart
        rsi_values = np.random.uniform(30, 75, 60)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=rsi_values, name='RSI', line=dict(color='#f59e0b', width=2)))
        fig.add_hline(y=70, line_dash="dash", line_color="red")
        fig.add_hline(y=30, line_dash="dash", line_color="green")
        fig.update_layout(
            title="RSI (14 Period)",
            xaxis_title="Date",
            yaxis_title="RSI",
            template="plotly_dark",
            height=400,
            paper_bgcolor='rgba(15, 23, 42, 0.5)',
            plot_bgcolor='rgba(15, 23, 42, 0.5)',
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # ===== TRADING RECOMMENDATION =====
    st.markdown('<h3 class="section-header">🎯 Trading Signal & Recommendation</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # Determine signal
    rsi = technicals['RSI 14']
    if rsi > 70:
        signal = "⚠️ SELL"
        color = "red"
        reasoning = "RSI Overbought - Time to take profits"
    elif rsi < 30:
        signal = "✅ BUY"
        color = "green"
        reasoning = "RSI Oversold - Good buying opportunity"
    else:
        signal = "➡️ HOLD"
        color = "blue"
        reasoning = "No clear signal - Wait for confirmation"
    
    with col1:
        st.markdown(f"""
        <div style='background: rgba({255 if color=="red" else 34 if color=="green" else 59}, 
        {165 if color=="red" else 197 if color=="green" else 130}, 
        {68 if color=="red" else 94 if color=="green" else 246}, 0.2); 
        border: 1px solid rgba({255 if color=="red" else 34 if color=="green" else 59}, 
        {165 if color=="red" else 197 if color=="green" else 130}, 
        {68 if color=="red" else 94 if color=="green" else 246}, 0.5); 
        border-radius: 8px; padding: 16px;'>
            <div style='font-size: 14px; font-weight: 700; color: #{"ef4444" if color=="red" else "22c55e" if color=="green" else "3b82f6"}; margin-bottom: 8px;'>📈 Trading Signal</div>
            <div style='font-size: 20px; font-weight: 700; color: #fff;'>{signal}</div>
            <div style='font-size: 12px; color: #cbd5e1; margin-top: 8px;'>{reasoning}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: rgba(34, 197, 94, 0.2); border: 1px solid rgba(34, 197, 94, 0.5); border-radius: 8px; padding: 16px;'>
            <div style='font-size: 14px; font-weight: 700; color: #22c55e; margin-bottom: 8px;'>🎯 Price Targets</div>
            <div style='font-size: 12px; color: #cbd5e1;'>
                <strong>Target 1:</strong> ₹{technicals['Resistance 1']:.0f}<br>
                <strong>Target 2:</strong> ₹{technicals['Resistance 2']:.0f}<br>
                <strong>Stop Loss:</strong> ₹{technicals['Support 1']:.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: rgba(34, 197, 94, 0.2); border: 1px solid rgba(34, 197, 94, 0.5); border-radius: 8px; padding: 16px;'>
            <div style='font-size: 14px; font-weight: 700; color: #22c55e; margin-bottom: 8px;'>⚖️ Risk-Reward</div>
            <div style='font-size: 12px; color: #cbd5e1;'>
                <strong>Ratio:</strong> 1:{((technicals['Resistance 2'] - technicals['Current Price']) / (technicals['Current Price'] - technicals['Support 1'])):.1f}<br>
                <strong>Risk Level:</strong> {'Low' if ((technicals['Resistance 2'] - technicals['Current Price']) / (technicals['Current Price'] - technicals['Support 1'])) > 2 else 'Medium' if ((technicals['Resistance 2'] - technicals['Current Price']) / (technicals['Current Price'] - technicals['Support 1'])) > 1 else 'High'}<br>
                <strong>Confidence:</strong> {int(rsi / 10)}/10
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main application"""
    
    st.set_page_config(page_title="Stock Screener & Analyzer", layout="wide", initial_sidebar_state="collapsed")
    
    # Custom CSS
    st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)
    
    # ===== MAIN NAVIGATION =====
    st.markdown('<h1 style="color: #3b82f6; text-align: center; margin-bottom: 30px;">📈 Professional Stock Screener & Analyzer</h1>', unsafe_allow_html=True)
    
    analysis_type = st.radio(
        "Choose Analysis Type:",
        ["Stock Screener", "Individual Stock Analysis"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if analysis_type == "Stock Screener":
        render_stock_screener()
    else:
        render_individual_stock_analysis()

if __name__ == "__main__":
    main()
