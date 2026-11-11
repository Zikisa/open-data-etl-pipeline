"""
Stage 7: Convert transformed weather CSV data to Parquet.

Input:
    data/processed/weather_transformed.csv

Output:
    data/processed/weather_transformed.parquet
"""

from pathlib import Path
import polars as pl


# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "weather_transformed.csv"

OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "weather_transformed.parquet"


# --------------------------------------------------
# 2. Check that the input file exists
# --------------------------------------------------

print("Starting CSV to Parquet conversion...")

if not INPUT_FILE.exists():
    raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")


# --------------------------------------------------
# 3. Read transformed CSV using Polars
# --------------------------------------------------

print("\nReading transformed CSV data...")

df = pl.read_csv(
    INPUT_FILE,
    try_parse_dates=True
)

print(f"Records loaded: {df.height}")
print(f"Columns loaded: {df.width}")


# --------------------------------------------------
# 4. Convert CSV DataFrame to Parquet
# --------------------------------------------------

print("\nConverting data to Parquet...")

df.write_parquet(
    OUTPUT_FILE,
    compression="zstd"
)

print(f"Parquet file created: {OUTPUT_FILE}")


# --------------------------------------------------
# 5. Read Parquet file back for verification
# --------------------------------------------------

print("\nVerifying Parquet output...")

parquet_df = pl.read_parquet(OUTPUT_FILE)


# --------------------------------------------------
# 6. Validate record count and column names
# --------------------------------------------------

assert parquet_df.height == df.height, "Record count mismatch!"

assert parquet_df.columns == df.columns, "Column names mismatch!"


# --------------------------------------------------
# 7. Display final results
# --------------------------------------------------

print("\n========== PARQUET CONVERSION RESULTS ==========")

print(f"Original CSV records: {df.height}")
print(f"Parquet records: {parquet_df.height}")

print(f"Original CSV columns: {df.width}")
print(f"Parquet columns: {parquet_df.width}")

print(f"Parquet file size: {OUTPUT_FILE.stat().st_size:,} bytes")

print("\nParquet schema:")
print(parquet_df.schema)

print("\nSample records:")
print(parquet_df.head(5))

print("\nPARQUET CONVERSION SUCCESSFUL!")