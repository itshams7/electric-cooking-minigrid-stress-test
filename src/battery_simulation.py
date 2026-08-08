import pandas as pd
import numpy as np

# -----------------------------
# PARAMETERS
# -----------------------------

BASELINE_UNMET_TARGET = 16.23   # baseline case unmet energy
SOC_MIN_FRACTION = 0.2
EFFICIENCY = 0.95

# -----------------------------
# LOAD DATA
# -----------------------------

df_pv = pd.read_csv("data/solar_hourly_2023.csv")
df_load = pd.read_csv("data/load_with_cooking.csv")

df_pv["datetime"] = pd.to_datetime(df_pv["datetime"])
df_load["datetime"] = pd.to_datetime(df_load["datetime"])

df = pd.merge(df_pv[["datetime", "pv_kw"]],
              df_load[["datetime", "total_load_kw"]],
              on="datetime")
              
BASE_PV_CAPACITY = 40

# -----------------------------
# BATTERY SIMULATION
# -----------------------------

def run_simulation(battery_capacity):

    soc = battery_capacity
    soc_min = battery_capacity * SOC_MIN_FRACTION

    total_unmet = 0

    for i in range(len(df)):

        pv = df.loc[i, "pv_kw"]
        load = df.loc[i, "total_load_kw"]

        net = pv - load

        if net >= 0:
            charge = net * EFFICIENCY
            soc = min(soc + charge, battery_capacity)

        else:
            needed = -net
            available = (soc - soc_min)

            discharge = min(needed / EFFICIENCY, available)
            soc -= discharge
            unmet = needed - discharge * EFFICIENCY
            total_unmet += max(unmet, 0)

    return total_unmet

# -----------------------------
# ENERGY BALANCE DIAGNOSTIC
# -----------------------------

annual_pv = df["pv_kw"].sum()
annual_load = df["total_load_kw"].sum()

print("Annual PV generation (kWh):", round(annual_pv, 2))
print("Annual load (kWh):", round(annual_load, 2))
print("Energy deficit (kWh):", round(annual_load - annual_pv, 2))
print()


# -----------------------------
# COMBINED PV + BATTERY SCALING
# -----------------------------

print("\n--- Combined PV + Battery Scaling Test ---")

pv_range = range(40, 61, 2)          # 40 to 60 kW in steps of 2
battery_range = range(150, 251, 10)  # 150 to 250 kWh in steps of 10

solution_found = False

for pv_capacity in pv_range:

    for battery_capacity in battery_range:

        # Scale PV
        pv_scaled = df["pv_kw"] * (pv_capacity / BASE_PV_CAPACITY)

        soc = battery_capacity
        soc_min = battery_capacity * SOC_MIN_FRACTION

        total_unmet = 0

        for i in range(len(df)):

            pv = pv_scaled.iloc[i]
            load = df.loc[i, "total_load_kw"]

            net = pv - load

            if net >= 0:
                charge = net * EFFICIENCY
                soc = min(soc + charge, battery_capacity)

            else:
                needed = -net
                available = (soc - soc_min)

                discharge = min(needed / EFFICIENCY, available)
                soc -= discharge
                unmet = needed - discharge * EFFICIENCY
                total_unmet += max(unmet, 0)

        if total_unmet <= BASELINE_UNMET_TARGET:
            print("\n✅ Reliability restored with:")
            print("PV capacity (kW):", pv_capacity)
            print("Battery capacity (kWh):", battery_capacity)
            print("Final unmet energy (kWh):", round(total_unmet, 2))
            solution_found = True
            break

    if solution_found:
        break

if not solution_found:
    print("\n❌ No combination in tested range restored baseline reliability.")