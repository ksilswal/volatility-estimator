import os
import matplotlib.pyplot as plt
from fetch_data import get_ohlc
from VolatilityEstimator import (
    close_to_close_vol,
    ewma_vol,
    parkinson_vol,
    garman_klass_vol,
    yang_zhang_vol
)

# -----------------------------
# Paths (robust)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# Fetch data
df = get_ohlc("SPY", start="2019-01-01")
df = df[["Open", "High", "Low", "Close"]].apply(lambda x: x.squeeze())

close = df["Close"].squeeze()   # IMPORTANT

hv20 = close_to_close_vol(close, window=20)
print(hv20.tail())

# Compute volatilities
ewma = ewma_vol(close, lam=0.94)
parkinson = parkinson_vol(df, window=20)
gk = garman_klass_vol(df, window=20)
yz = yang_zhang_vol(df, window=20)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(hv20, label="Close-to-Close (20d)")
plt.plot(ewma, label="EWMA (λ=0.94)")
plt.plot(parkinson, label="Parkinson")
plt.plot(gk, label="Garman–Klass")
plt.plot(yz, label="Yang–Zhang")

plt.title("Volatility Estimators on SPY (Annualized)")
plt.ylabel("Volatility")
plt.xlabel("Date")
plt.legend()
plt.grid(alpha=0.3)

# -----------------------------
# Save plot
# -----------------------------
output_path = os.path.join(PLOTS_DIR, "volatility_comparison_SPY.png")
plt.tight_layout()
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Plot saved to: {output_path}")
