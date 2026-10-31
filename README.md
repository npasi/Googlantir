# Googlantir


Googlantir is a small Streamlit app for experimenting with Google's TimesFM forecasting model on market data. Give it a ticker, choose how much history to use, and plot a forecast alongside the observed prices.

I built it because I wanted to understand TimesFM and have a straightforward interface for trying it out. The aim is to make the model easier to explore, not to turn its output into a trading strategy.

## How it works

The app retrieves historical prices through `yfinance` and passes them to TimesFM. The model generates a forecast without being trained specifically on the ticker you select. You can change the context and forecast lengths to see how the output responds.

There are three modes, each using a different sampling interval:

| Mode | Price interval | Scope |
| --- | --- | --- |
| Standard | Daily | Day-to-day price movements |
| Deep Dive | Hourly | Shorter-term patterns |
| Macro | Weekly | Longer-term trends |

Forecasts include shaded bands between the 10th and 90th percentiles and the 30th and 70th percentiles. These show the range of the model's predictions. They are not guarantees that future prices will fall inside those ranges, and narrower bands do not necessarily mean a forecast is more accurate.

## Running locally

Clone the repository and open its directory:

```bash
git clone <your-repo-url>
cd googlantir
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows, use `venv\Scripts\activate` instead.

Install the dependencies and start the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The first run downloads the model weights, so it can take longer than subsequent runs. Download and inference times depend on your connection and hardware.

## Using the app

Enter a ticker such as `GOOGL`, `BTC-USD`, or `SPY`, then select a mode. Set the context length and forecast horizon, and click **FIRE** to run the forecast.

The context length controls how many historical observations the model receives. The horizon controls how many observations it predicts. Both use the interval of the selected mode: a horizon of 12 means 12 hourly observations in Deep Dive and 12 weekly observations in Macro.

The results appear in an interactive Plotly chart with the historical prices, forecast, and prediction bands. You can zoom in to inspect a particular section.

## Choosing parameters

There is no single context-to-horizon ratio that works for every series. More history is not always more useful, and a longer forecast does not become reliable simply because you provide a longer context.

For an initial experiment, try a short horizon and vary the context while keeping the other settings fixed. If you want to assess accuracy, test forecasts against held-out historical data rather than judging whether the chart looks plausible. Compare against a simple baseline, such as carrying the last observed price forward.

Weekly sampling can make longer-term movements easier to inspect, but it does not make them easier to predict. Similarly, hourly data gives more detail without necessarily providing more useful signal.

## Dependencies

The app uses TimesFM for forecasting, Streamlit for the interface, `yfinance` for historical prices, Plotly for charts, and PyTorch to run the model. The interface takes inspiration from Google's visual design.

## Limitations

Market prices are noisy, and a general-purpose forecasting model can produce convincing-looking curves without offering useful predictive accuracy. The app is intended for learning and experimentation, not financial advice or validated trading signals.

Data availability also varies by ticker and interval. Some tickers may not have enough history for the requested context. Hourly stock data contains gaps outside trading hours; consecutive observations are therefore not always consecutive clock hours. A market closure is not a missing price that the model can simply infer.

If data is insufficient, try a shorter context, another interval, or a different ticker. Loading the model and running the first forecast may take some time. See [usage.txt](usage.txt) for additional troubleshooting notes.

## Further reading

- [TimesFM research overview](https://research.google/blog/time-series-foundation-models-can-be-few-shot-learners/)
- [TimesFM repository](https://github.com/google-research/timesfm)
- [Streamlit documentation](https://docs.streamlit.io/)

TimesFM is developed by Google Research. The name borrows from Tolkien. Issues and contributions are welcome.
