-- =====================================================
-- 05: Wind Speed Analysis by South African City
-- Source: BigQuery weather_daily
-- =====================================================

SELECT
    city,
    COUNT(*) AS days_recorded,
    ROUND(AVG(wind_speed_10m_max), 2) AS average_wind_speed,
    ROUND(MAX(wind_speed_10m_max), 2) AS highest_wind_speed,
    ROUND(MIN(wind_speed_10m_max), 2) AS lowest_wind_speed
FROM
    `open-data-etl-pipeline.weather_analytics_sa.weather_daily`
GROUP BY
    city
ORDER BY
    average_wind_speed DESC;