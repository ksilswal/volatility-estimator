# Volatility Estimation on Real Market Data

## Overview
This project implements and compares several commonly used volatility estimators
using real OHLC (Open, High, Low, Close) market data. Volatility is a fundamental
concept in quantitative finance, serving as a proxy for uncertainty and risk.
Because true volatility is unobservable, it must be estimated from historical
price data. Different estimators use different information sets and assumptions,
leading to distinct behavior in practice.

The goal of this project is to study how these estimators behave empirically,
highlight their trade-offs, and understand when each is most appropriate.

---

## What Is Volatility?

### Intuition
Volatility measures the magnitude of price fluctuations over time. High
volatility corresponds to large and frequent price changes, while low volatility
indicates more stable prices. In trading and risk management, volatility is
closely associated with uncertainty and potential risk.

### Formal Definition
Let ![](https://latex.codecogs.com/svg.image?P_t) denote the asset price at time \( t \). The log return is defined as

![log-return](https://latex.codecogs.com/svg.image?r_t=\log\left(\frac{P_t}{P_{t-1}}\right))

Volatility is defined as the standard deviation of returns:

![vol-def](https://latex.codecogs.com/svg.image?\sigma=\sqrt{\mathrm{Var}(r_t)})

Because the true return distribution is unknown, volatility must be estimated
from observed data.

---

## Why Multiple Volatility Estimators?

Volatility is not directly observable, and market data is discrete, noisy, and
incomplete. Different estimators:
- use different subsets of available price information,
- make different assumptions about price dynamics,
- respond differently to regime changes and shocks.

As a result, there is no single “correct” volatility—only estimates that are
useful for specific purposes.

---

## Implemented Volatility Estimators

### 1. Close-to-Close (Historical) Volatility
This estimator uses only closing prices and computes the standard deviation of
log returns over a rolling window.

**Pros**
- Simple and widely understood  
- Serves as a baseline estimator  

**Cons**
- Ignores intraday price movements  
- Can be noisy and slow to react to volatility spikes  

**Interpretation:**  
“How much do closing prices vary from day to day?”

---

### 2. EWMA Volatility (RiskMetrics)
Exponentially Weighted Moving Average (EWMA) volatility assigns greater weight
to recent returns:

![ewma](https://latex.codecogs.com/svg.image?\sigma_t^2=\lambda\sigma_{t-1}^2+(1-\lambda)r_t^2)

**Pros**
- Responds quickly to market shocks  
- Widely used in risk management systems  

**Cons**
- Still relies only on closing prices  
- Sensitive to the choice of decay parameter \( \lambda \)  

**Interpretation:**  
“How volatile is the market right now, with emphasis on recent movements?”

---

### 3. Parkinson Volatility
The Parkinson estimator uses the daily high–low price range:

![parkinson](https://latex.codecogs.com/svg.image?\sigma^2=\frac{1}{4\ln(2)}\left(\log\frac{H}{L}\right)^2)

**Pros**
- More efficient than close-to-close volatility  
- Uses intraday information  

**Cons**
- Assumes no drift  
- Ignores opening gaps  

**Interpretation:**  
“How wide was the trading range during the day?”

---

### 4. Garman–Klass Volatility
This estimator uses Open, High, Low, and Close prices to improve efficiency:

![gk](https://latex.codecogs.com/svg.image?\sigma^2=\frac{1}{2}\left(\log\frac{H}{L}\right)^2-(2\ln2-1)\left(\log\frac{C}{O}\right)^2)

**Pros**
- More efficient than Parkinson  
- Incorporates directional movement  

**Cons**
- Assumes continuous trading  
- Sensitive to overnight price jumps  

**Interpretation:**  
“How volatile was intraday trading, accounting for direction?”

---

### 5. Yang–Zhang Volatility
The Yang–Zhang estimator separates volatility into:
- overnight volatility,
- open-to-close volatility,
- intraday volatility (Rogers–Satchell).

![yz](https://latex.codecogs.com/svg.image?\sigma_{YZ}^2=\sigma_{overnight}^2+k\sigma_{open-close}^2+(1-k)\sigma_{RS}^2)


This makes it robust to opening gaps and discontinuous trading.

**Pros**
- Handles overnight jumps explicitly  
- One of the most robust practical estimators  

**Cons**
- More complex  
- Requires full OHLC data  

**Interpretation:**  
“How volatile was the market, accounting for both intraday trading and overnight information?”

---

## Data
Historical OHLC data is retrieved using the `yfinance` library. Estimators are
evaluated on liquid assets (e.g., SPY), allowing comparison across different
market regimes and volatility environments.

---

## Results
The estimators exhibit systematic differences:
- EWMA responds fastest to volatility shocks  
- Range-based estimators (Parkinson, Garman–Klass) are smoother and more efficient  
- Yang–Zhang handles overnight gaps more robustly  

These differences highlight how estimator choice depends on the intended
application.

---
