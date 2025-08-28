# data_cleaner.py
import os
import re
import pickle
import logging
from datetime import datetime
from typing import Dict, Any

import pandas as pd

# -------------------------
# CONSTANTS
# -------------------------
MARITIME_KEYWORDS = [
    "boat", "ship", "vessel", "port", "harbor", "harbour", "dock", "pier",
    "coast", "coastal", "fishermen", "fishing", "naval", "sea", "maritime", "gulf"
]
MARITIME_REGEX = re.compile(r"\b(" + "|".join(MARITIME_KEYWORDS) + r")\b", flags=re.IGNORECASE)

LAND_EVENTS = [
    'Riots/Protests', 'Riots', 'Protests', 'Peaceful protest', 'Civil Unrest',
    'Demonstrations', 'Strikes', 'Civil Disorder', 'Political Violence',
    'Social Unrest', 'Protest', 'Peaceful Protest', 'Violent Protest',
    'Mass Protest', 'Street Protest', 'Political Protest', 'Labor Strike',
    'General Strike', 'Work Stoppage', 'Industrial Action'
]

LANDLOCKED_COUNTRIES = {
    'Afghanistan', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 
    'Bhutan', 'Bolivia', 'Botswana', 'Burkina Faso', 'Burundi', 'Central African Republic', 
    'Chad', 'Czech Republic', 'Czechia', 'Eswatini', 'Ethiopia', 'Hungary', 
    'Kazakhstan', 'Kyrgyzstan', 'Laos', 'Lesotho', 'Liechtenstein', 'Luxembourg', 
    'Mali', 'Moldova', 'Mongolia', 'Nepal', 'Niger', 'North Macedonia', 
    'Paraguay', 'Rwanda', 'San Marino', 'Serbia', 'Slovakia', 'South Sudan', 
    'Switzerland', 'Tajikistan', 'Turkmenistan', 'Uganda', 'Uzbekistan', 
    'Vatican City', 'Zambia', 'Zimbabwe'
}

OCEAN_REGIONS = [
    {'lat_min': -60, 'lat_max': 60, 'lon_min': 100, 'lon_max': 260},   # Pacific
    {'lat_min': -60, 'lat_max': 60, 'lon_min': -80, 'lon_max': 20},    # Atlantic
    {'lat_min': -60, 'lat_max': 30, 'lon_min': 20, 'lon_max': 120},    # Indian
    {'lat_min': 60,  'lat_max': 90, 'lon_min': -180, 'lon_max': 180},  # Arctic
    {'lat_min': -90, 'lat_max': -60, 'lon_min': -180, 'lon_max': 180}, # Southern
]

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# -------------------------
# HELPERS
# -------------------------

def has_maritime_keywords(notes: str) -> bool:
    return bool(notes) and bool(MARITIME_REGEX.search(str(notes)))

def is_ocean_coordinate(lat: float, lon: float) -> bool:
    if pd.isna(lat) or pd.isna(lon):
        return False
    return any(region['lat_min'] <= lat <= region['lat_max'] and
               region['lon_min'] <= lon <= region['lon_max']
               for region in OCEAN_REGIONS)

def is_maritime_event(event_type: str, sub_event_type: str) -> bool:
    event_text = f"{event_type} {sub_event_type}".lower()
    return not any(land_event.lower() in event_text for land_event in LAND_EVENTS)

def is_coastal_country(country: str) -> bool:
    return country not in LANDLOCKED_COUNTRIES

# -------------------------
# MAIN PIPELINE
# -------------------------

def clean_maritime_data(
    csv_file: str = "2024-01-01-2024-12-31.csv",
    cache_file: str = "maritime_data_cache.pkl"
) -> Dict[str, Any]:

    if (os.path.exists(cache_file) and 
        os.path.getmtime(cache_file) > os.path.getmtime(csv_file)):
        logging.info("Loading cached data...")
        with open(cache_file, "rb") as f:
            return pickle.load(f)

    logging.info("Processing CSV data...")

    usecols = ['Event_Date', 'Event_Type', 'Sub_Event_Type', 'Country', 
               'Location', 'Latitude', 'Longitude', 'Notes']
    df = pd.read_csv(
        csv_file, usecols=usecols,
        dtype={
            'Country': 'category',
            'Event_Type': 'category',
            'Sub_Event_Type': 'category',
            'Location': 'string',
            'Latitude': 'float32',
            'Longitude': 'float32'
        }
    )
    df['Event_Date'] = pd.to_datetime(df['Event_Date'], format='%m/%d/%Y %H:%M')

    logging.info(f"Total events loaded: {len(df):,}")

    # === Step 1: Maritime keywords ===
    before = len(df)
    df = df[df['Notes'].apply(has_maritime_keywords)]
    logging.info(f"Keyword filter removed {before - len(df):,} rows → {len(df):,} left")

    # === Step 2: Remove Township ===
    before = len(df)
    df = df[~df['Notes'].str.contains("Township", case=False, na=False)]
    logging.info(f"'Township' filter removed {before - len(df):,} rows → {len(df):,} left")

    # === Step 3: Coastal countries ===
    before = len(df)
    df = df[df['Country'].apply(is_coastal_country)]
    logging.info(f"Landlocked filter removed {before - len(df):,} rows → {len(df):,} left")

    # === Step 4: Maritime events ===
    before = len(df)
    df = df[df.apply(lambda r: is_maritime_event(r['Event_Type'], r['Sub_Event_Type']), axis=1)]
    logging.info(f"Land-event filter removed {before - len(df):,} rows → {len(df):,} left")

    # === Step 5: Ocean coordinates ===
    before = len(df)
    df = df[df.apply(lambda r: is_ocean_coordinate(r['Latitude'], r['Longitude']), axis=1)]
    logging.info(f"Coordinate filter removed {before - len(df):,} rows → {len(df):,} left")

    # Final cleanup
    df = df.dropna(subset=['Country', 'Latitude', 'Longitude'])

    data_package = {
        'df_events': df,
        'countries': df['Country'].cat.categories.tolist(),
        'events': df['Event_Type'].cat.categories.tolist(),
        'total_events': len(df),
        'total_countries': df['Country'].nunique(),
        'cache_timestamp': datetime.now()
    }

    with open(cache_file, "wb") as f:
        pickle.dump(data_package, f)
    logging.info(f"Data processing complete: {len(df):,} events cached")

    return data_package

# -------------------------
# METADATA
# -------------------------

def get_filtering_stats() -> Dict[str, Any]:
    return {
        'maritime_keywords': MARITIME_KEYWORDS,
        'landlocked_countries_count': len(LANDLOCKED_COUNTRIES),
        'land_events_filtered': LAND_EVENTS
    }
