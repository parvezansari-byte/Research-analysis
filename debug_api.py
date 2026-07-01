"""
API DEBUG SCRIPT
Verify yfinance and Finnhub are working correctly
"""

import yfinance as yf
import requests
import pandas as pd
from datetime import datetime

print("="*80)
print("🔬 API VERIFICATION SCRIPT")
print("="*80)

# ============================================================================
# TEST 1: NIFTY 50 DATA
# ============================================================================

print("\n✅ TEST 1: NIFTY 50 DATA")
print("-" * 80)

try:
    nifty = yf.Ticker('^NSEI')
    data = nifty.history(period='1d')
    
    if not data.empty:
        print(f"Status: ✅ WORKING")
        print(f"Current Price: ₹{data['Close'].iloc[-1]:.2f}")
        print(f"Open: ₹{data['Open'].iloc[-1]:.2f}")
        print(f"High: ₹{data['High'].iloc[-1]:.2f}")
        print(f"Low: ₹{data['Low'].iloc[-1]:.2f}")
        print(f"Volume: {data['Volume'].iloc[-1]:,.0f}")
        
        change = data['Close'].iloc[-1] - data['Open'].iloc[-1]
        change_pct = (change / data['Open'].iloc[-1]) * 100
        print(f"Change: ₹{change:.2f} ({change_pct:+.2f}%)")
    else:
        print("Status: ❌ NO DATA RETURNED")
except Exception as e:
    print(f"Status: ❌ ERROR - {e}")

# ============================================================================
# TEST 2: BANK NIFTY DATA
# ============================================================================

print("\n✅ TEST 2: BANK NIFTY DATA")
print("-" * 80)

try:
    banknifty = yf.Ticker('^NSEBANK')
    data = banknifty.history(period='1d')
    
    if not data.empty:
        print(f"Status: ✅ WORKING")
        print(f"Current Price: ₹{data['Close'].iloc[-1]:.2f}")
        print(f"Open: ₹{data['Open'].iloc[-1]:.2f}")
        print(f"High: ₹{data['High'].iloc[-1]:.2f}")
        print(f"Low: ₹{data['Low'].iloc[-1]:.2f}")
        print(f"Volume: {data['Volume'].iloc[-1]:,.0f}")
        
        change = data['Close'].iloc[-1] - data['Open'].iloc[-1]
        change_pct = (change / data['Open'].iloc[-1]) * 100
        print(f"Change: ₹{change:.2f} ({change_pct:+.2f}%)")
    else:
        print("Status: ❌ NO DATA RETURNED")
except Exception as e:
    print(f"Status: ❌ ERROR - {e}")

# ============================================================================
# TEST 3: INDIVIDUAL STOCK
# ============================================================================

print("\n✅ TEST 3: RELIANCE STOCK")
print("-" * 80)

try:
    reliance = yf.Ticker('RELIANCE.NS')
    data = reliance.history(period='1d')
    info = reliance.info
    
    if not data.empty:
        print(f"Status: ✅ WORKING")
        print(f"Current Price: ₹{data['Close'].iloc[-1]:.2f}")
        print(f"PE Ratio: {info.get('trailingPE', 'N/A')}")
        print(f"ROE: {info.get('returnOnEquity', 'N/A')}")
        print(f"Dividend Yield: {info.get('dividendYield', 'N/A')}")
        print(f"Market Cap: {info.get('marketCap', 'N/A')}")
    else:
        print("Status: ❌ NO DATA RETURNED")
except Exception as e:
    print(f"Status: ❌ ERROR - {e}")

# ============================================================================
# TEST 4: FINNHUB API
# ============================================================================

print("\n✅ TEST 4: FINNHUB API (Analyst Ratings)")
print("-" * 80)

FINNHUB_API_KEY = "cqkfdqpr01qulvh1dct0cqkfdqpr01qulvh1dct"
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

try:
    url = f"{FINNHUB_BASE_URL}/stock/recommendation"
    params = {
        'symbol': 'RELIANCE',
        'token': FINNHUB_API_KEY
    }
    
    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            print(f"Status: ✅ WORKING")
            print(f"Latest Ratings: {data[0]}")
            print(f"Buy: {data[0].get('buy', 0)}")
            print(f"Hold: {data[0].get('hold', 0)}")
            print(f"Sell: {data[0].get('sell', 0)}")
        else:
            print("Status: ⚠️ NO DATA FOR THIS STOCK")
    else:
        print(f"Status: ❌ API Error - Status {response.status_code}")
except Exception as e:
    print(f"Status: ❌ ERROR - {e}")

# ============================================================================
# TEST 5: TOP GAINERS
# ============================================================================

print("\n✅ TEST 5: TOP GAINERS & LOSERS")
print("-" * 80)

try:
    nse_stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS']
    
    print("Fetching data for 5 stocks...")
    results = []
    
    for stock in nse_stocks:
        try:
            ticker = yf.Ticker(stock)
            data = ticker.history(period='1d')
            
            if not data.empty:
                current = float(data['Close'].iloc[-1])
                prev_close = float(data['Open'].iloc[-1])
                change_pct = ((current - prev_close) / prev_close * 100) if prev_close != 0 else 0
                
                results.append({
                    'Stock': stock.replace('.NS', ''),
                    'Price': current,
                    'Change %': change_pct
                })
        except:
            pass
    
    if results:
        df = pd.DataFrame(results)
        print(f"Status: ✅ WORKING")
        print(df.to_string(index=False))
    else:
        print("Status: ❌ NO DATA RETURNED")
except Exception as e:
    print(f"Status: ❌ ERROR - {e}")

# ============================================================================
# TEST 6: TECHNICAL INDICATORS
# ============================================================================

print("\n✅ TEST 6: TECHNICAL INDICATORS (RSI, MACD)")
print("-" * 80)

try:
    ticker = yf.Ticker('TCS.NS')
    data = ticker.history(period='1y')
    
    if len(data) >= 200:
        print(f"Status: ✅ WORKING")
        
        close = data['Close']
        
        # RSI 14
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        print(f"RSI 14: {rsi.iloc[-1]:.2f}")
        
        # SMA
        sma20 = close.rolling(window=20).mean()
        sma50 = close.rolling(window=50).mean()
        sma200 = close.rolling(window=200).mean()
        
        print(f"SMA 20: ₹{sma20.iloc[-1]:.2f}")
        print(f"SMA 50: ₹{sma50.iloc[-1]:.2f}")
        print(f"SMA 200: ₹{sma200.iloc[-1]:.2f}")
        
        # MACD
        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()
        macd = ema12 - ema26
        macd_signal = macd.ewm(span=9).mean()
        
        print(f"MACD: {macd.iloc[-1]:.4f}")
        print(f"MACD Signal: {macd_signal.iloc[-1]:.4f}")
        print(f"Trend: {'Bullish' if macd.iloc[-1] > macd_signal.iloc[-1] else 'Bearish'}")
    else:
        print(f"Status: ⚠️ NOT ENOUGH DATA (Need 200, Have {len(data)})")
except Exception as e:
    print(f"Status: ❌ ERROR - {e}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("📊 SUMMARY")
print("="*80)

print("""
✅ If all tests show WORKING:
   └─ Your APIs are configured correctly!
   └─ Data should update every 5 minutes

⚠️ If some tests show NO DATA:
   └─ Market may be closed
   └─ Try running script during market hours (9:15 AM - 3:30 PM IST)

❌ If you see ERROR messages:
   └─ Check internet connection
   └─ Try: pip install --upgrade yfinance requests
   └─ Check firewall/antivirus blocking APIs

📝 NOTES:
   • Market hours: Mon-Fri 9:15 AM - 3:30 PM IST
   • Prices update only during market hours
   • After market hours, you'll see previous close prices
   • API caching: Prices refresh every 5 minutes
""")

print("="*80)
print("✅ Debug script complete!")
print("="*80)
