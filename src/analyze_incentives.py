import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# DRIVER INCENTIVE OPTIMIZATION
# Marketplace Incentive Analysis
# ============================================================

# Input dataset
INPUT_FILE = Path("data/driver_incentive_data.csv")

# Output directory
OUTPUT_DIR = Path("data/outputs")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 1. LOAD DATA
# ============================================================

print("\nLoading marketplace dataset...")

df = pd.read_csv(INPUT_FILE)

print(
    f"Dataset loaded successfully: {len(df):,} rows"
)


# ============================================================
# 2. BASIC DATA VALIDATION
# ============================================================

print("\nRunning basic data validation...")

print(
    f"Unique drivers: {df['driver_id'].nunique():,}"
)

print(
    f"Missing driver IDs: {df['driver_id'].isna().sum()}"
)

print(
    f"Missing trip values: {df['trips'].isna().sum()}"
)

print(
    f"Negative trip values: {(df['trips'] < 0).sum()}"
)


# ============================================================
# 3. AGGREGATE DRIVER PERFORMANCE
# ============================================================

print("\nCalculating driver-level performance...")


driver_summary = (

    df

    .groupby(
        [
            "driver_id",
            "segment",
            "incentive_strategy",
            "period"
        ],

        as_index=False
    )

    .agg(

        trips=(
            "trips",
            "sum"
        ),

        active_hours=(
            "active_hours",
            "sum"
        ),

        incentive_cost=(
            "incentive_cost",
            "sum"
        )
    )
)


# ============================================================
# 4. CREATE PRE / POST DATASET
# ============================================================

print(
    "\nCreating pre/post comparison..."
)


pivot = (

    driver_summary

    .pivot_table(

        index=[
            "driver_id",
            "segment",
            "incentive_strategy"
        ],

        columns="period",

        values=[
            "trips",
            "active_hours",
            "incentive_cost"
        ],

        aggfunc="sum",

        fill_value=0
    )
)


# Flatten column names

pivot.columns = [

    "_".join(column).strip()

    for column in pivot.columns
]


pivot = pivot.reset_index()


# ============================================================
# 5. CALCULATE PERFORMANCE CHANGE
# ============================================================

pivot["trip_change"] = (

    pivot["trips_post"]

    -

    pivot["trips_pre"]
)


pivot["active_hours_change"] = (

    pivot["active_hours_post"]

    -

    pivot["active_hours_pre"]
)


pivot["trip_pct_change"] = (

    pivot["trip_change"]

    /

    pivot["trips_pre"].replace(
        0,
        pd.NA
    )
)


# ============================================================
# 6. CALCULATE INCENTIVE EFFICIENCY
# ============================================================

pivot["incremental_trips_per_cost"] = (

    pivot["trip_change"]

    /

    pivot["incentive_cost_post"].replace(
        0,
        pd.NA
    )
)


# ============================================================
# 7. CREATE SEGMENT SUMMARY
# ============================================================

print(
    "\nCreating segment-level summary..."
)


segment_summary = (

    pivot

    .groupby(
        [
            "segment",
            "incentive_strategy"
        ],

        as_index=False
    )

    .agg(

        drivers=(
            "driver_id",
            "nunique"
        ),

        avg_pre_trips=(
            "trips_pre",
            "mean"
        ),

        avg_post_trips=(
            "trips_post",
            "mean"
        ),

        avg_trip_change=(
            "trip_change",
            "mean"
        ),

        avg_trip_pct_change=(
            "trip_pct_change",
            "mean"
        ),

        total_incentive_cost=(
            "incentive_cost_post",
            "sum"
        ),

        avg_incremental_trips_per_cost=(
            "incremental_trips_per_cost",
            "mean"
        )
    )
)


# ============================================================
# 8. ROUND VALUES
# ============================================================

numeric_columns = [

    "avg_pre_trips",
    "avg_post_trips",
    "avg_trip_change",
    "avg_trip_pct_change",
    "total_incentive_cost",
    "avg_incremental_trips_per_cost"
]


segment_summary[numeric_columns] = (

    segment_summary[numeric_columns]

    .round(2)
)


# ============================================================
# 9. SAVE ANALYTICAL OUTPUTS
# ============================================================

pivot.to_csv(

    OUTPUT_DIR
    / "driver_response.csv",

    index=False
)


segment_summary.to_csv(

    OUTPUT_DIR
    / "segment_summary.csv",

    index=False
)


# ============================================================
# 10. STRATEGY-LEVEL SUMMARY
# ============================================================

strategy_summary = (

    pivot

    .groupby(
        "incentive_strategy",
        as_index=False
    )

    .agg(

        drivers=(
            "driver_id",
            "nunique"
        ),

        avg_pre_trips=(
            "trips_pre",
            "mean"
        ),

        avg_post_trips=(
            "trips_post",
            "mean"
        ),

        avg_trip_change=(
            "trip_change",
            "mean"
        ),

        total_incentive_cost=(
            "incentive_cost_post",
            "sum"
        )
    )
)


strategy_summary = strategy_summary.round(2)


strategy_summary.to_csv(

    OUTPUT_DIR
    / "strategy_summary.csv",

    index=False
)


# ============================================================
# 11. PRINT BUSINESS SUMMARY
# ============================================================

print("\n")
print("=" * 70)

print(
    "STRATEGY-LEVEL BUSINESS SUMMARY"
)

print("=" * 70)

print(
    strategy_summary.to_string(
        index=False
    )
)


print("\n")
print("=" * 70)

print(
    "SEGMENT-LEVEL SUMMARY"
)

print("=" * 70)

print(
    segment_summary.to_string(
        index=False
    )
)


# ============================================================
# 12. VISUALIZATION — STRATEGY COMPARISON
# ============================================================

print(
    "\nCreating strategy comparison chart..."
)


plt.figure(
    figsize=(8, 5)
)


plt.bar(

    strategy_summary[
        "incentive_strategy"
    ],

    strategy_summary[
        "avg_trip_change"
    ]
)


plt.title(
    "Average Change in Trips by Incentive Strategy"
)


plt.xlabel(
    "Incentive Strategy"
)


plt.ylabel(
    "Average Change in Trips"
)


plt.tight_layout()


plt.savefig(

    OUTPUT_DIR
    / "strategy_trip_change.png",

    dpi=180
)


plt.close()


# ============================================================
# 13. VISUALIZATION — SEGMENT RESPONSE
# ============================================================

print(
    "Creating segment response charts..."
)


for strategy in (

    segment_summary[
        "incentive_strategy"
    ]

    .unique()

):

    subset = segment_summary[
        segment_summary[
            "incentive_strategy"
        ]

        == strategy
    ]


    plt.figure(
        figsize=(10, 5)
    )


    plt.bar(

        subset["segment"],

        subset["avg_trip_change"]
    )


    plt.title(

        f"Average Trip Change — {strategy}"
    )


    plt.xlabel(
        "Driver Segment"
    )


    plt.ylabel(
        "Average Change in Trips"
    )


    plt.xticks(
        rotation=25,
        ha="right"
    )


    plt.tight_layout()


    safe_name = (

        strategy

        .lower()

        .replace(
            " ",
            "_"
        )
    )


    plt.savefig(

        OUTPUT_DIR
        / f"{safe_name}_segment_response.png",

        dpi=180
    )


    plt.close()


# ============================================================
# 14. FINAL MESSAGE
# ============================================================

print("\n")
print("=" * 70)

print(
    "ANALYSIS COMPLETED SUCCESSFULLY"
)

print("=" * 70)

print(
    f"\nAll analytical outputs are available in:"
)

print(
    f"{OUTPUT_DIR}"
)

print("\nGenerated files:")

for file in OUTPUT_DIR.iterdir():

    print(
        f"  - {file.name}"
    )

print("\n")
