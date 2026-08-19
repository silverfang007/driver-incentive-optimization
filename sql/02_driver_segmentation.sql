-- ============================================================
-- DRIVER INCENTIVE OPTIMIZATION
-- SQL 02: Driver Segmentation
-- ============================================================
--
-- Purpose:
-- Create behavioral segments using pre-incentive activity.
--
-- Important:
-- Segmentation is based ONLY on the pre-incentive period.
-- This prevents the incentive treatment from influencing
-- the segment definition.
-- ============================================================


WITH driver_baseline AS (

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
                WHEN period = 'pre'
                THEN active_hours
                ELSE 0
            END
        ) AS pre_active_hours

    FROM driver_incentive_data

    GROUP BY
        driver_id,
        segment,
        incentive_strategy
)


SELECT

    driver_id,

    incentive_strategy,

    pre_trips,

    pre_active_hours,

    CASE

        WHEN pre_trips >= 140
            THEN 'Highly Active'

        WHEN pre_trips >= 80
            THEN 'Stable'

        WHEN pre_trips >= 40
            THEN 'Low Activity'

        ELSE 'At Risk / Declining'

    END AS behavioral_segment

FROM driver_baseline

ORDER BY
    pre_trips DESC;
