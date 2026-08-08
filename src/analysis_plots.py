import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PARAMETERS
# -----------------------------

BASE_PV_CAPACITY = 40
BATTERY_CAPACITY = 150
SOC_MIN_FRACTION = 0.2
EFFICIENCY = 0.95

HOUSEHOLDS = 100
COOKING_POWER_KW = 1.3

adoption_rates = [0.0, 0.2, 0.4]

results = []

# -----------------------------
# LOAD BASE DATA
# -----------------------------

df_pv = pd.read_csv("data/solar_hourly_2023.csv")
df_pv["datetime"] = pd.to_datetime(df_pv["datetime"])

df_base_load = pd.read_csv("data/load_hourly_baseline.csv")
df_base_load["datetime"] = pd.to_datetime(df_base_load["datetime"])

df = pd.merge(df_pv[["datetime", "pv_kw"]],
              df_base_load[["datetime", "load_kw"]],
              on="datetime")

# -----------------------------
# RUN SIMULATIONS
# -----------------------------

for rate in adoption_rates:

    df["total_load_kw"] = df["load_kw"]

    cooking_households = int(HOUSEHOLDS * rate)
    group_size = cooking_households // 3

    def cooking_load(hour):
        if hour in [18, 19]:
            return COOKING_POWER_KW * group_size
        elif hour in [20, 21]:
            return COOKING_POWER_KW * group_size
        elif hour in [22, 23]:
            return COOKING_POWER_KW * group_size
        else:
            return 0

    df["hour"] = df["datetime"].dt.hour
    df["cooking_kw"] = df["hour"].apply(cooking_load)
    df["total_load_kw"] += df["cooking_kw"]

    soc = BATTERY_CAPACITY
    soc_min = BATTERY_CAPACITY * SOC_MIN_FRACTION

    total_unmet = 0

    for i in range(len(df)):

        pv = df.loc[i, "pv_kw"]
        load = df.loc[i, "total_load_kw"]

        net = pv - load

        if net >= 0:
            charge = net * EFFICIENCY
            soc = min(soc + charge, BATTERY_CAPACITY)
        else:
            needed = -net
            available = (soc - soc_min)
            discharge = min(needed / EFFICIENCY, available)
            soc -= discharge
            unmet = needed - discharge * EFFICIENCY
            total_unmet += max(unmet, 0)

    results.append(total_unmet)

# -----------------------------
# PLOT 1: UNMET ENERGY
# -----------------------------

plt.figure(figsize=(8,5))

x_vals = [r*100 for r in adoption_rates]
y_vals = results

plt.plot(x_vals, y_vals, marker='o', linewidth=2)

for x, y in zip(x_vals, y_vals):
    plt.text(x, y + 500, f"{int(y)}", ha='center')

plt.xlabel("Electric Cooking Adoption (%)", fontsize=12)
plt.ylabel("Annual Unmet Energy (kWh)", fontsize=12)
plt.title("Infrastructure Stress from Cooking Electrification", fontsize=13)

plt.xticks([0, 20, 40])
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("figure_unmet_vs_adoption.png", dpi=300)
plt.show()



# -----------------------------
# PLOT 2: PEAK LOAD ESCALATION
# -----------------------------

peak_results = []

for rate in adoption_rates:

    df["total_load_kw"] = df["load_kw"]

    cooking_households = int(HOUSEHOLDS * rate)
    group_size = cooking_households // 3

    def cooking_load(hour):
        if hour in [18, 19]:
            return COOKING_POWER_KW * group_size
        elif hour in [20, 21]:
            return COOKING_POWER_KW * group_size
        elif hour in [22, 23]:
            return COOKING_POWER_KW * group_size
        else:
            return 0

    df["hour"] = df["datetime"].dt.hour
    df["cooking_kw"] = df["hour"].apply(cooking_load)
    df["total_load_kw"] += df["cooking_kw"]

    peak_results.append(df["total_load_kw"].max())

plt.figure(figsize=(8,5))

plt.plot(x_vals, peak_results, marker='o', linewidth=2, color='darkred')

for x, y in zip(x_vals, peak_results):
    plt.text(x, y + 2, f"{round(y,1)} kW", ha='center')

plt.xlabel("Electric Cooking Adoption (%)", fontsize=12)
plt.ylabel("Peak System Load (kW)", fontsize=12)
plt.title("Peak Demand Escalation from Cooking Electrification", fontsize=13)

plt.xticks([0, 20, 40])
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("figure_peak_load_vs_adoption.png", dpi=300)
plt.show()


# -----------------------------
# SOC STRESS SNAPSHOT (40% ADOPTION)
# -----------------------------

rate = 0.4

df["total_load_kw"] = df["load_kw"]

cooking_households = int(HOUSEHOLDS * rate)
group_size = cooking_households // 3

def cooking_load(hour):
    if hour in [18, 19]:
        return COOKING_POWER_KW * group_size
    elif hour in [20, 21]:
        return COOKING_POWER_KW * group_size
    elif hour in [22, 23]:
        return COOKING_POWER_KW * group_size
    else:
        return 0

df["hour"] = df["datetime"].dt.hour
df["cooking_kw"] = df["hour"].apply(cooking_load)
df["total_load_kw"] += df["cooking_kw"]

soc = BATTERY_CAPACITY
soc_min = BATTERY_CAPACITY * SOC_MIN_FRACTION

soc_list = []

for i in range(len(df)):
    pv = df.loc[i, "pv_kw"]
    load = df.loc[i, "total_load_kw"]

    net = pv - load

    if net >= 0:
        charge = net * EFFICIENCY
        soc = min(soc + charge, BATTERY_CAPACITY)
    else:
        needed = -net
        available = (soc - soc_min)
        discharge = min(needed / EFFICIENCY, available)
        soc -= discharge

    soc_list.append(soc)

df["soc_kwh"] = soc_list

# Take one representative week (mid-year)
week_df = df.iloc[3000:3168]   # ~1 week slice

plt.figure(figsize=(10,5))
plt.plot(week_df["datetime"], week_df["soc_kwh"], label="Battery SOC (kWh)")
plt.axhline(y=soc_min, color='r', linestyle='--', label="SOC Minimum")
plt.title("Battery Stress During High Adoption (40%)")
plt.ylabel("State of Charge (kWh)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("figure_soc_stress.png", dpi=300)
plt.show()

