-- ============================================================
-- DRIVER INCENTIVE OPTIMIZATION
-- SQL 04: Segment-Level Executive Summary
-- ============================================================
--
-- Purpose:
-- Summarize incentive performance by behavioral segment
-- and incentive strategy.
--
-- Business question:
--
-- "Which driver segments respond most strongly to each
-- incentive strategy, and where should incentive budget
-- be concentrated?"
-- ============================================================


WITH driver_response AS (

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
),


segment_summary AS (

    SELECT

        segment,

        incentive_strategy,

        COUNT(
            DISTINCT driver_id
        ) AS drivers,

        ROUND(
            AVG(pre_trips),
            2
        ) AS avg_pre_trips,

        ROUND(
            AVG(post_trips),
            2
        ) AS avg_post_trips,

        ROUND(
            AVG(
                post_trips - pre_trips
            ),
            2
        ) AS avg_trip_change,

        ROUND(

            AVG(

                (
                    post_trips - pre_trips
                )

                /

                NULLIF(
                    pre_trips,
                    0
                )

            ),

            4

        ) AS avg_trip_pct_change,

        ROUND(
            SUM(incentive_cost),
            2
        ) AS total_incentive_cost,

        ROUND(

            SUM(
                post_trips - pre_trips
            )

            /

            NULLIF(
                SUM(incentive_cost),
                0
            ),

            2

        ) AS incremental_trips_per_cost

    FROM driver_response

    GROUP BY

        segment,

        incentive_strategy
)


SELECT

    segment,

    incentive_strategy,

    drivers,

    avg_pre_trips,

    avg_post_trips,

    avg_trip_change,

    avg_trip_pct_change,

    total_incentive_cost,

    incremental_trips_per_cost

FROM segment_summary

ORDER BY

    incremental_trips_per_cost DESC;
