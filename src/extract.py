
from pathlib import Path

import polars as pl
import truststore

# Use the Windows trusted certification store.
truststore.inject_into_ssl()
import requests


# ---------------------------------------
# 1. PROJECT CONFIGURATION
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = BASE_DIR / "data" / "raw"

OUTPUT_FILE = RAW_DATA_DIR / "weather_data.csv"

API_URL = "https://archive-api.open-meteo.com/v1/archive"

START_DATE = "2025-01-01"
END_DATE = "2025-01-07"


# ---------------------------------------
# 2. DEFINE CITY LOCATIONS
# ---------------------------------------

CITIES = {
    "Cape Town": {
        "latitude": -33.9249,
        "longitude": 18.4241,
    },
    "Johannesburg": {
        "latitude": -26.2041,
        "longitude": 28.0473,
    },
    "Durban": {
        "latitude": -29.8587,
        "longitude": 31.0218,
    },
}


# ---------------------------------------
# 3. DEFINE WEATHER VARIABLES
# ---------------------------------------

WEATHER_VARIABLES = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
    "weather_code",
]


# ---------------------------------------
# 4. EXTRACT WEATHER DATA
# ---------------------------------------

def extract_weather_data(city, coordinates):

    print(f"Extracting weather data for {city}...")

    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": ",".join(WEATHER_VARIABLES),
        "timezone": "Africa/Johannesburg",
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if "daily" not in data:
        raise ValueError(
            f"No daily weather data returned for {city}"
        )

    daily_data = data["daily"]

    # Convert API response into a Polars DataFrame.
    df = pl.DataFrame(daily_data)

    # Add city information.
    df = df.with_columns(
        [
            pl.lit(city).alias("city"),
            pl.lit("South Africa").alias("country"),
            pl.lit(coordinates["latitude"]).alias("latitude"),
            pl.lit(coordinates["longitude"]).alias("longitude"),
        ]
    )

    # Rename the date column.
    df = df.rename({"time": "date"})

    # Convert date strings into date values.
    df = df.with_columns(
        pl.col("date").str.to_date("%Y-%m-%d")
    )

    # Organise the columns.
    df = df.select(
        [
            "date",
            "city",
            "country",
            "latitude",
            "longitude",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max",
            "weather_code",
        ]
    )

    print(f"Successfully extracted {city}: {df.height} rows")

    return df


# ---------------------------------------
# 5. RUN EXTRACTION FOR ALL CITIES
# ---------------------------------------

def main():

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    weather_data = []

    for city, coordinates in CITIES.items():

        df = extract_weather_data(
            city,
            coordinates,
        )

        weather_data.append(df)

    # Combine all city datasets.
    final_df = pl.concat(weather_data)

    # Sort data by city and date.
    final_df = final_df.sort(
        ["city", "date"]
    )

    # Save extracted data as CSV.
    final_df.write_csv(OUTPUT_FILE)

    print("\nExtraction completed successfully!")

    print(f"Total records: {final_df.height}")

    print(f"Output file: {OUTPUT_FILE}")

    print("\nData preview:")

    print(final_df.head(10))

    print("\nRecords per city:")

    print(
        final_df.group_by("city")
        .len()
        .sort("city")
    )


# ---------------------------------------
# 6. EXECUTE THE PIPELINE
# ---------------------------------------

if __name__ == "__main__":
    main()
