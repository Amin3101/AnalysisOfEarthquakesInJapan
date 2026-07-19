import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from pathlib import Path

from src.processing.geometry_engine import GeometryEngine

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def categorize_magnitude(mag_series: pd.Series) -> pd.Series:
    """Vectorized replacement for the previous .apply(lambda ...) pattern.
    np.select evaluates the whole column at once instead of looping row by row,
    which is significantly faster on large datasets."""
    conditions = [mag_series >= 6, mag_series < 4]
    choices = ["Severe", "Weak"]
    return np.select(conditions, choices, default="Average")

df_usgs = pd.read_csv(RAW_DIR / "JAPAN_USGS.csv")
df_geofon = pd.read_csv(RAW_DIR / "JAPAN_GEOFON.csv")
df_messy = pd.read_csv(RAW_DIR / "japan_messy_earthquakes.csv")
df_emsc = pd.read_csv(RAW_DIR / "JAPAN_EMSC.csv")

# Pre-processing & Cleaning 4 dataframes
# 1- JAPAN_USGS:
df_usgs = df_usgs[['time', 'latitude', 'longitude', 'depth', 'mag', 'place']]
df_usgs["time"] = pd.to_datetime(df_usgs["time"])
df_usgs["month"] = df_usgs["time"].dt.month_name()
df_usgs["category"] = categorize_magnitude(df_usgs["mag"])
df_usgs["area_name"] = df_usgs["place"].str.split(",").str[0]
df_usgs["area_name"] = df_usgs["area_name"].astype(str)
df_usgs = df_usgs.rename(columns={"mag": "magnitude"})
df_usgs["source"] = "JAPAN_USGS"

# 2- JAPAN_GEOFON:
df_geofon = df_geofon.drop(columns="Event_ID")
new_order = ['DateTime_UTC', 'Latitude', 'Longitude', 'Depth_km', 'Magnitude', 'Region']
df_geofon = df_geofon[new_order]
df_geofon["DateTime_UTC"] = pd.to_datetime(df_geofon["DateTime_UTC"], utc=True)
df_geofon["Depth_km"] = df_geofon["Depth_km"].astype(float)
df_geofon["month"] = df_geofon["DateTime_UTC"].dt.month_name()
df_geofon["category"] = categorize_magnitude(df_geofon["Magnitude"])
df_geofon["area_name"] = df_geofon["Region"].str.split(",").str[0]
df_geofon["area_name"] = df_geofon["area_name"].astype(str)
df_geofon["source"] = "JAPAN_GEOFON"
df_geofon = df_geofon.rename(columns={'DateTime_UTC': 'time', 'Latitude': 'latitude', 'Longitude': 'longitude',
                                      'Depth_km': 'depth', 'Magnitude': 'magnitude', 'Region': 'place'})

# 3- JAPAN_MESSY_EARTHQUAKES:
df_messy = df_messy.drop(columns=["status","notes"])
df_messy = df_messy.drop_duplicates()
def convert_type(x):
    if pd.isna(x):
        return pd.NaT
    x = str(x).strip()
    if re.match(r"\d{4}-\d{2}-\d{2}T", x):
        return pd.to_datetime(x, utc=True)
    elif re.match(r"[A-Za-z]{3}\s\d{1,2},\s\d{4}", x):
        return pd.to_datetime(x, format="%b %d, %Y, %H:%M:%S", utc=True)
    elif re.match(r"\d{4}-\d{2}-\d{2}\s", x):
        return pd.to_datetime(x, format="%Y-%m-%d %I:%M %p", utc=True)
    elif re.match(r"\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}", x):
        return pd.to_datetime(x, format="%d/%m/%Y %H:%M:%S", utc=True)
    else:
        return pd.to_datetime(x, utc=True)

df_messy["time"] = df_messy["time"].apply(convert_type)

numbers = {"zero": "0", "one": "1", "two": "2", "three": "3","four": "4",
            "five": "5", "six": "6", "seven": "7","eight": "8", "nine": "9", "point": "."}

def mag_to_float(x):
    if pd.isna(x):
        return np.nan
    x = str(x).lower()
    for word, num in numbers.items():
        x = x.replace(word, num)
    try:
        return float(x)
    except:
        return np.nan

df_messy["mag"] = df_messy["mag"].apply(mag_to_float)
df_messy["depth"] = df_messy["depth"].fillna(np.nan)

def depth_clean(val):
    if pd.isna(val):
        return np.nan
    val = str(val)
    if "miles" in val or "km" in val or "meters" in val:
        lst = val.split()
        if lst[1] == "miles":
            return float(lst[0]) * 1.6093
        elif lst[1] == "meters":
            return float(lst[0]) / 1000
        else:
            return float(lst[0])
    elif float(val) < 0:
        return -float(val)
    else:
        return float(val)

df_messy["depth"] = df_messy["depth"].apply(depth_clean)
df_messy.replace(["UNKNOWN"], np.nan, inplace=True)
df_messy["latitude"] = df_messy["latitude"].astype(float)

df_messy["latitude"] = df_messy["latitude"].fillna(df_messy["latitude"].mean())
df_messy["longitude"] = df_messy["longitude"].fillna(df_messy["longitude"].mean())
df_messy["depth"] = df_messy["depth"].fillna(df_messy["depth"].median())
df_messy["mag"] = df_messy["mag"].fillna(df_messy["mag"].mean())

df_messy["month"] = df_messy["time"].dt.month_name()
df_messy["category"] = categorize_magnitude(df_messy["mag"])
df_messy["area_name"] = df_messy["place"].str.split(",").str[0]
df_messy["area_name"] = df_messy["area_name"].astype(str)
df_messy = df_messy.rename(columns={"mag": "magnitude"})
df_messy["source"] = "japan_messy_earthquakes"

#4- JAPAN_EMSC:
df_emsc = df_emsc.drop(columns="magnitude_type")
df_emsc["date_time_UTC"] = pd.to_datetime(df_emsc["date_time_UTC"], utc=True)
df_emsc["depth_km"] = df_emsc["depth_km"].astype(float)
df_emsc["month"] = df_emsc["date_time_UTC"].dt.month_name()
df_emsc["category"] = categorize_magnitude(df_emsc["magnitude_value"])
df_emsc["area_name"] = df_emsc["region"].str.split(",").str[0]
df_emsc["area_name"] = df_emsc["area_name"].astype(str)
df_emsc["source"] = "JAPAN_EMSC"
df_emsc = df_emsc.rename(columns={'date_time_UTC': 'time', 'latitude_deg': 'latitude', 'longitude_deg': 'longitude',
                         'depth_km': 'depth', 'magnitude_value': 'magnitude', 'region': 'place'})

df_combined = pd.concat([df_usgs, df_geofon, df_messy, df_emsc], ignore_index=True)
df_combined[["latitude", "longitude", "depth"]] = df_combined[["latitude", "longitude", "depth"]].round(2)

# Bug fix: GeometryEngine was written but never called on df_combined.
# Apply the Haversine-based geometry calculations (distance to reference point,
# hypocenter distance, and Japan bounding-box check) to the final combined dataframe.
geo_engine = GeometryEngine()
df_combined = geo_engine.calculate_metrics(df_combined)

shape = df_combined.shape
indices = np.arange(1, len(df_combined)+1)
df_combined.index = indices
df_combined.to_csv(PROCESSED_DIR / "All_csv.csv", index=False)

print(f"There are {shape[0]} rows and {shape[1]} columns")
print("====================================================== «Japan Earthquake Analysis» ======================================================\n")
print(df_combined)

table1 = df_combined.groupby(["category", "month"]).size()
table1 = table1.reset_index()
table1 = table1.rename(columns={0:"count"})
table1 = table1.pivot_table("count", "category", "month", "sum", fill_value=0)
table1['Mean'] = table1.mean(axis=1).round(2)

table2 = df_combined.groupby("area_name").agg({"magnitude": ["mean", "max"], "depth": ["mean", "max"]}).round(2)
table3 = df_combined.groupby("area_name").size().sort_values(ascending=False)

print("============================== Earthquakes numbers & average by month ==============================")
print(table1)
print("=========================== Mean & Max of magnitude & depth by area_name ===========================")
print(table2)
print("================================  Number of earthquakes by area_name ================================")
print(table3)

table3.head(20).plot(kind='bar', figsize=(12,6))
plt.title("Top 20 Areas by Record Count")
plt.xlabel("Area Name")
plt.ylabel("Count")
plt.xticks(rotation=90)
