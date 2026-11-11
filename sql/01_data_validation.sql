
-- Stage 9.1: Verify BigQuery weather data

SELECT
    COUNT(*) AS total_records,

    COUNT(DISTINCT CONCAT(
        city,
        '|',
        CAST(date AS STRING)
    )) AS unique_city_date_records,

    COUNT(DISTINCT city) AS total_cities,

    MIN(date) AS first_weather_date,

    MAX(date) AS last_weather_date,

    COUNTIF(temperature_2m_max IS NULL)
        AS missing_max_temperature,

    COUNTIF(temperature_2m_min IS NULL)
        AS missing_min_temperature

FROM
    `open-data-etl-pipeline.weather_analytics_sa.weather_daily`;
