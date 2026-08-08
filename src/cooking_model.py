import pandas as pd
import numpy as np

# -----------------------------
# PARAMETERS
# -----------------------------

HOUSEHOLDS = 100
COOKING_POWER_KW = 1.3
COOKING_HOURS = 1.5
YEAR = 2023

ADOPTION_RATE = 0.4   # change to 0.4 later for scenario

# -----------------------------
# LOAD BASELINE DATA
# -----------------------------

df = pd.read_csv("load_hourly_baseline.csv")
df["datetime"] = pd.to_datetime(df["datetime"])
df["hour"] = df["datetime"].dt.hour

# -----------------------------
# CALCULATE NUMBER OF COOKING HOUSEHOLDS
# -----------------------------

cooking_households = int(HOUSEHOLDS * ADOPTION_RATE)

# Split into 3 groups
group_size = cooking_households // 3

# -----------------------------
# DEFINE COOKING LOAD FUNCTION
# -----------------------------

def cooking_load(hour):
    if hour in [18, 19]:
        return COOKING_POWER_KW * group_size
    elif hour in [20, 21]:
        return COOKING_POWER_KW * group_size
    elif hour in [22, 23]:
        return COOKING_POWER_KW * group_size
    else:
        return 0

df["cooking_kw"] = df["hour"].apply(cooking_load)

# Total load
df["total_load_kw"] = df["load_kw"] + df["cooking_kw"]

print(df.head())

print("\nAnnual cooking energy (kWh):",
      round(df["cooking_kw"].sum(), 2))

print("\nTotal annual load (kWh):",
      round(df["total_load_kw"].sum(), 2))

df.to_csv("load_with_cooking.csv", index=False)

print("\n✅ Cooking scenario file saved as load_with_cooking.csv")