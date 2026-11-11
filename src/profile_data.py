
from pathlib import Path

import polars as pl


# ---------------------------------------
# 1. DEFINE FILE PATH
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "raw" / "weather_data.csv"


# ---------------------------------------
# 2. LOAD RAW CSV DATA
# ---------------------------------------

df = pl.read_csv(
    INPUT_FILE,
    try_parse_dates=True,
)

print("\n========== DATASET OVERVIEW ==========")

# Display the number of rows and columns.
print("Dataset shape:", df.shape)

print("Total rows:", df.height)

print("Total columns:", df.width)


# ---------------------------------------
# 3. INSPECT COLUMN NAMES AND DATA TYPES
# ---------------------------------------

print("\n========== DATA SCHEMA ==========")

print(df.schema)


# ---------------------------------------
# 4. INSPECT FIRST FIVE RECORDS
# ---------------------------------------

print("\n========== FIRST FIVE RECORDS ==========")

print(df.head(5))


# ---------------------------------------
# 5. CHECK FOR MISSING VALUES
# ---------------------------------------

print("\n========== MISSING VALUES ==========")

print(df.null_count())


# ---------------------------------------
# 6. CHECK FOR DUPLICATE RECORDS
# ---------------------------------------

print("\n========== DUPLICATE RECORDS ==========")

duplicate_records = df.group_by(
    ["city", "date"]
).len().filter(
    pl.col("len") > 1
)

print("Duplicate city/date combinations:")

print(duplicate_records)

print("Duplicate combinations:", duplicate_records.height)


# ---------------------------------------
# 7. INSPECT NUMERIC STATISTICS
# ---------------------------------------

print("\n========== NUMERIC STATISTICS ==========")

numeric_columns = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
]

print(
    df.select(numeric_columns).describe()
)


# ---------------------------------------
# 8. INSPECT RECORDS PER CITY
# ---------------------------------------

print("\n========== RECORDS PER CITY ==========")

print(
    df.group_by("city")
    .agg(
        pl.len().alias("total_records")
    )
    .sort("city")
)


# ---------------------------------------
# 9. INSPECT DATE RANGE
# ---------------------------------------

print("\n========== DATE RANGE ==========")

print("Earliest date:", df["date"].min())

print("Latest date:", df["date"].max())


# ---------------------------------------
# 10. COMPLETION MESSAGE
# ---------------------------------------

print("\nData profiling completed successfully!")
