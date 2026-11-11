
-- Stage 9.4: Daily weather trends

SELECT
    date,
    city,

    temperature_2m_max,
    temperature_2m_min,

    temperature_range,

    precipitation_sum,

    wind_speed_10m_max

FROM
    `open-data-etl-pipeline.weather_analytics_sa.weather_daily`

ORDER BY
    date ASC,
    city ASC;
