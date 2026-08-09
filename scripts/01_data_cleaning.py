"""
01_data_cleaning.py
--------------------
Loads the raw emergency dispatch dataset, validates and cleans it,
engineers a few time-based features, and writes a cleaned version
to data/processed/.

Run from the project root:
    python scripts/01_data_cleaning.py
"""

import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/emergency_service_routing_with_timestamps.csv")
OUT_PATH = Path("data/processed/ems_cleaned.csv")


def load_raw(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded {len(df):,} rows, {df.shape[1]} columns from {path}")
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # --- Duplicates ---
    n_dupes = df.duplicated().sum()
    if n_dupes:
        df = df.drop_duplicates()
    print(f"Dropped {n_dupes:,} duplicate rows")

    # --- Timestamps ---
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df["Year"] = df["Timestamp"].dt.year
    df["Month"] = df["Timestamp"].dt.month
    df["Month_Name"] = df["Timestamp"].dt.strftime("%b")
    df["DayOfWeek"] = df["Timestamp"].dt.day_name()
    df["Hour"] = df["Timestamp"].dt.hour

    # Shift buckets, useful for staffing/apparatus-utilization style analysis
    def shift_bucket(hour):
        if 6 <= hour < 14:
            return "Day (06:00-14:00)"
        elif 14 <= hour < 22:
            return "Evening (14:00-22:00)"
        else:
            return "Overnight (22:00-06:00)"

    df["Shift"] = df["Hour"].apply(shift_bucket)

    # --- Missing values ---
    # Weather_Impact is null exactly when Weather_Condition == 'Clear'
    # (verified during EDA) -> that's not "missing data", it's "no impact".
    # Encode it explicitly instead of dropping or imputing blindly.
    before_na = df["Weather_Impact"].isna().sum()
    df["Weather_Impact"] = df["Weather_Impact"].fillna("None")
    print(f"Filled {before_na:,} Weather_Impact nulls with 'None' "
          f"(all occur when Weather_Condition == 'Clear')")

    remaining_na = df.isna().sum()
    remaining_na = remaining_na[remaining_na > 0]
    if len(remaining_na):
        print("Remaining nulls by column:\n", remaining_na)
    else:
        print("No remaining nulls in any column.")

    # --- Range sanity checks ---
    assert df["Response_Time"].between(0, 120).all(), "Response_Time out of expected range"
    assert df["Number_of_Injuries"].ge(0).all(), "Negative injury count found"

    # --- Category dtype (saves memory, makes grouping faster) ---
    cat_cols = [
        "Incident_Severity", "Incident_Type", "Region_Type", "Traffic_Congestion",
        "Weather_Condition", "Drone_Availability", "Ambulance_Availability",
        "Air_Traffic", "Specialist_Availability", "Road_Type", "Emergency_Level",
        "Weather_Impact", "Dispatch_Coordinator", "Label", "DayOfWeek",
        "Month_Name", "Shift",
    ]
    for c in cat_cols:
        df[c] = df[c].astype("category")

    return df


def main():
    df = load_raw(RAW_PATH)
    df_clean = clean(df)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(OUT_PATH, index=False)
    print(f"\nSaved cleaned dataset -> {OUT_PATH} ({len(df_clean):,} rows)")

    # Small sample for quick inspection / repo demo (full file is too large for git)
    sample_path = Path("data/processed/ems_cleaned_sample.csv")
    df_clean.sample(5000, random_state=42).to_csv(sample_path, index=False)
    print(f"Saved 5,000-row sample -> {sample_path}")


if __name__ == "__main__":
    main()
