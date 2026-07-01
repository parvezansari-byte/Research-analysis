"""
ENHANCED STOCKS & SECTORS DATABASE
100+ NSE Stocks + 20+ Sectors + Advanced Technical Indicators
"""

# ============================================================================
# COMPREHENSIVE STOCK LIST (100+ STOCKS)
# ============================================================================

NSE_STOCKS = {
    # BANKING (15 stocks)
    'Banking': [
        'HDFCBANK.NS', 'ICICIBANK.NS', 'AXISBANK.NS', 'KOTAKBANK.NS', 
        'IDFCFIRSTB.NS', 'SBI.NS', 'INDUSINDBK.NS', 'FEDERALBNK.NS',
        'UBIBANK.NS', 'BANKBARODA.NS', 'BANDHANBNK.NS', 'YESBANK.NS',
        'AUBANK.NS', 'CAREBANK.NS', 'PNBHOUSING.NS'
    ],
    
    # IT & SOFTWARE (12 stocks)
    'IT': [
        'TCS.NS', 'INFY.NS', 'WIPRO.NS', 'HCL-INSYS.NS', 'MINDTREE.NS',
        'LTTS.NS', 'PERSIST.NS', 'COFORGE.NS', 'MPHASIS.NS', 'KPITTECH.NS',
        'SONACOMS.NS', 'CYIENT.NS'
    ],
    
    # ENERGY & POWER (12 stocks)
    'Energy': [
        'RELIANCE.NS', 'NTPC.NS', 'POWERGRID.NS', 'ONGC.NS', 'OILNLGAS.NS',
        'IOCL.NS', 'BPCL.NS', 'ADANIGREEN.NS', 'ADANIPOWER.NS', 'TATAPOWER.NS',
        'TORRENTPHAR.NS', 'INFORTECH.NS'
    ],
    
    # AUTOMOBILES (12 stocks)
    'Auto': [
        'MARUTI.NS', 'TATAMOTORS.NS', 'MAHINDRA.NS', 'BAJAJ-AUTO.NS',
        'HEROMOTOCO.NS', 'EICHER.NS', 'MOTORCORP.NS', 'ASHOKLEY.NS',
        'SUNTV.NS', 'CUMMINSIND.NS', 'BOSCHLTD.NS', 'GRAPHITE.NS'
    ],
    
    # PHARMA & HEALTHCARE (15 stocks)
    'Pharma': [
        'SUNPHARMA.NS', 'LUPIN.NS', 'DRREDDY.NS', 'CIPLA.NS', 'STRIDES.NS',
        'AUROPHARMA.NS', 'ABBOTINDIA.NS', 'GLAXOSMITHKLINE.NS', 'ZYDUSLIFE.NS',
        'DIVISLAB.NS', 'NATCPHARMA.NS', 'PFIZER.NS', 'SANOFI.NS',
        'BIOCON.NS', 'APOLLOHOSP.NS'
    ],
    
    # FMCG (12 stocks)
    'FMCG': [
        'HINDUNILVR.NS', 'ITC.NS', 'NESTLEIND.NS', 'ASIANPAINT.NS',
        'BRITANNIA.NS', 'MARICO.NS', 'EMAMILTD.NS', 'GODREJCP.NS',
        'JYOTHYLAB.NS', 'COLPAL.NS', 'UNILEVER.NS', 'FRONTLINE.NS'
    ],
    
    # METALS & MINING (10 stocks)
    'Metals': [
        'HINDALCO.NS', 'VEDL.NS', 'JINDALSTEL.NS', 'TATASTEEL.NS',
        'NMDC.NS', 'JSPL.NS', 'MOIL.NS', 'NATIONALAL.NS',
        'SAILINDST.NS', 'RPOWER.NS'
    ],
    
    # INFRASTRUCTURE (12 stocks)
    'Infrastructure': [
        'LT.NS', 'SIEMENS.NS', 'GODREJPROP.NS', 'DLF.NS', 'OBEROI.NS',
        'PRESTIGE.NS', 'BRIGADE.NS', 'MAGICBRICKS.NS', 'NBCC.NS',
        'ICCBANK.NS', 'IIFL.NS', 'BHEL.NS'
    ],
    
    # FINANCE & INSURANCE (12 stocks)
    'Finance': [
        'BAJAJFINSV.NS', 'JIOFINANCIAL.NS', 'HDFCLIFE.NS', 'ICICIPRULI.NS',
        'SBILIFE.NS', 'MOTILALOFS.NS', 'ICICISECURITIES.NS', 'SHYAMMETALL.NS',
        'ADFNONFOODS.NS', 'GICREF.NS', 'INDIANB.NS', 'AXISBANK.NS'
    ],
    
    # TELECOM (8 stocks)
    'Telecom': [
        'JIO.NS', 'AIRTELGLOBAL.NS', 'VODAFONE.NS', 'STEL.NS',
        'BSNL.NS', 'MTNL.NS', 'TATACOMM.NS', 'INDIAONL.NS'
    ],
    
    # UTILITIES (8 stocks)
    'Utilities': [
        'ADANIPORTS.NS', 'ADANIENTERP.NS', 'APOLLOHOSP.NS', 'WIPRO.NS',
        'BHARTIARTL.NS', 'IBULHSGFIN.NS', 'INDHOTEL.NS', 'IRCTC.NS'
    ]
}

# ============================================================================
# EXPANDED SECTORS (20+ SECTORS)
# ============================================================================

SECTOR_DATA = {
    'Banking': 1.89,
    'IT': 2.45,
    'Energy': 3.12,
    'Auto': 0.23,
    'Pharma': -0.56,
    'FMCG': -1.23,
    'Metals': 1.67,
    'Infrastructure': -0.34,
    'Finance': 0.95,
    'Telecom': 0.89,
    'Utilities': 1.45,
    'Media': 1.23,
    'Textiles': -0.45,
    'Food & Beverage': 0.67,
    'Hotels & Tourism': 1.34,
    'Chemicals': 0.56,
    'Retail': 0.78,
    'Real Estate': -0.12,
    'Cement': 1.12,
    'Steel': 1.89,
    'Logistics': 0.45,
    'Renewable Energy': 2.34,
}

# ============================================================================
# ADVANCED TECHNICAL INDICATORS
# ============================================================================

TECHNICAL_INDICATORS = {
    'Trend Indicators': [
        'SMA (20, 50, 200)',
        'EMA (12, 26)',
        'MACD',
        'ADX (Average Directional Index)',
        'Parabolic SAR',
    ],
    'Momentum Indicators': [
        'RSI (Relative Strength Index)',
        'Stochastic Oscillator',
        'Williams %R',
        'Momentum',
        'Rate of Change (ROC)',
    ],
    'Volatility Indicators': [
        'Bollinger Bands',
        'ATR (Average True Range)',
        'Standard Deviation',
        'Keltner Channel',
        'Donchian Channel',
    ],
    'Volume Indicators': [
        'On Balance Volume (OBV)',
        'Volume Rate of Change',
        'Accumulation/Distribution Line',
        'Money Flow Index (MFI)',
        'Chaikin Money Flow',
    ],
    'Support & Resistance': [
        'Pivot Points',
        'Fibonacci Retracement',
        'Fibonacci Extension',
        'Support & Resistance Levels',
        'Camarilla Pivot',
    ],
    'Pattern Recognition': [
        'Head & Shoulders',
        'Double Top/Bottom',
        'Triangle Pattern',
        'Flag Pattern',
        'Cup & Handle',
    ]
}

# ============================================================================
# INDICATOR DESCRIPTIONS
# ============================================================================

INDICATOR_DESCRIPTIONS = {
    'SMA': 'Simple Moving Average - Trend direction (20=short, 50=medium, 200=long)',
    'EMA': 'Exponential Moving Average - More responsive to price changes',
    'RSI': 'Relative Strength Index - Overbought (>70) or Oversold (<30)',
    'MACD': 'Moving Average Convergence Divergence - Trend and momentum',
    'Stochastic': 'Stochastic Oscillator - Momentum and overbought/oversold levels',
    'Williams %R': "Williams Percentage Range - Similar to Stochastic, -80 to -20 oversold",
    'Momentum': 'Rate of price change - Strength of trend',
    'ROC': 'Rate of Change - Percentage price change over period',
    'Bollinger Bands': 'Volatility indicator - Price bands around SMA',
    'ATR': 'Average True Range - Volatility measure',
    'OBV': 'On Balance Volume - Relationship between price and volume',
    'MFI': 'Money Flow Index - Volume-weighted momentum',
    'Pivot Points': 'Support and resistance levels calculated from previous price',
    'Fibonacci': 'Retracement levels - 23.6%, 38.2%, 50%, 61.8%, 78.6%',
    'ADX': 'Average Directional Index - Trend strength (>25 = strong trend)',
    'Parabolic SAR': 'Stop and Reverse - Trend reversal indicator',
}

# ============================================================================
# SIGNAL GENERATION RULES
# ============================================================================

BUY_SIGNALS = {
    'RSI': 'RSI < 30 (Oversold)',
    'MACD': 'MACD crosses above signal line (Bullish)',
    'SMA': 'Price crosses above SMA 200 (Golden Cross)',
    'Stochastic': 'Stochastic < 20 (Oversold)',
    'ADX': 'ADX > 25 with +DI > -DI (Strong uptrend)',
    'Fibonacci': 'Price at 38.2% or 61.8% retracement',
    'Volume': 'Volume > 20-day average with price increase',
}

SELL_SIGNALS = {
    'RSI': 'RSI > 70 (Overbought)',
    'MACD': 'MACD crosses below signal line (Bearish)',
    'SMA': 'Price crosses below SMA 200 (Death Cross)',
    'Stochastic': 'Stochastic > 80 (Overbought)',
    'ADX': 'ADX > 25 with -DI > +DI (Strong downtrend)',
    'Fibonacci': 'Price at resistance (0% or 23.6%)',
    'Volume': 'Volume > 20-day average with price decrease',
}

# ============================================================================
# STOCK INFORMATION
# ============================================================================

STOCK_INFO = {
    'RELIANCE.NS': {
        'name': 'Reliance Industries',
        'sector': 'Energy',
        'industry': 'Oil & Gas',
        'market_cap': '₹18.5 Trillion',
        'pe': 21.5,
        'dividend_yield': 1.85,
    },
    'TCS.NS': {
        'name': 'Tata Consultancy Services',
        'sector': 'IT',
        'industry': 'Software',
        'market_cap': '₹14.2 Trillion',
        'pe': 25.3,
        'dividend_yield': 2.34,
    },
    'INFY.NS': {
        'name': 'Infosys',
        'sector': 'IT',
        'industry': 'Software',
        'market_cap': '₹8.9 Trillion',
        'pe': 24.1,
        'dividend_yield': 1.56,
    },
    'HDFCBANK.NS': {
        'name': 'HDFC Bank',
        'sector': 'Banking',
        'industry': 'Banking',
        'market_cap': '₹16.3 Trillion',
        'pe': 23.7,
        'dividend_yield': 0.95,
    },
}

def get_all_stocks():
    """Get all 100+ stocks"""
    all_stocks = []
    for sector, stocks in NSE_STOCKS.items():
        all_stocks.extend(stocks)
    return sorted(list(set(all_stocks)))

def get_stocks_by_sector(sector):
    """Get stocks in specific sector"""
    return NSE_STOCKS.get(sector, [])

def get_all_sectors():
    """Get all sectors"""
    return sorted(list(NSE_STOCKS.keys()))

def get_sector_performance():
    """Get all sector performance data"""
    return SECTOR_DATA

def get_technical_indicators_list():
    """Get all technical indicators grouped by category"""
    return TECHNICAL_INDICATORS

def get_indicator_description(indicator):
    """Get description of specific indicator"""
    return INDICATOR_DESCRIPTIONS.get(indicator, 'No description available')
