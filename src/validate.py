
from pathlib import Path
from datetime import date

import polars as pl


# ---------------------------------------
# 1. DEFINE FILE PATH
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "weather_transformed.csv"
)


# ---------------------------------------
# 2. LOAD TRANSFORMED DATA
# ---------------------------------------

print("Loading transformed weather data...")

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Transformed file not found: {INPUT_FILE}"
    )

df = pl.read_csv(
    INPUT_FILE,
    try_parse_dates=True,
)

print(f"Loaded {df.height} records.")


# ---------------------------------------
# 3. DEFINE VALIDATION CHECKS
# ---------------------------------------

required_columns = [
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
    "temperature_range",
    "year",
    "month",
    "day",
]

expected_cities = [
    "cape_town",
    "durban",
    "johannesburg",
]


# ---------------------------------------
# 4. CHECK REQUIRED COLUMNS
# ---------------------------------------

columns_valid = all(
    column in df.columns
    for column in required_columns
)


# ---------------------------------------
# 5. CHECK RECORD COUNT
# ---------------------------------------

record_count_valid = df.height == 21


# ---------------------------------------
# 6. CHECK MISSING VALUES
# ---------------------------------------

missing_values = df.null_count().row(0)

no_missing_values = all(
    value == 0
    for value in missing_values
)


# ---------------------------------------
# 7. CHECK DUPLICATE RECORDS
# ---------------------------------------

duplicates = (
    df.group_by(["city", "date"])
    .len()
    .filter(pl.col("len") > 1)
)

no_duplicates = duplicates.height == 0


# ---------------------------------------
# 8. CHECK TEMPERATURE LOGIC
# ---------------------------------------

invalid_temperatures = df.filter(
    pl.col("temperature_2m_max")
    < pl.col("temperature_2m_min")
)

temperatures_valid = (
    invalid_temperatures.height == 0
)


# ---------------------------------------
# 9. CHECK NON-NEGATIVE MEASUREMENTS
# ---------------------------------------

invalid_measurements = df.filter(
    (pl.col("precipitation_sum") < 0)
    | (pl.col("wind_speed_10m_max") < 0)
)

measurements_valid = (
    invalid_measurements.height == 0
)


# ---------------------------------------
# 10. CHECK RECORDS PER CITY
# ---------------------------------------

city_counts = (
    df.group_by("city")
    .agg(pl.len().alias("total_records"))
)

city_counts_valid = (
    city_counts.height == 3
    and city_counts.filter(
        pl.col("total_records") != 7
    ).height == 0
    and sorted(city_counts["city"].to_list())
    == sorted(expected_cities)
)


# ---------------------------------------
# 11. CHECK DATE RANGE
# ---------------------------------------

from datetime import date

date_range_valid = (
    df["date"].min() == date(2025, 1, 1)
    and df["date"].max() == date(2025, 1, 7)
)


# ---------------------------------------
# 12. CHECK DATE COMPONENTS
# ---------------------------------------

date_components_valid = (
    df.filter(
        (pl.col("year") != pl.col("date").dt.year())
        | (pl.col("month") != pl.col("date").dt.month())
        | (pl.col("day") != pl.col("date").dt.day())
    ).height == 0
)


# ---------------------------------------
# 13. CHECK TEMPERATURE RANGE
# ---------------------------------------

temperature_range_valid = (
    df.filter(
        (
            pl.col("temperature_range")
            - (
                pl.col("temperature_2m_max")
                - pl.col("temperature_2m_min")
            )
        ).abs() > 0.001
    ).height == 0
)


# ---------------------------------------
# 14. DISPLAY VALIDATION RESULTS
# ---------------------------------------

validation_results = {
    "Required columns": columns_valid,
    "Expected record count (21)": record_count_valid,
    "No missing values": no_missing_values,
    "No duplicate city/date records": no_duplicates,
    "Maximum temperature >= minimum temperature": temperatures_valid,
    "Precipitation and wind speeds non-negative": measurements_valid,
    "Seven records per expected city": city_counts_valid,
    "Expected date range": date_range_valid,
    "Date components are correct": date_components_valid,
    "Temperature range calculations are correct": temperature_range_valid,
}

print("\n========== DATA QUALITY RESULTS ==========")

for check, passed in validation_results.items():
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {check}")


# ---------------------------------------
# 15. FINAL VALIDATION SUMMARY
# ---------------------------------------

passed_checks = sum(validation_results.values())

total_checks = len(validation_results)

failed_checks = total_checks - passed_checks

print("\n========== VALIDATION SUMMARY ==========")

print(f"Total checks: {total_checks}")
print(f"Passed checks: {passed_checks}")
print(f"Failed checks: {failed_checks}")

if failed_checks == 0:
    print("\nDATA QUALITY VALIDATION PASSED!")
else:
    print("\nDATA QUALITY VALIDATION FAILED!")
    raise SystemExit(1)
