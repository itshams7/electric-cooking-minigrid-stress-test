import pandas as pd
import numpy as np

# -----------------------------
# PARAMETERS
# -----------------------------

HOUSEHOLDS = 100
DAILY_KWH_PER_HH = 1.0   # baseline assumption
YEAR = 2023

# -----------------------------
# CREATE HOURLY TIME INDEX
# -----------------------------

df = pd.DataFrame(
    pd.date_range(start=f"{YEAR}-01-01 00:00",
                  end=f"{YEAR}-12-31 23:00",
                  freq="h"),
    columns=["datetime"]
)

df["hour"] = df["datetime"].dt.hour

# -----------------------------
# DEFINE BASELINE LOAD SHAPE
# -----------------------------

def baseline_shape(hour):
    # Simple rural pattern
    if 6 <= hour < 8:
        return 0.08   # morning bump
    elif 18 <= hour < 22:
        return 0.12   # evening peak
    else:
        return 0.03   # low background

df["shape"] = df["hour"].apply(baseline_shape)

# Normalize so daily total per household = DAILY_KWH_PER_HH
daily_sum = df.groupby(df["datetime"].dt.date)["shape"].sum().iloc[0]
df["shape_normalized"] = df["shape"] * (DAILY_KWH_PER_HH / daily_sum)

# Multiply by number of households
df["load_kw"] = df["shape_normalized"] * HOUSEHOLDS

print(df.head())
print("\nTotal annual baseline load (kWh):",
      round(df["load_kw"].sum(), 2))

df.to_csv("load_hourly_baseline.csv", index=False)

print("\n✅ Baseline load file saved as load_hourly_baseline.csv")