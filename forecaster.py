import torch
import timesfm
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from datetime import timedelta


import data

# --- 1. BRIDGE FUNCTION ---
def get_ticker_data(ticker, period, interval):
  
    return data.get_ticker_data(ticker, period, interval)

# --- 2. LOAD MODEL ---
def load_timesfm_model(context_len, forecasting_horizon):
    model = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
    model.compile(
        timesfm.ForecastConfig(
            max_context=context_len,
            max_horizon=forecasting_horizon + 1,
            normalize_inputs=False,
            use_continuous_quantile_head=True,
            force_flip_invariance=True,
            infer_is_positive=True,
            fix_quantile_crossing=True,
        )
    )
    return model

# --- 3. FORECAST LOGIC ---
def run_forecast_logic(time_series, model, context_len, forecasting_horizon, freq_token):
    if len(time_series) < context_len: 
        input_data = time_series.values
    else: 
        input_data = time_series.values[-context_len:]
    
    scaler = StandardScaler()
    normalized_input = scaler.fit_transform(input_data.reshape(-1, 1))
    inputs_list = [normalized_input.flatten().astype(np.float32)]
    
    point_forecast, quantile_forecast = model.forecast(
        horizon=forecasting_horizon, 
        inputs=inputs_list
    )
    
    forecast_vals = scaler.inverse_transform(point_forecast[0].reshape(-1, 1)).flatten()
    norm_quantiles = quantile_forecast[0]
    q_map = {'p10': 1, 'p30': 3, 'p70': 6, 'p90': 8}
    results = {'forecast': forecast_vals}
    for key, idx in q_map.items():
        results[key] = scaler.inverse_transform(norm_quantiles[:, idx].reshape(-1, 1)).flatten()
    return results

# --- 4. DATE GENERATOR ---
def generate_future_dates(start_date, num_periods, interval_code, is_crypto):
    dates = []
    current = start_date
    count = 0
    
    while count < num_periods:
        if interval_code == "1h":
            current += timedelta(hours=1)
            if not is_crypto:
                if current.weekday() >= 5: continue
                if current.hour < 9 or current.hour >= 16: continue
       
        elif interval_code == "1d":
            current += timedelta(days=1)
            if not is_crypto and current.weekday() >= 5: continue

        elif interval_code == "1wk":
            current += timedelta(weeks=1)
            
        dates.append(current)
        count += 1
    return pd.DatetimeIndex(dates)
# --- CHART CREATION ---
def create_trading_chart(time_series, forecast_data, ticker, forecasting_horizon, interval_code, colors_dict, auto_scale_y=False):
    last_date = time_series.index[-1]
    is_crypto = "-USD" in ticker or "-EUR" in ticker
    
    forecast_dates = generate_future_dates(last_date, forecasting_horizon, interval_code, is_crypto)

    if interval_code == "1h":
        x_fmt = '%d %b %H:00'
        zoom_lookback = timedelta(days=5) # Zoom su 5 giorni per orario
    elif interval_code == "1wk":
        x_fmt = '%d %b %Y'
        zoom_lookback = timedelta(weeks=52) # Zoom su 1 anno per macro
    else:
        x_fmt = '%d %b %Y'
        zoom_lookback = timedelta(days=90) # Zoom su 3 mesi per daily

    # Calcolo data inizio zoom
    start_zoom = time_series.index[-1] - zoom_lookback
    if start_zoom < time_series.index[0]:
        start_zoom = time_series.index[0]

    # --- LOGICA SMART SCALING Y ---
    y_range_override = None
    if auto_scale_y:
        # 1. Prendiamo solo la parte di storico che sarà visibile
        visible_history = time_series[time_series.index >= start_zoom]
        
        # 2. Uniamo i valori visibili (storico recente + previsione)
        # Usiamo p90 e p10 per assicurarci che anche le bande siano dentro
        all_visible_values = np.concatenate([
            visible_history.values.flatten(),
            forecast_data['p90'],
            forecast_data['p10']
        ])
        
        # 3. Troviamo min e max
        local_min = np.min(all_visible_values)
        local_max = np.max(all_visible_values)
        
        # 4. Aggiungiamo un cuscinetto (padding) del 5% sopra e sotto
        padding = (local_max - local_min) * 0.05
        y_range_override = [local_min - padding, local_max + padding]

    fig = go.Figure()

    # Bande di confidenza
    fig.add_trace(go.Scatter(x=forecast_dates, y=forecast_data['p90'], mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=forecast_dates, y=forecast_data['p10'], mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(52, 168, 83, 0.1)', name='Very Likely (10-90%)', hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=forecast_dates, y=forecast_data['p70'], mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=forecast_dates, y=forecast_data['p30'], mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(52, 168, 83, 0.25)', name='Probable Scenario (30-70%)', hoverinfo='skip'))

    # Dati storici
    fig.add_trace(go.Scatter(
        x=time_series.index, y=time_series.values.flatten(), mode='lines', name='Historical Data',
        line=dict(color=colors_dict['blue'], width=2.5),
        connectgaps=True, 
        hovertemplate=f'%{{x|{x_fmt}}}<br>Price: $%{{y:.2f}}<extra></extra>'
    ))

    # Previsione AI
    mode_forecast = 'lines+markers' if forecasting_horizon < 20 else 'lines'
    fig.add_trace(go.Scatter(
        x=forecast_dates, y=forecast_data['forecast'], mode=mode_forecast, name='AI Forecast',
        line=dict(color=colors_dict['green'], width=2.5, dash='dash'),
        marker=dict(size=5),
        hovertemplate=f'%{{x|{x_fmt}}}<br>Pred: $%{{y:.2f}}<extra></extra>'
    ))
    
    # Connettore
    fig.add_trace(go.Scatter(
        x=[time_series.index[-1], forecast_dates[0]],
        y=[time_series.values.flatten()[-1], forecast_data['forecast'][0]],
        mode='lines', line=dict(color=colors_dict['green'], width=2.5, dash='dot'), showlegend=False, hoverinfo='skip'
    ))

    # Rangebreaks
    rangebreaks = []
    if not is_crypto:
        if interval_code != "1wk": 
            rangebreaks.append(dict(bounds=["sat", "mon"])) 
        if interval_code == "1h":
            rangebreaks.append(dict(bounds=[16, 9.5], pattern="hour"))

    fig.update_layout(
        template='plotly_white',
        paper_bgcolor='rgba(255,255,255,0.8)', plot_bgcolor='rgba(255,255,255,0.8)', 
        height=700, hovermode='x unified', font=dict(color=colors_dict['text_main']),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="top", y=0.99, xanchor="right", x=0.99, font=dict(color=colors_dict['text_main']), bgcolor='rgba(255,255,255,0.9)', bordercolor=colors_dict['border'], borderwidth=1),
        xaxis=dict(
            type="date", showgrid=True, gridcolor='#f1f3f4',
            rangeslider=dict(visible=False),
            tickfont=dict(color='#202124'), title_font=dict(color='#202124'),
            rangebreaks=rangebreaks,
            range=[start_zoom, forecast_dates[-1]] # Range X forzato qui
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#f1f3f4', 
            zerolinecolor=colors_dict['border'], 
            tickfont=dict(color='#202124'), 
            title_font=dict(color='#202124'),
            range=y_range_override, # Range Y dinamico applicato qui se presente
            fixedrange=False # Permette all'utente di modificare lo zoom trascinando
        )
    )
    
    return fig
