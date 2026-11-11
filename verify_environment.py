import polars as pl
import pyarrow
import requests
from dotenv import load_dotenv
from google.cloud import bigquery
import pytest

print("All dependencies are imported successfully.")

print("Polars version:", pl.__version__)
print("PyArrow version:", pyarrow.__version__)
print("Requests version:", requests.__version__)
print("BigQuery version:", bigquery.__version__)
print("Pytest version:", pytest.__version__)