\# South African Weather Analytics – Open Data ETL Pipeline



\## Project Overview



This project demonstrates an end-to-end data engineering pipeline that extracts historical weather data for three South African cities, transforms and validates the data, stores it in Parquet format, loads it into Google BigQuery, and presents analytical insights through SQL and Power BI.



The project uses weather observations from Cape Town, Durban, and Johannesburg for 1–7 January 2025.



\## Architecture



```text

Open-Meteo Archive API

&#x20;         |

&#x20;         v

&#x20;   Python Extraction

&#x20;         |

&#x20;         v

&#x20;      Raw CSV

&#x20;         |

&#x20;         v

&#x20;  Polars Transformation

&#x20;         |

&#x20;         v

&#x20;   Data Validation

&#x20;         |

&#x20;         v

&#x20;   Processed Parquet

&#x20;         |

&#x20;         v

&#x20;     BigQuery

&#x20;         |

&#x20;         v

&#x20;     SQL Analytics

&#x20;         |

&#x20;         v

&#x20;   Power BI Dashboard

```



\## Technology Stack



| Technology | Purpose |

|---|---|

| Python | Data extraction and pipeline orchestration |

| Polars | Data transformation and processing |

| PyArrow | Parquet file support |

| Open-Meteo API | Historical weather data source |

| Google BigQuery | Cloud data warehouse |

| SQL | Data analysis and aggregation |

| Power BI | Dashboard and visualisation |

| Git | Version control |



\## Project Structure



```text

open-data-etl-pipeline/

├── data/

│   ├── archive/

│   ├── processed/

│   └── raw/

├── logs/

├── powerbi/

│   └── South African Weather Analytics.pbix

├── sql/

│   ├── 01\_data\_validation.sql

│   ├── 02\_city\_weather\_comparison.sql

│   ├── 03\_rainfall\_analysis.sql

│   ├── 04\_weather\_trends.sql

│   └── 05\_wind\_analysis.sql

└── src/

&#x20;   ├── extract.py

&#x20;   ├── profile\_data.py

&#x20;   ├── transform.py

&#x20;   ├── validate.py

&#x20;   ├── to\_parquet.py

&#x20;   └── load\_to\_bigquery.py

```



\## Data Pipeline



\### 1. Extraction



Extracted historical daily weather observations from the Open-Meteo Archive API for:

\- Cape Town

\- Durban

\- Johannesburg



The extraction generated 21 records covering seven days for each city.



\### 2. Transformation



Used Polars to:

\- Process and standardise the weather data.

\- Calculate daily temperature ranges.

\- Extract year, month, and day components.

\- Prepare the dataset for analytical storage.



\### 3. Data Quality Validation



Implemented validation checks covering:

\- Required columns.

\- Missing values.

\- Duplicate city/date combinations.

\- Temperature consistency.

\- Non-negative precipitation and wind speed.

\- Expected record counts.

\- Date range and calculated fields.



All 10 validation checks passed.



\### 4. Parquet Storage



Converted the transformed CSV dataset into Parquet using PyArrow support and ZSTD compression.



\### 5. BigQuery Loading



Loaded the processed dataset into:



\- Google Cloud project: `open-data-etl-pipeline`

\- BigQuery dataset: `weather\_analytics\_sa`

\- Table: `weather\_daily`

\- Location: `africa-south1`



The table contains 21 records and 14 columns.



\### 6. SQL Analytics



Created SQL queries to analyse:

\- Dataset quality and completeness.

\- Temperature comparisons by city.

\- Rainfall patterns.

\- Daily weather trends.

\- Wind speed comparisons.



\### 7. Power BI Dashboard



Created an interactive dashboard featuring:

\- Weather KPI cards.

\- Average maximum and minimum temperatures.

\- Daily temperature trends.

\- South African city map.

\- Weather summary table.

\- City filtering.



\## Key Findings



Based on the seven-day sample:



\- Durban recorded the highest average maximum temperature at approximately 30.37°C.

\- Durban recorded the highest total rainfall at 51.0 mm.

\- Johannesburg recorded rainfall on all seven days.

\- Cape Town recorded no rainfall during the sample period.

\- Cape Town recorded the highest average maximum wind speed at approximately 19.74 km/h.



These findings describe the selected seven-day sample and should not be interpreted as long-term climate averages.



\## Running the Pipeline



Create and activate a Python virtual environment:



```powershell

py -3.12 -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

python -m pip install -r requirements.txt

```



Run the pipeline stages:



```powershell

python src/extract.py

python src/profile\_data.py

python src/transform.py

python src/validate.py

python src/to\_parquet.py

python src/load\_to\_bigquery.py

```



Google Cloud authentication and BigQuery permissions are required for the cloud-loading stage.



Run the SQL files in BigQuery Studio and open the Power BI report from the `powerbi` directory.



\## Future Improvements



\- Increase the historical data range.

\- Automate scheduled extraction.

\- Introduce incremental BigQuery loading.

\- Add automated testing to the pipeline.

\- Implement GitHub Actions for CI.

\- Expand the Power BI dashboard with additional analytical pages.



\## Data Source



\[Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)



\## Author



Data Engineering Portfolio Project



\*\*Focus areas:\*\* Python, SQL, Polars, ETL, Parquet, BigQuery, and Power BI.