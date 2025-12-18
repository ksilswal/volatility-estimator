#fetch_data.py
import yfinance as yf
import pandas as pd
from typing import Optional

def get_ohlc(
    ticker: str,
    start: str = "2018-01-01",
    end: Optional[str] = None
) -> pd.DataFrame:
    df = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False
    )

    # Keep only OHLC
    df = df[["Open", "High", "Low", "Close"]].dropna()
    return df

if __name__ == "__main__":
    df = get_ohlc("SPY")
    print(df.head())
