import pandas as pd
import numpy as np
import math

# -----------------------------
# PARAMETERS
# -----------------------------

LAT = 13.18                  # El Obeid latitude
PV_CAPACITY_KW = 40          # Rated PV capacity
PERFORMANCE_RATIO = 0.75     # System derating factor
YEAR = 2023

# -----------------------------
# LOAD DAILY SOLAR DATA
# -----------------------------

df_daily = pd.read_csv("solar_daily_2023.csv")
df_daily["date"] = pd.to_datetime(df_daily["date"])
df_daily["day_of_year"] = df_daily["date"].dt.dayofyear

# Create empty hourly dataframe
df_hourly = pd.DataFrame(
    pd.date_range(start=f"{YEAR}-01-01 00:00",
                  end=f"{YEAR}-12-31 23:00",
                  freq="h"),
    columns=["datetime"]
)

df_hourly["day_of_year"] = df_hourly["datetime"].dt.dayofyear
df_hourly["hour"] = df_hourly["datetime"].dt.hour

# -----------------------------
# SOLAR POSITION CALCULATION
# -----------------------------

def solar_declination(day):
    return 23.45 * math.sin(math.radians(360 * (284 + day) / 365))

def daylight_hours(day, lat):
    delta = math.radians(solar_declination(day))
    phi = math.radians(lat)
    omega = math.acos(-math.tan(phi) * math.tan(delta))
    return (2 * omega * 24) / (2 * math.pi)

# -----------------------------
# BUILD HOURLY PV OUTPUT
# -----------------------------

pv_output = []

for idx, row in df_hourly.iterrows():
    day = row["day_of_year"]
    hour = row["hour"]

    daily_ghi = df_daily.loc[df_daily["day_of_year"] == day,
                             "ghi_kwh_m2_day"].values[0]

    daylight = daylight_hours(day, LAT)
    sunrise = 12 - daylight / 2
    sunset = 12 + daylight / 2

    if sunrise <= hour <= sunset:
        x = (hour - sunrise) / (sunset - sunrise)
        shape = math.sin(math.pi * x)
        pv_kw = PV_CAPACITY_KW * shape * PERFORMANCE_RATIO
    else:
        pv_kw = 0

    pv_output.append(pv_kw)

df_hourly["pv_kw_raw"] = pv_output

# -----------------------------
# NORMALIZE TO MATCH DAILY GHI
# -----------------------------

df_hourly["date"] = df_hourly["datetime"].dt.date

scaled_output = []

for day, group in df_hourly.groupby("date"):
    doy = group["day_of_year"].iloc[0]
    daily_ghi = df_daily.loc[df_daily["day_of_year"] == doy,
                             "ghi_kwh_m2_day"].values[0]

    total_shape = group["pv_kw_raw"].sum()

    # Expected daily PV generation (kWh)
    expected_daily_kwh = daily_ghi * PV_CAPACITY_KW * PERFORMANCE_RATIO

    if total_shape > 0:
        scale_factor = expected_daily_kwh / total_shape
    else:
        scale_factor = 0

    scaled = group["pv_kw_raw"] * scale_factor
    scaled_output.extend(scaled)

df_hourly["pv_kw"] = scaled_output

print(df_hourly.head())
print("\nTotal annual PV generation (kWh):",
      round(df_hourly["pv_kw"].sum(), 2))

df_hourly.to_csv("solar_hourly_2023.csv", index=False)

print("\n✅ Hourly PV file saved as solar_hourly_2023.csv")