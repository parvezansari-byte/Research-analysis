"""
VISUAL ENHANCEMENTS - THEME SYSTEM
Beautiful Dark/Light Mode with Enhanced Styling
"""

# ============================================================================
# THEME CONFIGURATION
# ============================================================================

DARK_THEME = {
    'name': 'Dark',
    'primary_bg': '#0f1729',
    'secondary_bg': '#1a2332',
    'card_bg': 'linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%)',
    'text_primary': '#ffffff',
    'text_secondary': '#cbd5e1',
    'text_muted': '#94a3b8',
    'accent_blue': '#2563eb',
    'accent_teal': '#06b6d4',
    'accent_green': '#10b981',
    'accent_red': '#ef4444',
    'border_color': 'rgba(148, 163, 184, 0.2)',
    'shadow': '0 8px 32px rgba(0, 0, 0, 0.4)',
}

LIGHT_THEME = {
    'name': 'Light',
    'primary_bg': '#f8fafc',
    'secondary_bg': '#f1f5f9',
    'card_bg': 'linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%)',
    'text_primary': '#0f172a',
    'text_secondary': '#475569',
    'text_muted': '#64748b',
    'accent_blue': '#0284c7',
    'accent_teal': '#0d9488',
    'accent_green': '#059669',
    'accent_red': '#dc2626',
    'border_color': 'rgba(0, 0, 0, 0.1)',
    'shadow': '0 8px 32px rgba(0, 0, 0, 0.1)',
}

# ============================================================================
# ENHANCED CSS STYLING
# ============================================================================

ENHANCED_CSS = """
<style>
    /* Smooth Transitions */
    * {
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(148, 163, 184, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #2563eb 0%, #06b6d4 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #1e40af 0%, #0891b2 100%);
    }
    
    /* Button Animations */
    button {
        position: relative;
        overflow: hidden;
    }
    
    button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    /* Card Hover Effects */
    .metric-card {
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        transform: translateY(0);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
    }
    
    /* Smooth Text Animation */
    .header-title {
        font-size: 28px;
        font-weight: 900;
        background: linear-gradient(135deg, #2563eb, #06b6d4, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 4s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
    }
    
    /* Fade-in Animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stMetric {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Chart Container */
    .plotly-container {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    /* Section Header Styling */
    .section-header {
        font-size: 24px;
        font-weight: 800;
        margin: 32px 0 20px 0;
        padding-bottom: 12px;
        border-bottom: 2px solid;
        border-image: linear-gradient(90deg, #2563eb, #06b6d4, #10b981) 1;
    }
    
    /* Divider Enhancement */
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #2563eb, transparent);
    }
    
    /* Tooltip Styling */
    .tooltip {
        background: linear-gradient(135deg, #1e40af, #0891b2);
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
</style>
"""

# ============================================================================
# ENHANCED CARD GENERATOR
# ============================================================================

def create_gradient_card(title, value, subtitle, color_from, color_to, icon="📊"):
    """Create an enhanced gradient card with animations"""
    return f"""
    <div style="
        background: linear-gradient(135deg, {color_from} 0%, {color_to} 100%);
        border-radius: 16px;
        padding: 28px;
        color: white;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    " class="metric-card">
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.1), transparent);
            pointer-events: none;
        "></div>
        <div style="position: relative; z-index: 1;">
            <div style="
                font-size: 14px;
                opacity: 0.85;
                font-weight: 700;
                margin-bottom: 12px;
                letter-spacing: 1px;
                text-transform: uppercase;
            ">{icon} {title}</div>
            <div style="
                font-size: 36px;
                font-weight: 900;
                margin-bottom: 10px;
                letter-spacing: -1px;
            ">{value}</div>
            <div style="
                font-size: 12px;
                opacity: 0.8;
            ">{subtitle}</div>
        </div>
    </div>
    """

def create_stat_box(label, value, change_pct=None, icon="📊"):
    """Create a beautiful stat box with optional change indicator"""
    change_color = "#10b981" if change_pct and change_pct > 0 else "#ef4444"
    change_arrow = "▲" if change_pct and change_pct > 0 else "▼"
    change_text = f"{change_arrow} {abs(change_pct):.2f}%" if change_pct else ""
    
    return f"""
    <div style="
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(6, 182, 212, 0.1));
        border: 1px solid rgba(37, 99, 235, 0.2);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        transition: all 0.3s ease;
    ">
        <div style="
            font-size: 13px;
            color: #94a3b8;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        ">{icon} {label}</div>
        <div style="
            font-size: 24px;
            font-weight: 900;
            color: #fff;
            margin-bottom: 6px;
        ">{value}</div>
        {f'<div style="font-size: 12px; color: {change_color}; font-weight: 700;">{change_text}</div>' if change_text else ''}
    </div>
    """

# ============================================================================
# THEME SWITCHER
# ============================================================================

def get_theme_css(theme):
    """Get CSS variables for current theme"""
    return f"""
    <style>
        :root {{
            --primary-bg: {theme['primary_bg']};
            --secondary-bg: {theme['secondary_bg']};
            --text-primary: {theme['text_primary']};
            --text-secondary: {theme['text_secondary']};
            --text-muted: {theme['text_muted']};
            --accent-blue: {theme['accent_blue']};
            --accent-teal: {theme['accent_teal']};
            --accent-green: {theme['accent_green']};
            --accent-red: {theme['accent_red']};
            --border-color: {theme['border_color']};
            --shadow: {theme['shadow']};
        }}
        
        body {{
            background-color: {theme['primary_bg']};
            color: {theme['text_primary']};
        }}
        
        [data-testid="stMainBlockContainer"] {{
            background: {theme['primary_bg']};
        }}
        
        .stMarkdown {{
            color: {theme['text_primary']};
        }}
    </style>
    """

# ============================================================================
# CHART STYLING TEMPLATES
# ============================================================================

CHART_TEMPLATE = {
    'layout': {
        'template': 'plotly_dark',
        'paper_bgcolor': 'rgba(15, 23, 42, 0.5)',
        'plot_bgcolor': 'rgba(15, 23, 42, 0.3)',
        'font': {
            'family': 'Arial, sans-serif',
            'color': '#ffffff',
            'size': 12,
        },
        'hovermode': 'x unified',
        'margin': {'l': 60, 'r': 60, 't': 80, 'b': 60},
        'title': {
            'font': {'size': 20, 'color': '#ffffff', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center',
        }
    }
}

# ============================================================================
# COLOR PALETTES
# ============================================================================

GRADIENT_PALETTES = {
    'blue_teal': ['#1e40af', '#0891b2'],
    'blue_green': ['#2563eb', '#10b981'],
    'teal_cyan': ['#0891b2', '#06b6d4'],
    'green_emerald': ['#059669', '#10b981'],
    'purple_blue': ['#7c3aed', '#2563eb'],
    'red_orange': ['#dc2626', '#f97316'],
    'gradient_full': ['#2563eb', '#06b6d4', '#10b981'],
}

CHART_COLORS = {
    'positive': '#10b981',  # Green
    'negative': '#ef4444',  # Red
    'neutral': '#3b82f6',   # Blue
    'warning': '#f59e0b',   # Orange
    'info': '#06b6d4',      # Teal
}

# ============================================================================
# ANIMATION CLASSES
# ============================================================================

ANIMATIONS = {
    'fade_in': 'animation: fadeIn 0.5s ease-out;',
    'slide_in': 'animation: slideIn 0.6s ease-out;',
    'bounce': 'animation: bounce 0.6s ease-in-out;',
    'pulse': 'animation: pulse 2s infinite;',
    'glow': 'animation: glow 2s ease-in-out infinite;',
}
