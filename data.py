import yfinance as yf
import pandas as pd

def get_ticker_data(ticker, period, interval):

    period_map = {
        "5 days": "5d",
        "1 month": "1mo",
        "3 months": "3mo",
        "6 months": "6mo",
        "1 year": "1y", 
        "2 years": "2y", 
        "5 years": "5y", 
        "10 years": "10y",
        "Max": "max"
    }
    yf_period = period_map.get(period, "1y")

    try:
  
        data = yf.download(ticker, period=yf_period, interval=interval, progress=False)
        
        if data.empty: 
            return None

       
        if isinstance(data.columns, pd.MultiIndex):
            try: 
                time_series = data["Close"][ticker]
            except KeyError: 
                time_series = data["Close"] if "Close" in data.columns else data.iloc[:, 0]
        else: 
            time_series = data["Close"] if "Close" in data.columns else data.iloc[:, 0]
            
        time_series = time_series.dropna()


        is_crypto = "-USD" in ticker or "-EUR" in ticker
        if not is_crypto:
            if time_series.index.tz is None:
                time_series.index = time_series.index.tz_localize('UTC').tz_convert('America/New_York')
            else:
                time_series.index = time_series.index.tz_convert('America/New_York')
        else:
            if time_series.index.tz is not None:
                time_series.index = time_series.index.tz_localize(None)

        return time_series
    
    except Exception as e: 
        print(f"Error in data fetching: {e}")
        return None