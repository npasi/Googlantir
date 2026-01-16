import streamlit as st
import forecaster  
from datetime import timedelta

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Googlantir",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GOOGLE LIGHT THEME CSS ---
COLORS = {
    "blue": "#1a73e8",       
    "red": "#d93025",        
    "yellow": "#f9ab00",     
    "green": "#1e8e3e",      
    "text_main": "#202124",  
    "text_sec": "#5f6368",   
    "bg_light": "#f8f9fa",   
    "bg_accent": "#f1f3f4",  
    "border": "#dadce0"      
}

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Product+Sans:wght@300;400;700&family=Google+Sans:wght@400;500;700&family=Roboto:wght@300;400;500&display=swap');

    /* BASE LIGHT THEME */
    .stApp {{
        font-family: 'Google Sans', 'Product Sans', 'Roboto', sans-serif;
        color: {COLORS['text_main']};
        background-color: #FFFFFF;
        background-image: 
            radial-gradient(circle at 0% 0%, rgba(234, 67, 53, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 100% 0%, rgba(251, 188, 4, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 100% 100%, rgba(66, 133, 244, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 0% 100%, rgba(52, 168, 83, 0.05) 0%, transparent 50%);
        background-attachment: fixed;
    }}
    
    header[data-testid="stHeader"] {{
        background-color: {COLORS['bg_accent']} !important;
        border-bottom: 1px solid {COLORS['border']};
        z-index: 1;
    }}
    
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 95% !important;
    }}

    /* --- EXPANDER STYLING (INGRANDITO) --- */
    .streamlit-expanderHeader {{
        font-family: 'Google Sans', sans-serif !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: {COLORS['blue']} !important;
        background-color: #f8f9fa;
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        margin-bottom: 10px;
        padding-top: 15px !important;
        padding-bottom: 15px !important;
    }}
    
    /* --- FIX UI COLORS --- */
    [data-testid="stRadio"] p {{ color: #202124 !important; font-weight: 500 !important; }}
    [data-testid="stRadio"] div[role="radiogroup"] label {{ color: #202124 !important; }}
    [data-testid="stCheckbox"] label p, [data-testid="stSidebar"] label p {{ color: #202124 !important; font-weight: 600 !important; }}

    /* --- ALERT STYLE --- */
    [data-testid="stAlert"] {{
        background-color: #fce8e6 !important; 
        border: 1px solid {COLORS['red']} !important;
        color: #c5221f !important;
        border-radius: 8px;
    }}
    [data-testid="stAlert"] div, [data-testid="stAlert"] p {{ color: #202124 !important; }}
    [data-testid="stAlert"] svg {{ fill: {COLORS['red']} !important; }}

    /* --- CARDS --- */
    .google-card {{
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 30px;
        height: 100%;
        border: 1px solid {COLORS['border']};
        box-shadow: 0 2px 5px rgba(60,64,67,0.1);
    }}
    .border-top-blue {{ border-top: 6px solid {COLORS['blue']}; }}
    .border-top-red {{ border-top: 6px solid {COLORS['red']}; }}
    .border-top-yellow {{ border-top: 6px solid {COLORS['yellow']}; }}
    .border-top-green {{ border-top: 6px solid {COLORS['green']}; }}

    .card-body {{ font-family: 'Roboto'; font-size: 1.1rem; line-height: 1.6; color: {COLORS['text_sec']}; }}
    
    /* --- TABLE --- */
    .google-table {{ width: 100%; border-collapse: collapse; font-family: 'Roboto', sans-serif; margin-top: 20px; }}
    .google-table th {{ text-align: left; padding: 12px; border-bottom: 2px solid {COLORS['border']}; color: {COLORS['text_sec']}; background-color: {COLORS['bg_accent']}; }}
    .google-table td {{ padding: 12px; border-bottom: 1px solid {COLORS['border']}; color: {COLORS['text_main']}; vertical-align: top; }}

    /* --- PLOTLY CONTAINER --- */
    [data-testid="stPlotlyChart"] {{
        width: 100%; background-color: #FFFFFF; border-radius: 16px; border: 1px solid {COLORS['border']};
        box-shadow: 0 2px 6px rgba(60,64,67,0.1); padding: 15px;
    }}

    /* --- SIDEBAR --- */
    [data-testid="stSidebar"] {{ background-color: #FFFFFF; border-right: 6px solid {COLORS['blue']}; }}
    
    .google-outline {{ -webkit-text-stroke: 1.5px #FFFFFF; paint-order: stroke fill; text-shadow: 0px 2px 5px rgba(0,0,0,0.15); }}
    .google-main-title {{
        font-family: 'Product Sans', 'Google Sans', sans-serif; font-weight: 700; font-size: 5rem;
        letter-spacing: -1.5px; text-align: center !important; width: 100%; display: block;
        margin-top: 20px; margin-bottom: 10px; line-height: 1.2; padding-top: 10px;
    }}
    
    .stButton > button {{
        background-color: {COLORS['blue']}; color: white !important; border-radius: 8px; padding: 0.8rem 2.5rem;
        font-size: 1.3rem; font-weight: 700; border: none; box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        font-family: 'Google Sans'; width: 100%; text-transform: uppercase; letter-spacing: 1px;
    }}
    .spacer-div {{ height: 50px; }}
    </style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---

def generate_colored_text(text, css_class="", font_size=""):
    colors = [COLORS['blue'], COLORS['red'], COLORS['yellow'], COLORS['blue'], COLORS['green'], COLORS['red']]
    style_attr = f'style="font-size:{font_size}; font-weight:700; font-family:\'Google Sans\';"' if font_size else ""
    final_class = f"{css_class} google-outline"
    html = f'<div class="{final_class}" {style_attr}>'
    char_count = 0
    for char in text:
        if char == " ": html += "&nbsp;"
        else:
            color = colors[char_count % len(colors)]
            html += f'<span style="color:{color}">{char}</span>'
            char_count += 1
    html += '</div>'
    return html

@st.cache_resource
def get_model(context_len, forecasting_horizon):
    return forecaster.load_timesfm_model(context_len, forecasting_horizon)

# --- 4. APP UI ---

# --- HEADER SECTION ---
st.markdown(generate_colored_text("Googlantir", "google-main-title"), unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; margin-top: -30px; margin-bottom: 40px; font-family: "Product Sans", sans-serif; font-weight: 300; font-size: 1.6rem; color: #202124;'>
        <br>- "What if Google stole a Palantír?" -
    </div>
""", unsafe_allow_html=True)

# --- PROFESSIONAL NOTE ---
st.markdown("""
    <div style='text-align: center; margin-bottom: 25px; font-family: "Roboto", sans-serif; color: #5f6368; font-size: 0.95rem; line-height: 1.5;'>
        Forecaster powered by <b>Google Research TimesFM</b> architecture, a foundation model designed for zero-shot time-series forecasting across diverse domains and granularities.
    </div>
""", unsafe_allow_html=True)

# INFO CARDS
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div class="google-card border-top-blue">
        <div style="text-align:center; margin-bottom:15px;">{generate_colored_text("Context Length", font_size="1.5rem")}</div>
        <div class="card-body">
            <b>How much history do we take into account?</b><br>
            It has to be balanced considering the<br><b>NOISE-BIAS TRADEOFF</b>.<br><br>
            • <b>Long (1024):</b> Great for capturing seasonal patterns.<br>
            • <b>Short (64):</b> Good for reacting to recents shifts.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="google-card border-top-red">
        <div style="text-align:center; margin-bottom:15px;">{generate_colored_text("Horizon Length", font_size="1.5rem")}</div>
        <div class="card-body">
            <b>How far ahead are we looking?</b><br>
            Predicting tomorrow is easy. Predicting next month is hard.<br><br>
            • <b>Short:</b> Point-in-time confidence level.<br>
            • <b>Long:</b> Cumulative error rate grows.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="google-card border-top-yellow">
        <div style="text-align:center; margin-bottom:15px;">{generate_colored_text("Confidence", font_size="1.5rem")}</div>
        <div class="card-body">
            <b>Risk & Confidence Levels</b><br>
            Multi-tier intervals to assess forecast reliability:<br><br>
        • <b>Conservative (10-90):</b> Worst/Best Case.<br>
        • <b>Aggressive (30-70):</b> Likely outcome.<br>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="spacer-div"></div>', unsafe_allow_html=True)

# DEEP DIVE SECTION
st.markdown(f"""
<div class="google-card" style="background-color:rgba(248, 249, 250, 0.9); margin-bottom: 20px;">
    <div style="text-align:center; margin-bottom:20px;">
        {generate_colored_text("The Memory-Vision Trade-off", font_size="1.8rem")}
    </div>
    <div class="card-body" style="text-align:center; font-size:1.1rem; color:#4a5568;">
        Forecasting is a <b>dynamic equilibrium</b> between <b>Structural Memory</b> and <b>Adaptive Vision</b>. 
    </div>
</div>
""", unsafe_allow_html=True)

# --- EXPANDERS ---
with st.expander("📚 Guide: Tactical vs Strategic Horizon Configuration (Click to Expand)", expanded=False):
    st.markdown(f"""
    <h2 style='font-family:"Google Sans"; color:{COLORS['text_main']}; text-align:center;'>Configuration Guide: Forecast Horizon</h2>
    <p style='text-align:center; color:{COLORS['text_sec']}; max-width:800px; margin:0 auto 30px auto;'>
        The selection of the <b>Horizon Length</b> defines the strategic nature of your forecast. 
        Below is the breakdown between Tactical (Short) and Strategic (Long) approaches.
    </p>
    """, unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        st.markdown(f"""
        <div class="google-card border-top-green" style="padding:20px;">
            <div style="color:{COLORS['green']}; font-weight:bold; font-size:1.2rem; margin-bottom:10px;">1. Tactical Horizon (Short-Term)</div>
            <div class="card-body" style="font-size:0.95rem;">
                <b>Focus: Operational Efficiency</b><br>
                The model leverages recent data inertia. Events from the last few days determine the prediction.<br><br>
                • <b>Characteristics:</b> High precision, low variance.<br>
                • <b>Objective:</b> Logistics, stock for the weekend, real-time anomalies.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with g2:
        st.markdown(f"""
        <div class="google-card border-top-blue" style="padding:20px;">
            <div style="color:{COLORS['blue']}; font-weight:bold; font-size:1.2rem; margin-bottom:10px;">2. Strategic Horizon (Long-Term)</div>
            <div class="card-body" style="font-size:0.95rem;">
                <b>Focus: Planning & Macro Trends</b><br>
                Pushes the model beyond inertia, forcing it to rely on structural seasonality patterns.<br><br>
                • <b>Characteristics:</b> Reliable on trend direction, volatile on exact numbers.<br>
                • <b>Objective:</b> Annual budgeting, supply contracts.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <table class="google-table">
        <tr style="background-color:{COLORS['bg_accent']};">
            <th>Type</th><th>Typical Configuration</th><th>Primary Goal</th><th>Risk Profile</th>
        </tr>
        <tr><td><b>Operational (Short)</b></td><td>1 - 7 steps</td><td><b>Efficiency</b></td><td><span style="color:{COLORS['green']};">Low</span> (High Confidence)</td></tr>
        <tr><td><b>Tactical (Mid)</b></td><td>12 - 30 steps</td><td><b>Allocation</b></td><td><span style="color:{COLORS['yellow']};">Medium</span> (Divergence begins)</td></tr>
        <tr><td><b>Strategic (Long)</b></td><td>60 - 100+ steps</td><td><b>Vision</b></td><td><span style="color:{COLORS['red']};">High</span> (Trend Reliance)</td></tr>
    </table>
    <div style="margin-top:20px; padding:15px; background-color:#e8f0fe; border-radius:8px; color:{COLORS['blue']}; font-family:'Roboto'; border-left:5px solid {COLORS['blue']};">
        <b>💡 Pro Tip: Input/Output Ratio</b><br>
        If your goal is a Long Horizon, ensure that the Context Length is at least <b>3 to 4 times longer</b> than the requested horizon.
    </div>
    """, unsafe_allow_html=True)

with st.expander("🧠 Guide: Balancing Context Length & Memory Span (Click to Expand)", expanded=False):
    st.markdown(f"""
    <h2 style='font-family:"Google Sans"; color:{COLORS['text_main']}; text-align:center;'>Configuration Guide: Context Length</h2>
    <p style='text-align:center; color:{COLORS['text_sec']}; max-width:800px; margin:0 auto 30px auto;'>
        Context Length determines the <b>Memory Span</b> of the model. 
        It defines how much history the AI processes to understand the current state.
        The challenge is balancing <b>Responsiveness</b> (Short Memory) vs <b>Pattern Recognition</b> (Long Memory).
    </p>
    """, unsafe_allow_html=True)

    c_guide1, c_guide2 = st.columns(2)
    with c_guide1:
        st.markdown(f"""
        <div class="google-card border-top-yellow" style="padding:20px;">
            <div style="color:{COLORS['yellow']}; font-weight:bold; font-size:1.2rem; margin-bottom:10px;">1. Short Memory (Reactive)</div>
            <div class="card-body" style="font-size:0.95rem;">
                <b>Focus: Recent Volatility & Trends</b><br>
                The model ignores the distant past and focuses only on the latest price action. It behaves like a day-trader.<br><br>
                • <b>Best for:</b> Assets that changed behavior recently (e.g., after a news event).<br>
                • <b>Risk:</b> "Blindness" to seasonal cycles (e.g., forgetting that sales peak in December).
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c_guide2:
        st.markdown(f"""
        <div class="google-card border-top-blue" style="padding:20px;">
            <div style="color:{COLORS['blue']}; font-weight:bold; font-size:1.2rem; margin-bottom:10px;">2. Long Memory (Cyclical)</div>
            <div class="card-body" style="font-size:0.95rem;">
                <b>Focus: Seasonality & Structure</b><br>
                The model looks far back to find repeating patterns (weekly, monthly, yearly). It behaves like a macro-economist.<br><br>
                • <b>Best for:</b> Stable businesses with recurring revenue (Retail, Energy, SaaS).<br>
                • <b>Risk:</b> "Inertia". Old data might dilute the signal of a new, emerging trend.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <table class="google-table">
        <tr style="background-color:{COLORS['bg_accent']};">
            <th>Configuration</th><th>Input Length</th><th>Ideal Use Case</th><th>The Trade-off</th>
        </tr>
        <tr><td><b>Short Context</b></td><td>32 - 96 steps</td><td><b>Crypto / Breaking News</b></td><td><b>High Sensitivity</b> (Reacts fast, potential noise)</td></tr>
        <tr><td><b>Medium Context</b></td><td>128 - 300 steps</td><td><b>Swing Trading</b></td><td><b>Balanced</b> (Trend + Inertia)</td></tr>
        <tr><td><b>Long Context</b></td><td>512 - 1024 steps</td><td><b>Retail / Macro</b></td><td><b>High Stability</b> (Captures "Big Picture")</td></tr>
    </table>
    <div style="margin-top:20px; padding:15px; background-color:#fff8e1; border-radius:8px; color:#b7791f; font-family:'Roboto'; border-left:5px solid {COLORS['yellow']};">
        <b>💡 Pro Tip: The "Full Cycle" Rule</b><br>
        To capture seasonality effectively, your Context Length must cover <b>at least one full cycle</b> of the pattern you want to predict.
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="spacer-div"></div>', unsafe_allow_html=True)

# --- CHEAT SHEET SECTION ---
st.markdown(generate_colored_text("Quick Reference Cheat Sheet", font_size="1.8rem"), unsafe_allow_html=True)
st.markdown(f"""
<table class="google-table">
    <tr style="background-color:{COLORS['bg_accent']};">
        <th>Granularity (Candle)</th>
        <th>Trading Style / Analysis</th>
        <th>Forecast Horizon</th>
        <th>Optimal Context Length</th>
        <th>Rationale</th>
    </tr>
    <tr>
        <td><b>1 Hour</b></td>
        <td>Day Trading</td>
        <td>6 - 12 Hours</td>
        <td><b>168</b> (1 Week)</td>
        <td>Crucial: 168h covers a full week. The model learns the difference between Monday morning and Friday evening.</td>
    </tr>
    <tr>
        <td><b>1 Day</b></td>
        <td>Swing Trading (Short)</td>
        <td>3 - 7 Days</td>
        <td><b>90</b> (1 Quarter)</td>
        <td>Sufficient to capture quarterly trends (earnings cycle) and project the week.</td>
    </tr>
    <tr>
        <td><b>1 Day</b></td>
        <td>Position Trading</td>
        <td>14 - 30 Days</td>
        <td><b>365 - 512</b> (1 Year+)</td>
        <td>To predict a full month, the model <i>must</i> have seen the full annual seasonality.</td>
    </tr>
    <tr>
        <td><b>1 Week</b></td>
        <td>Macro Investing</td>
        <td>4 - 12 Weeks</td>
        <td><b>104 - 200</b> (2-4 Years)</td>
        <td>Weekly data has less noise. Requires long history to understand multi-year economic cycles.</td>
    </tr>
</table>
""", unsafe_allow_html=True)

st.markdown('<div class="spacer-div"></div>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown(generate_colored_text("Settings", font_size="1.8rem"), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    ticker = st.text_input("Insert Ticker", "GOOGL")
    
    analysis_mode = st.radio(
        "Analysis Mode", 
        ["Standard (Daily)", "Deep Dive (Hourly)", "Macro (Weekly)"], 
        index=0
    )
    
    if "Deep Dive" in analysis_mode:
        st.info("ℹ️ Deep Dive enables 1-hour resolution.")
        
        period = st.selectbox("Deep Dive Period", ["5 days", "1 week", "2 weeks", "1 month", "3 months"], index=1)
        interval_code = "1h"
        default_context = 48 
        default_horizon = 7  
        unit_label = "Hours"
        max_horizon = 35
        
    elif "Macro" in analysis_mode:
        st.info("ℹ️ Macro Mode enables 1-week resolution for long-term trends.")
        period = st.selectbox("Macro Period", ["1 year", "2 years", "5 years", "10 years", "Max"], index=1)
        interval_code = "1wk"
        default_context = 104 
        default_horizon = 4   
        unit_label = "Weeks"
        max_horizon = 52 
        
    else:
        period = st.selectbox("Historical Period", ["6 months", "1 year", "2 years", "5 years", "Max"], index=1)
        interval_code = "1d"
        default_context = 90
        default_horizon = 14
        unit_label = "Days"
        max_horizon = 90
    
    st.markdown("---")
    
    horizon = st.slider(f"Horizon Length: {unit_label} to predict", 1, max_horizon, default_horizon)
    context = st.slider(f"Context Length: Memory Span ({unit_label})", 32, 1024, default_context, step=16)
    
    # --- VISUALS SECTION ---
    st.markdown("---")
    st.markdown(generate_colored_text("Visuals", font_size="1.2rem"), unsafe_allow_html=True)
    smart_scale = st.checkbox("🔍 Smart Y-Axis Scale", value=True, help="Automatically zoom the Y-axis to fit the recent price action and forecast, ignoring distant history.")
    
    st.markdown("---")
    run = st.button("FIRE") 

# EXECUTION
if run:
    if not ticker:
        st.error("Ops! We need a ticker symbol first.")
    else:
        with st.spinner("Waking up the AI... Crunching numbers..."):
            
            is_hourly = (interval_code == "1h")
            tfm_freq_token = 1 if is_hourly else 2
            
            mapped_period = period
            if period == "1 week": mapped_period = "5d"
            if period == "2 weeks": mapped_period = "1mo"
            
            ts_data = forecaster.get_ticker_data(ticker, mapped_period, interval_code)
            
            if ts_data is None or ts_data.empty:
                st.error(f"❌ **Ticker '{ticker}' not found or no data available.** Please check the symbol (e.g., use 'BTC-USD' for crypto, 'GOOGL' for stocks).")
            
            else:
                if period == "2 weeks":
                    cutoff = ts_data.index[-1] - timedelta(weeks=2)
                    ts_data = ts_data[ts_data.index >= cutoff]

                if len(ts_data) > 30:
                    model = get_model(context, horizon)
                    res = forecaster.run_forecast_logic(ts_data, model, context, horizon, tfm_freq_token)
                    
                    last_p = float(ts_data.iloc[-1])
                    pred_p = float(res['forecast'][-1])
                    chg = ((pred_p - last_p) / last_p) * 100
                    color_css = COLORS['green'] if chg >= 0 else COLORS['red']
                    
                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-around; align-items:center; margin-bottom:20px; padding:20px; border:1px solid #dadce0; border-radius:16px; background-color:{COLORS['bg_accent']}; box-shadow:0 2px 6px rgba(60,64,67,0.1);">
                        <div style="text-align:center;">
                            <span style="font-size:1rem; color:#5f6368; font-family:Roboto;">CURRENT PRICE</span><br>
                            <span style="font-size:2.2rem; font-weight:bold; font-family:Google Sans;">${last_p:.2f}</span>
                        </div>
                        <div style="text-align:center;">
                            <span style="font-size:1rem; color:#5f6368; font-family:Roboto;">PREDICTED MOVE</span><br>
                            <span style="font-size:3rem; font-weight:bold; font-family:Google Sans; color:{color_css};">{chg:+.2f}%</span>
                        </div>
                        <div style="text-align:center;">
                            <span style="font-size:1rem; color:#5f6368; font-family:Roboto;">TARGET PRICE</span><br>
                            <span style="font-size:2.2rem; font-weight:bold; font-family:Google Sans;">${pred_p:.2f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    chart_title = generate_colored_text(f"Interactive Analysis: {ticker.upper()}", font_size="1.8rem")
                    st.markdown(f"<div style='text-align:center; margin-bottom:20px;'>{chart_title}</div>", unsafe_allow_html=True)
                    
                    st.caption("💡 **Tip:** If the chart looks squeezed, click the **'Autoscale'** or **'Reset Axes'** button in the chart toolbar above.")
                    
                    fig = forecaster.create_trading_chart(ts_data, res, ticker, horizon, interval_code, COLORS, auto_scale_y=smart_scale)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error(f"⚠️ **Not enough historical data for '{ticker}'.** TimesFM needs at least 35 candles to establish a trend context (approx 5 trading days for hourly data).")

st.markdown('<div class="spacer-div"></div>', unsafe_allow_html=True)

f1, f2 = st.columns(2)
with f1:
    st.markdown(f"""
        <div class="google-card" style="display:flex; align-items:center; gap:20px;">
            <div style="font-size:40px;">📄</div>
            <div>
                <div style="margin-bottom:5px;">{generate_colored_text("TimesFM: The Theory", font_size="1.5rem")}</div>
                <div class="card-body">
                    Foundation models for time series? It's a real thing. 
                    <a href="https://research.google/blog/time-series-foundation-models-can-be-few-shot-learners/" target="_blank" style="color:{COLORS['blue']}; font-weight:bold; text-decoration:none; margin-left:5px;">Check the blog ↗</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown(f"""
        <div class="google-card" style="display:flex; align-items:center; gap:20px;">
            <div style="font-size:40px;">🔧</div>
            <div>
                <div style="margin-bottom:5px;">{generate_colored_text("Pop the Hood", font_size="1.5rem")}</div>
                <div class="card-body">
                    Developers, start your engines. The code is open.
                    <a href="https://github.com/google-research/timesfm" target="_blank" style="color:{COLORS['blue']}; font-weight:bold; text-decoration:none; margin-left:5px;">Visit GitHub ↗</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
