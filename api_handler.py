"""
API INTEGRATION MODULE
Real Data from yfinance + Finnhub
"""

import yfinance as yf
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
from functools import lru_cache
import time

# ============================================================================
# API CONFIGURATION
# ============================================================================

FINNHUB_API_KEY = "cqkfdqpr01qulvh1dct0cqkfdqpr01qulvh1dct"  # FREE TIER KEY
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

# ============================================================================
# CACHE FOR PERFORMANCE
# ============================================================================

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_stock_price(symbol):
    """Get current stock price from yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        if not data.empty:
            return float(data['Close'].iloc[-1])
        return None
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None

@st.cache_data(ttl=3600)
def get_stock_info(symbol):
    """Get stock info from yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return info
    except Exception as e:
        print(f"Error fetching info for {symbol}: {e}")
        return {}

@st.cache_data(ttl=86400)  # Cache for 24 hours
def get_fundamentals_finnhub(symbol):
    """Get fundamentals from Finnhub"""
    try:
        # Remove .NS suffix for API call
        api_symbol = symbol.replace('.NS', '').replace('.BO', '')
        
        url = f"{FINNHUB_BASE_URL}/financials-reported"
        params = {
            'symbol': api_symbol,
            'token': FINNHUB_API_KEY,
            'freq': 'annual'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                return data['data'][0]
        return None
    except Exception as e:
        print(f"Error fetching fundamentals from Finnhub: {e}")
        return None

@st.cache_data(ttl=3600)
def get_historical_data(symbol, period='1y'):
    """Get historical data from yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        return data
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return None

# ============================================================================
# NIFTY 50 & INDICES DATA
# ============================================================================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_nifty50_data():
    """Get NIFTY 50 real data"""
    try:
        nifty = yf.Ticker('^NSEI')
        data = nifty.history(period='1d')
        
        if not data.empty:
            current = float(data['Close'].iloc[-1])
            prev_close = float(data['Open'].iloc[-1])
            change = current - prev_close
            change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
            high = float(data['High'].iloc[-1])
            low = float(data['Low'].iloc[-1])
            volume = int(data['Volume'].iloc[-1]) if 'Volume' in data.columns else 0
            
            return {
                'price': current,
                'change': change,
                'change_pct': change_pct,
                'high': high,
                'low': low,
                'volume': volume,
                'market_cap': 'N/A'
            }
        return None
    except Exception as e:
        print(f"Error fetching NIFTY 50: {e}")
        return None

@st.cache_data(ttl=300)
def get_banknifty_data():
    """Get BANK NIFTY real data"""
    try:
        banknifty = yf.Ticker('^NSEBANK')
        data = banknifty.history(period='1d')
        
        if not data.empty:
            current = float(data['Close'].iloc[-1])
            prev_close = float(data['Open'].iloc[-1])
            change = current - prev_close
            change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
            high = float(data['High'].iloc[-1])
            low = float(data['Low'].iloc[-1])
            volume = int(data['Volume'].iloc[-1]) if 'Volume' in data.columns else 0
            
            return {
                'price': current,
                'change': change,
                'change_pct': change_pct,
                'high': high,
                'low': low,
                'volume': volume,
                'market_cap': 'N/A'
            }
        return None
    except Exception as e:
        print(f"Error fetching BANK NIFTY: {e}")
        return None

@st.cache_data(ttl=300)
def get_nifty100_data():
    """Get NIFTY 100 real data"""
    try:
        nifty100 = yf.Ticker('^NIFTY100')
        data = nifty100.history(period='1d')
        
        if not data.empty:
            current = float(data['Close'].iloc[-1])
            prev_close = float(data['Open'].iloc[-1])
            change = current - prev_close
            change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
            
            return {
                'price': current,
                'change': change,
                'change_pct': change_pct,
            }
        return None
    except Exception as e:
        print(f"Error fetching NIFTY 100: {e}")
        return None

@st.cache_data(ttl=300)
def get_indiavix_data():
    """Get INDIA VIX real data"""
    try:
        vix = yf.Ticker('^INDIAVIX')
        data = vix.history(period='1d')
        
        if not data.empty:
            current = float(data['Close'].iloc[-1])
            prev_close = float(data['Open'].iloc[-1])
            change = current - prev_close
            change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
            
            return {
                'price': current,
                'change': change,
                'change_pct': change_pct,
            }
        return None
    except Exception as e:
        print(f"Error fetching INDIA VIX: {e}")
        return None

# ============================================================================
# COMPANY FUNDAMENTALS
# ============================================================================

@st.cache_data(ttl=86400)
def get_company_fundamentals(symbol):
    """Get company fundamentals from yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        fundamentals = {
            'PE Ratio': info.get('trailingPE', 'N/A'),
            'PB Ratio': info.get('priceToBook', 'N/A'),
            'ROE': info.get('returnOnEquity', 'N/A'),
            'ROA': info.get('returnOnAssets', 'N/A'),
            'Dividend Yield': info.get('dividendYield', 'N/A'),
            'Debt/Equity': info.get('debtToEquity', 'N/A'),
            'Current Ratio': info.get('currentRatio', 'N/A'),
            'Profit Margin': info.get('profitMargins', 'N/A'),
            'EPS Growth': info.get('earningsGrowth', 'N/A'),
            'Revenue Growth': info.get('revenueGrowth', 'N/A'),
        }
        
        return fundamentals
    except Exception as e:
        print(f"Error fetching fundamentals: {e}")
        return {}

@st.cache_data(ttl=3600)
def get_technical_indicators(symbol):
    """Calculate technical indicators from yfinance data"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1y')
        
        if len(data) < 200:
            return None
        
        # Calculate indicators
        close = data['Close']
        
        # RSI 14
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Moving averages
        sma20 = close.rolling(window=20).mean()
        sma50 = close.rolling(window=50).mean()
        sma200 = close.rolling(window=200).mean()
        
        # Bollinger Bands
        bb_middle = sma20.iloc[-1]
        bb_std = close.rolling(window=20).std()
        bb_upper = bb_middle + (bb_std.iloc[-1] * 2)
        bb_lower = bb_middle - (bb_std.iloc[-1] * 2)
        
        # Current price
        current_price = close.iloc[-1]
        
        # MACD (simplified)
        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()
        macd = ema12 - ema26
        macd_signal = macd.ewm(span=9).mean()
        macd_trend = 'Bullish' if macd.iloc[-1] > macd_signal.iloc[-1] else 'Bearish'
        
        return {
            'Current Price': current_price,
            'RSI 14': rsi.iloc[-1],
            'MACD': macd_trend,
            'SMA 20': sma20.iloc[-1],
            'SMA 50': sma50.iloc[-1],
            'SMA 200': sma200.iloc[-1],
            'Bollinger Upper': bb_upper,
            'Bollinger Middle': bb_middle,
            'Bollinger Lower': bb_lower,
            'ATR': data['High'].rolling(14).max().iloc[-1] - data['Low'].rolling(14).min().iloc[-1],
        }
    except Exception as e:
        print(f"Error calculating technicals: {e}")
        return None

# ============================================================================
# TOP GAINERS & LOSERS
# ============================================================================

@st.cache_data(ttl=300)
def get_top_gainers_losers():
    """Get top gainers and losers"""
    try:
        # Popular NSE stocks
        nse_stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
                      'WIPRO.NS', 'AXISBANK.NS', 'MARUTI.NS', 'LT.NS', 'BAJAJFINSV.NS']
        
        gainers = []
        losers = []
        
        for stock in nse_stocks:
            try:
                ticker = yf.Ticker(stock)
                data = ticker.history(period='1d')
                
                if not data.empty:
                    current = float(data['Close'].iloc[-1])
                    prev_close = float(data['Open'].iloc[-1])
                    change_pct = ((current - prev_close) / prev_close * 100) if prev_close != 0 else 0
                    
                    stock_name = stock.replace('.NS', '')
                    
                    if change_pct > 0:
                        gainers.append({'Stock': stock_name, 'Price': current, 'Change %': change_pct})
                    else:
                        losers.append({'Stock': stock_name, 'Price': current, 'Change %': change_pct})
            except:
                pass
        
        gainers.sort(key=lambda x: x['Change %'], reverse=True)
        losers.sort(key=lambda x: x['Change %'])
        
        return pd.DataFrame(gainers[:5]), pd.DataFrame(losers[:5])
    except Exception as e:
        print(f"Error fetching gainers/losers: {e}")
        return pd.DataFrame(), pd.DataFrame()

# ============================================================================
# SENTIMENT DATA
# ============================================================================

@st.cache_data(ttl=3600)
def get_analyst_ratings(symbol):
    """Get analyst ratings from Finnhub"""
    try:
        api_symbol = symbol.replace('.NS', '').replace('.BO', '')
        
        url = f"{FINNHUB_BASE_URL}/stock/recommendation"
        params = {
            'symbol': api_symbol,
            'token': FINNHUB_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                latest = data[0]
                return {
                    'Buy': latest.get('buy', 0),
                    'Hold': latest.get('hold', 0),
                    'Sell': latest.get('sell', 0),
                }
        return {'Buy': 0, 'Hold': 0, 'Sell': 0}
    except Exception as e:
        print(f"Error fetching analyst ratings: {e}")
        return {'Buy': 0, 'Hold': 0, 'Sell': 0}

@st.cache_data(ttl=3600)
def get_company_news(symbol, limit=5):
    """Get company news from Finnhub"""
    try:
        api_symbol = symbol.replace('.NS', '').replace('.BO', '')
        
        url = f"{FINNHUB_BASE_URL}/company-news"
        params = {
            'symbol': api_symbol,
            'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'to': datetime.now().strftime('%Y-%m-%d'),
            'token': FINNHUB_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            news_items = []
            for item in data[:limit]:
                news_items.append({
                    'headline': item.get('headline', 'N/A'),
                    'summary': item.get('summary', 'N/A'),
                    'source': item.get('source', 'N/A'),
                    'url': item.get('url', '#')
                })
            return news_items
        return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

# ============================================================================
# COMPARE STOCKS
# ============================================================================

@st.cache_data(ttl=3600)
def compare_stocks(symbols):
    """Compare multiple stocks"""
    try:
        comparison_data = []
        
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            data = ticker.history(period='1d')
            
            if not data.empty:
                current = float(data['Close'].iloc[-1])
                prev_close = float(data['Open'].iloc[-1])
                change_pct = ((current - prev_close) / prev_close * 100) if prev_close != 0 else 0
                
                comparison_data.append({
                    'Symbol': symbol.replace('.NS', ''),
                    'Price': current,
                    'Change %': change_pct,
                    'PE Ratio': info.get('trailingPE', 'N/A'),
                    'Market Cap': info.get('marketCap', 'N/A'),
                    'ROE': info.get('returnOnEquity', 'N/A'),
                })
        
        return pd.DataFrame(comparison_data)
    except Exception as e:
        print(f"Error comparing stocks: {e}")
        return pd.DataFrame()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def format_large_number(num):
    """Format large numbers"""
    if num is None:
        return 'N/A'
    if isinstance(num, str):
        return num
    
    if num >= 1e12:
        return f'₹{num/1e12:.1f}T'
    elif num >= 1e9:
        return f'₹{num/1e9:.1f}B'
    elif num >= 1e6:
        return f'₹{num/1e6:.1f}M'
    else:
        return f'₹{num:.0f}'

def format_percentage(num):
    """Format percentage"""
    if num is None:
        return 'N/A'
    return f'{num:.2f}%'

def get_stock_color(change):
    """Get color based on change"""
    if change > 0:
        return '#22c55e'  # Green
    elif change < 0:
        return '#ef4444'  # Red
    else:
        return '#64748b'  # Gray
