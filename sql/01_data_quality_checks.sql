-- ============================================================
-- DRIVER INCENTIVE OPTIMIZATION
-- SQL 01: Data Quality Checks
-- ============================================================
--
-- Purpose:
-- Validate marketplace driver activity data before analysis.
--
-- The project uses synthetic data for portfolio purposes.
-- ============================================================


-- ============================================================
-- 1. CHECK TOTAL RECORD COUNT
-- ============================================================

SELECT
    COUNT(*) AS total_records
FROM driver_incentive_data;


-- ============================================================
-- 2. CHECK UNIQUE DRIVERS
-- ============================================================

SELECT
    COUNT(DISTINCT driver_id) AS unique_drivers
FROM driver_incentive_data;


-- ============================================================
-- 3. CHECK NULL VALUES
-- ============================================================

SELECT
    SUM(
        CASE
            WHEN driver_id IS NULL THEN 1
            ELSE 0
        END
    ) AS null_driver_ids,

    SUM(
        CASE
            WHEN segment IS NULL THEN 1
            ELSE 0
        END
    ) AS null_segments,

    SUM(
        CASE
            WHEN incentive_strategy IS NULL THEN 1
            ELSE 0
        END
    ) AS null_strategies,

    SUM(
        CASE
            WHEN period IS NULL THEN 1
            ELSE 0
        END
    ) AS null_periods,

    SUM(
        CASE
            WHEN trips IS NULL THEN 1
            ELSE 0
        END
    ) AS null_trips,

    SUM(
        CASE
            WHEN active_hours IS NULL THEN 1
            ELSE 0
        END
    ) AS null_active_hours,

    SUM(
        CASE
            WHEN incentive_cost IS NULL THEN 1
            ELSE 0
        END
    ) AS null_incentive_cost

FROM driver_incentive_data;


-- ============================================================
-- 4. CHECK INVALID NEGATIVE VALUES
-- ============================================================

SELECT
    SUM(
        CASE
            WHEN trips < 0 THEN 1
            ELSE 0
        END
    ) AS negative_trips,

    SUM(
        CASE
            WHEN active_hours < 0 THEN 1
            ELSE 0
        END
    ) AS negative_active_hours,

    SUM(
        CASE
            WHEN incentive_cost < 0 THEN 1
            ELSE 0
        END
    ) AS negative_incentive_cost

FROM driver_incentive_data;


-- ============================================================
-- 5. CHECK VALID SEGMENTS
-- ============================================================

SELECT
    segment,
    COUNT(*) AS records
FROM driver_incentive_data
GROUP BY segment
ORDER BY records DESC;


-- ============================================================
-- 6. CHECK VALID INCENTIVE STRATEGIES
-- ============================================================

SELECT
    incentive_strategy,
    COUNT(DISTINCT driver_id) AS drivers
FROM driver_incentive_data
GROUP BY incentive_strategy
ORDER BY drivers DESC;


-- ============================================================
-- 7. CHECK PRE / POST DISTRIBUTION
-- ============================================================

SELECT
    period,
    COUNT(*) AS records,
    COUNT(DISTINCT driver_id) AS drivers
FROM driver_incentive_data
GROUP BY period
ORDER BY period;


-- ============================================================
-- 8. CHECK DUPLICATE DRIVER / PERIOD / DAY RECORDS
-- ============================================================

SELECT
    driver_id,
    period,
    day_number,
    COUNT(*) AS record_count
FROM driver_incentive_data
GROUP BY
    driver_id,
    period,
    day_number
HAVING COUNT(*) > 1;


-- ============================================================
-- 9. BASIC ACTIVITY DISTRIBUTION
-- ============================================================

SELECT
    incentive_strategy,

    COUNT(DISTINCT driver_id) AS drivers,

    ROUND(
        AVG(trips),
        2
    ) AS avg_trips,

    ROUND(
        AVG(active_hours),
        2
    ) AS avg_active_hours,

    ROUND(
        SUM(incentive_cost),
        2
    ) AS total_incentive_cost

FROM driver_incentive_data

GROUP BY incentive_strategy

ORDER BY avg_trips DESC;
