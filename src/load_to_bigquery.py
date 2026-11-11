
"""
Stage 8: Load Parquet weather data into Google BigQuery.
"""

from pathlib import Path

from google.cloud import bigquery
from datetime import datetime, timedelta, timezone


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

PROJECT_ID = "open-data-etl-pipeline"
DATASET_ID = "weather_analytics_sa"
TABLE_ID = "weather_daily"
LOCATION = "africa-south1"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PARQUET_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "weather_transformed.parquet"
)

FULL_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"


# --------------------------------------------------
# 2. Connect to BigQuery
# --------------------------------------------------

print("Connecting to Google BigQuery...")

client = bigquery.Client(project=PROJECT_ID)

print("BigQuery connection successful!")


# --------------------------------------------------
# 3. Verify dataset location
# --------------------------------------------------

print("\nChecking BigQuery dataset...")

dataset = client.get_dataset(
    f"{PROJECT_ID}.{DATASET_ID}"
)

if dataset.location != LOCATION:
    raise ValueError(
        f"Incorrect dataset location: {dataset.location}"
    )

print(f"Dataset: {DATASET_ID}")
print(f"Location: {dataset.location}")


# --------------------------------------------------
# 4. Set dataset default expiration to 59 days
# --------------------------------------------------

print("\nChecking dataset expiration policy...")

expiration_ms = 59 * 24 * 60 * 60 * 1000

if dataset.default_table_expiration_ms != expiration_ms:

    dataset.default_table_expiration_ms = expiration_ms

    client.update_dataset(
        dataset,
        ["default_table_expiration_ms"]
    )

    print("Dataset expiration updated to 59 days.")

else:
    print("Dataset expiration already set to 59 days.")

# --------------------------------------------------
# 5. Check Parquet file
# --------------------------------------------------

print("\nChecking Parquet file...")

if not PARQUET_FILE.exists():
    raise FileNotFoundError(
        f"Parquet file not found: {PARQUET_FILE}"
    )

print(f"File: {PARQUET_FILE}")
print(f"Size: {PARQUET_FILE.stat().st_size:,} bytes")


# --------------------------------------------------
# 6. Configure BigQuery load job
# --------------------------------------------------

print("\nPreparing BigQuery load job...")



job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    autodetect=True,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
)


# --------------------------------------------------
# 7. Upload Parquet file
# --------------------------------------------------

print("\nUploading Parquet data to BigQuery...")

with open(PARQUET_FILE, "rb") as parquet_file:

    load_job = client.load_table_from_file(
        parquet_file,
        FULL_TABLE_ID,
        job_config=job_config,
        location=LOCATION
    )

print(f"Load job started: {load_job.job_id}")

load_job.result()

print("BigQuery load job completed successfully!")


# --------------------------------------------------
# 8. Verify uploaded table
# --------------------------------------------------

print("\nVerifying BigQuery table...")

table = client.get_table(FULL_TABLE_ID)

print("\n========== BIGQUERY LOAD RESULTS ==========")

print(f"Project: {PROJECT_ID}")
print(f"Dataset: {DATASET_ID}")
print(f"Table: {TABLE_ID}")
print(f"Location: {table.location}")

print(f"Total records: {table.num_rows}")
print(f"Total columns: {len(table.schema)}")

print("\nBigQuery schema:")

for field in table.schema:
    print(f"{field.name}: {field.field_type}")

print("\nBIGQUERY DATA LOAD SUCCESSFUL!")
