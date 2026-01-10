# Googlantir 🔮

> *"What if Google stole a Palantír?"*

A time-series forecasting tool that lets you peek into market futures using Google's TimesFM foundation model.

---

## 📊 What This Does

Googlantir takes historical price data and projects it forward using **TimesFM**, Google Research's transformer-based forecasting model. Think of it as autocomplete for stock charts—trained on enough time series to predict yours without seeing it before.

### Analysis Modes

| Mode | Resolution | Best For | Typical Use Case |
|------|-----------|----------|------------------|
| **Standard** | Daily candles | Swing trading | Position analysis, weekly outlook |
| **Deep Dive** | Hourly candles | Day trading | Intraday patterns, short-term moves |
| **Macro** | Weekly candles | Long-term investing | Quarterly trends, strategic positioning |

Each forecast comes with **confidence bands** (10-90%, 30-70%) so you know when the model is confident vs. when it's guessing.

---

## ✨ Why This Exists

This model is:
- ✅ **Free** – No subscription, no API costs
- ✅ **Transparent** – Open source, understandable parameters
- ✅ **Educational** – Built-in guides explain context length vs. horizon tradeoffs
- ✅ **Clean** – Google-inspired interface, no cruft

---

## 🚀 Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd googlantir

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

> **Note:** First run downloads the 200M parameter model (~1 minute). Subsequent runs are fast.

---

## 🎯 How to Use

### Quick Start
1. **Enter a ticker** (e.g., `GOOGL`, `BTC-USD`, `SPY`)
2. **Select analysis mode** (Standard/Deep Dive/Macro)
3. **Configure parameters:**
   - **Context Length** – How much history to consider
   - **Horizon Length** – How far ahead to predict
4. **Hit FIRE** 🔥

### Output
- 📈 Current price vs. predicted price
- 📊 Confidence intervals (10-90%, 30-70%)
- 🖱️ Interactive Plotly chart with zoom controls

---

## ⚙️ Configuration Guide

### Recommended Settings

| Trading Style | Mode | Context | Horizon | Rationale |
|--------------|------|---------|---------|-----------|
| **Crypto Day Trading** | Deep Dive | ~168h | 6-24h | One week of hourly data captures intraday patterns |
| **Stock Swing Trading** | Standard | ~90d | 7-14d | One quarter captures earnings cycles |
| **Macro Positioning** | Macro | ~104w | 4-12w | Two years captures full business cycles |

### Golden Rule
> **Context should be 3-4x longer than Horizon**  
> Shorter ratios force the model to extrapolate beyond reliable patterns.

---

## 🛠️ Tech Stack

| Component | Purpose | Details |
|-----------|---------|---------|
| **TimesFM** | Forecasting engine | Google's foundation model, pre-trained on 100B data points |
| **Streamlit** | Web interface | Clean UI, zero JavaScript required |
| **yfinance** | Data source | Free access to Yahoo Finance (stocks, crypto, ETFs, indices) |
| **Plotly** | Visualization | Interactive charts, mobile-responsive |
| **PyTorch** | Model runtime | CPU by default, GPU-accelerated if CUDA available |

---

## ⚠️ Disclaimer

### What This Is
- 📚 An **educational tool** for exploring time-series forecasting
- 🔬 A **research interface** for understanding TimesFM behavior
- 🎓 A **learning resource** for model configuration

### What This Is NOT
- ❌ Financial advice
- ❌ A trading signal generator
- ❌ A guarantee of future performance

> **Markets are noisy. Models are approximations. Past performance ≠ future results.**

---

## 🐛 Known Issues

| Issue | Description | Workaround |
|-------|-------------|------------|
| Insufficient data | Illiquid tickers lack historical depth | Choose longer period or different ticker |
| Weekend gaps | Hourly mode skips non-trading hours | By design (realistic market simulation) |
| First forecast slow | Model recompiles on parameter changes | Subsequent forecasts are fast |

For detailed troubleshooting, see [`usage.txt`](usage.txt).

---

## 📚 Resources

- [TimesFM Research Paper](https://research.google/blog/time-series-foundation-models-can-be-few-shot-learners/)
- [TimesFM GitHub](https://github.com/google-research/timesfm)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

## 🙏 Credits

| Contribution | Source |
|--------------|--------|
| Model Architecture | [Google Research TimesFM](https://github.com/google-research/timesfm) |
| UI Design | Inspired by Google's Material Design |
| Naming | Tolkien + a questionable sense of humor |

---

## 📄 License

MIT License – Do whatever you want with this. If you make money, great. If you lose money, not my problem.

---

<div align="center">

**Built because I wanted to understand TimesFM and couldn't find a decent UI for it.**

⭐ Star this repo if you find it useful | 🐛 Report issues | 🤝 Contributions welcome

</div>
