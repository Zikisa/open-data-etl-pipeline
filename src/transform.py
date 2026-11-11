
from pathlib import Path

import polars as pl


# ---------------------------------------
# 1. DEFINE FILE PATHS
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "raw" / "weather_data.csv"

OUTPUT_FILE = BASE_DIR / "data" / "processed" / "weather_transformed.csv"


# ---------------------------------------
# 2. LOAD RAW DATA
# ---------------------------------------

print("Loading raw weather data...")

df = pl.read_csv(
    INPUT_FILE,
    try_parse_dates=True,
)

print(f"Loaded {df.height} records.")


# ---------------------------------------
# 3. STANDARDISE CITY NAMES
# ---------------------------------------

df = df.with_columns(
    pl.col("city")
    .str.to_lowercase()
    .str.replace_all(" ", "_")
    .alias("city")
)


# ---------------------------------------
# 4. ROUND NUMERIC MEASUREMENTS
# ---------------------------------------

df = df.with_columns(
    pl.col("temperature_2m_max").round(2),
    pl.col("temperature_2m_min").round(2),
    pl.col("precipitation_sum").round(2),
    pl.col("wind_speed_10m_max").round(2),
)


# ---------------------------------------
# 5. CREATE TEMPERATURE RANGE
# ---------------------------------------

df = df.with_columns(
    (
        pl.col("temperature_2m_max")
        - pl.col("temperature_2m_min")
    ).round(2).alias("temperature_range")
)


# ---------------------------------------
# 6. EXTRACT DATE COMPONENTS
# ---------------------------------------

df = df.with_columns(
    pl.col("date").dt.year().alias("year"),
    pl.col("date").dt.month().alias("month"),
    pl.col("date").dt.day().alias("day"),
)


# ---------------------------------------
# 7. SORT TRANSFORMED DATA
# ---------------------------------------

df = df.sort(
    ["city", "date"]
)


# ---------------------------------------
# 8. SAVE TRANSFORMED DATA
# ---------------------------------------

df.write_csv(OUTPUT_FILE)


# ---------------------------------------
# 9. DISPLAY RESULTS
# ---------------------------------------

print("\n========== TRANSFORMATION RESULTS ==========")

print("Output file:", OUTPUT_FILE)

print("Total records:", df.height)

print("Total columns:", df.width)

print("\nTransformed schema:")

print(df.schema)

print("\nFirst five transformed records:")

print(df.head(5))

print("\nRecords per city:")

print(
    df.group_by("city")
    .agg(
        pl.len().alias("total_records")
    )
    .sort("city")
)

print("\nTransformation completed successfully!")
