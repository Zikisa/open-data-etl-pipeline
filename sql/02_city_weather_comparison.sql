
-- Stage 9.2: Compare weather across South African cities

SELECT
    city,

    COUNT(*) AS days_recorded,

    ROUND(AVG(temperature_2m_max), 2)
        AS average_max_temperature,

    ROUND(AVG(temperature_2m_min), 2)
        AS average_min_temperature,

    ROUND(MAX(temperature_2m_max), 2)
        AS highest_temperature,

    ROUND(MIN(temperature_2m_min), 2)
        AS lowest_temperature,

    ROUND(AVG(temperature_range), 2)
        AS average_temperature_range

FROM
    `open-data-etl-pipeline.weather_analytics_sa.weather_daily`

GROUP BY
    city

ORDER BY
    average_max_temperature DESC;
