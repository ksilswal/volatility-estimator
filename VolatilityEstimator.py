import numpy as np
import pandas as pd

TRADING_DAYS = 252


def _to_series_1d(x):
    """
    Convert Series / DataFrame / ndarray to a 1D pandas Series.
    """
    if isinstance(x, pd.DataFrame):
        x = x.squeeze()
    elif isinstance(x, np.ndarray):
        x = x.squeeze()
    return pd.Series(x).dropna()

def log_returns(close):
    close = pd.Series(close.squeeze()).dropna()

    return np.log(close).diff().dropna()

def annualize_vol(daily_vol, periods_per_year=TRADING_DAYS):
    return daily_vol * np.sqrt(periods_per_year)

def close_to_close_vol(close, window=20, annualize=True):
    r = log_returns(close)
    vol = r.rolling(window).std(ddof=1)
    return annualize_vol(vol) if annualize else vol

def ewma_vol(close, lam=0.94, annualize=True):
    r = log_returns(close)
    var = np.zeros(len(r))
    var[0] = r.iloc[:min(30, len(r))].var(ddof=1) if len(r) > 1 else 0.0
    for i in range(1, len(r)):
        var[i] = lam * var[i-1] + (1 - lam) * (r.iloc[i] ** 2)
    vol = pd.Series(np.sqrt(var), index=r.index)
    return annualize_vol(vol) if annualize else vol

def parkinson_vol(df, window=20, annualize=True):
    h, l = df["High"], df["Low"]
    rs = (np.log(h / l) ** 2) / (4 * np.log(2))
    var = rs.rolling(window).mean()
    vol = np.sqrt(var)
    return annualize_vol(vol) if annualize else vol

def garman_klass_vol(df, window=20, annualize=True):
    o, h, l, c = df["Open"], df["High"], df["Low"], df["Close"]
    log_hl = np.log(h / l)
    log_co = np.log(c / o)
    var = 0.5 * (log_hl ** 2) - (2 * np.log(2) - 1) * (log_co ** 2)
    var = var.rolling(window).mean()
    vol = np.sqrt(var.clip(lower=0))
    return annualize_vol(vol) if annualize else vol

def yang_zhang_vol(df, window=20, annualize=True):
    o = _to_series_1d(df["Open"])
    h = _to_series_1d(df["High"])
    l = _to_series_1d(df["Low"])
    c = _to_series_1d(df["Close"])

    c_prev = c.shift(1)

    # Overnight and open-to-close returns
    r_overnight = np.log(o / c_prev)
    r_oc = np.log(c / o)

    # Rogers–Satchell volatility
    rs = (
        np.log(h / o) * np.log(h / c) +
        np.log(l / o) * np.log(l / c)
    )

    var_overnight = r_overnight.rolling(window).var(ddof=1)
    var_oc = r_oc.rolling(window).var(ddof=1)
    var_rs = rs.rolling(window).mean()

    k = 0.34 / (1.34 + (window + 1) / (window - 1))
    var_yz = var_overnight + k * var_oc + (1 - k) * var_rs

    vol = np.sqrt(var_yz.clip(lower=0))
    return annualize_vol(vol) if annualize else vol
