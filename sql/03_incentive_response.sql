-- ============================================================
-- DRIVER INCENTIVE OPTIMIZATION
-- SQL 03: Incentive Response Analysis
-- ============================================================
--
-- Purpose:
-- Compare driver activity before and after the incentive.
--
-- Key question:
-- Did driver activity increase after the intervention?
--
-- Metrics:
--   1. Pre-period trips
--   2. Post-period trips
--   3. Absolute trip change
--   4. Percentage trip change
--   5. Incentive cost
--   6. Incremental trips per incentive cost
-- ============================================================


WITH driver_period_summary AS (

    SELECT

        driver_id,

        segment,

        incentive_strategy,

        SUM(
            CASE
                WHEN period = 'pre'
                THEN trips
                ELSE 0
            END
        ) AS pre_trips,

        SUM(
            CASE
                WHEN period = 'post'
                THEN trips
                ELSE 0
            END
        ) AS post_trips,

        SUM(
            CASE
                WHEN period = 'pre'
                THEN active_hours
                ELSE 0
            END
        ) AS pre_active_hours,

        SUM(
            CASE
                WHEN period = 'post'
                THEN active_hours
                ELSE 0
            END
        ) AS post_active_hours,

        SUM(
            CASE
                WHEN period = 'post'
                THEN incentive_cost
                ELSE 0
            END
        ) AS incentive_cost

    FROM driver_incentive_data

    GROUP BY
        driver_id,
        segment,
        incentive_strategy
)


SELECT

    driver_id,

    segment,

    incentive_strategy,

    pre_trips,

    post_trips,

    post_trips - pre_trips
        AS trip_change,

    ROUND(

        (
            post_trips - pre_trips
        )

        /

        NULLIF(
            pre_trips,
            0
        ),

        4

    ) AS trip_pct_change,

    pre_active_hours,

    post_active_hours,

    post_active_hours - pre_active_hours
        AS active_hours_change,

    ROUND(
        incentive_cost,
        2
    ) AS incentive_cost,

    ROUND(

        (
            post_trips - pre_trips
        )

        /

        NULLIF(
            incentive_cost,
            0
        ),

        2

    ) AS incremental_trips_per_cost

FROM driver_period_summary

ORDER BY
    trip_change DESC;
