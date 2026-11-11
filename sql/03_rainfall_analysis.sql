
-- Stage 9.3: Rainfall analysis by South African city

SELECT
    city,

    COUNT(*) AS days_recorded,

    ROUND(SUM(precipitation_sum), 2)
        AS total_rainfall_mm,

    ROUND(AVG(precipitation_sum), 2)
        AS average_daily_rainfall_mm,

    ROUND(MAX(precipitation_sum), 2)
        AS highest_daily_rainfall_mm,

    COUNTIF(precipitation_sum > 0)
        AS rainy_days,

    COUNTIF(precipitation_sum = 0)
        AS dry_days

FROM
    `open-data-etl-pipeline.weather_analytics_sa.weather_daily`

GROUP BY
    city

ORDER BY
    total_rainfall_mm DESC;
