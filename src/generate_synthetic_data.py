import numpy as np
import pandas as pd
from pathlib import Path


# ============================================================
# DRIVER INCENTIVE OPTIMIZATION
# Synthetic Marketplace Data Generator
# ============================================================

# IMPORTANT:
# This project uses synthetic data.
# No confidential company data is used.


SEED = 42
rng = np.random.default_rng(SEED)

# Number of synthetic drivers
N_DRIVERS = 500

# Number of days before and after the incentive
DAYS_PRE = 14
DAYS_POST = 14


# ------------------------------------------------------------
# 1. CREATE DRIVER SEGMENTS
# ------------------------------------------------------------

segments = rng.choice(
    [
        "Highly Active",
        "Stable",
        "Low Activity",
        "At Risk / Declining"
    ],
    size=N_DRIVERS,
    p=[
        0.20,
        0.35,
        0.30,
        0.15
    ]
)


# ------------------------------------------------------------
# 2. ASSIGN INCENTIVE STRATEGIES
# ------------------------------------------------------------

strategies = rng.choice(
    [
        "Targeted",
        "Broad",
        "Control"
    ],
    size=N_DRIVERS,
    p=[
        0.35,
        0.35,
        0.30
    ]
)


# ------------------------------------------------------------
# 3. BASELINE ACTIVITY BY DRIVER SEGMENT
# ------------------------------------------------------------

segment_base = {

    "Highly Active": 13,

    "Stable": 8,

    "Low Activity": 4,

    "At Risk / Declining": 2
}


rows = []


# ------------------------------------------------------------
# 4. GENERATE DAILY DRIVER ACTIVITY
# ------------------------------------------------------------

for driver_num in range(N_DRIVERS):

    driver_id = f"D{driver_num + 1:04d}"

    segment = segments[driver_num]

    strategy = strategies[driver_num]

    baseline = segment_base[segment]


    # ----------------------------------------
    # Generate both pre and post periods
    # ----------------------------------------

    for period, days in [
        ("pre", DAYS_PRE),
        ("post", DAYS_POST)
    ]:

        for day in range(days):

            # Default multiplier
            multiplier = 1.0


            # ----------------------------------------
            # POST-INCENTIVE BEHAVIOR
            # ----------------------------------------

            if period == "post":

                # Targeted strategy
                if strategy == "Targeted":

                    multiplier = {

                        "Highly Active": 1.03,

                        "Stable": 1.18,

                        "Low Activity": 1.28,

                        "At Risk / Declining": 1.22

                    }[segment]


                # Broad strategy
                elif strategy == "Broad":

                    multiplier = {

                        "Highly Active": 1.02,

                        "Stable": 1.08,

                        "Low Activity": 1.10,

                        "At Risk / Declining": 1.08

                    }[segment]


                # Control group
                else:

                    multiplier = {

                        "Highly Active": 1.00,

                        "Stable": 1.02,

                        "Low Activity": 0.98,

                        "At Risk / Declining": 0.94

                    }[segment]


            # ----------------------------------------
            # SIMULATE NUMBER OF TRIPS
            # ----------------------------------------

            expected_trips = baseline * multiplier

            trips = max(
                0,
                int(rng.poisson(expected_trips))
            )


            # ----------------------------------------
            # SIMULATE ACTIVE HOURS
            # ----------------------------------------

            active_hours = max(
                0,
                rng.normal(
                    expected_trips / 2.2,
                    0.7
                )
            )


            # ----------------------------------------
            # SIMULATE INCENTIVE COST
            # ----------------------------------------

            incentive_cost = 0

            if (
                period == "post"
                and strategy != "Control"
            ):

                incentive_cost = round(
                    rng.uniform(2, 8),
                    2
                )


            # ----------------------------------------
            # STORE RECORD
            # ----------------------------------------

            rows.append(

                {

                    "driver_id": driver_id,

                    "segment": segment,

                    "incentive_strategy": strategy,

                    "period": period,

                    "day_number": day + 1,

                    "trips": trips,

                    "active_hours": round(
                        active_hours,
                        2
                    ),

                    "incentive_cost": incentive_cost

                }

            )


# ------------------------------------------------------------
# 5. CREATE DATAFRAME
# ------------------------------------------------------------

df = pd.DataFrame(rows)


# ------------------------------------------------------------
# 6. CREATE DATA DIRECTORY
# ------------------------------------------------------------

output_directory = Path("data")

output_directory.mkdir(
    exist_ok=True
)


# ------------------------------------------------------------
# 7. SAVE CSV
# ------------------------------------------------------------

output_file = (
    output_directory
    / "driver_incentive_data.csv"
)


df.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# 8. PRINT SUMMARY
# ------------------------------------------------------------

print(
    "\nSynthetic marketplace dataset created successfully!"
)

print(
    f"\nTotal rows: {len(df):,}"
)

print(
    f"Unique drivers: {df['driver_id'].nunique():,}"
)

print(
    "\nDriver segments:"
)

print(
    df[
        ["driver_id", "segment"]
    ]
    .drop_duplicates()
    ["segment"]
    .value_counts()
)

print(
    "\nIncentive strategies:"
)

print(
    df[
        ["driver_id", "incentive_strategy"]
    ]
    .drop_duplicates()
    ["incentive_strategy"]
    .value_counts()
)

print(
    f"\nDataset saved to: {output_file}"
)
