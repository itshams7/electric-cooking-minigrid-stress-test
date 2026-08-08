import requests
import pandas as pd

# Location: El Obeid, Sudan
LAT, LON = 13.18, 30.22
YEAR = 2023

url = "https://power.larc.nasa.gov/api/temporal/daily/point"
params = {
    "parameters": "ALLSKY_SFC_SW_DWN",
    "community": "RE",
    "longitude": LON,
    "latitude": LAT,
    "start": f"{YEAR}0101",
    "end": f"{YEAR}1231",
    "format": "JSON",
}

print("Requesting NASA POWER data...")

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]

df = pd.DataFrame({
    "date": pd.to_datetime(list(data.keys()), format="%Y%m%d"),
    "ghi_kwh_m2_day": list(data.values())
})

df.to_csv("solar_daily_2023.csv", index=False)

print("\nFirst 5 rows:")
print(df.head())

print("\nStatistics:")
print(df.describe())

print("\n✅ File saved as solar_daily_2023.csv")