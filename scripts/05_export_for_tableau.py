"""
05_export_for_tableau.py
--------------------------
Builds small, dashboard-ready aggregated tables from the cleaned
dataset and writes them to data/tableau/. Aggregating here (rather
than pointing Tableau at the 368k-row raw file) keeps the dashboard
fast and keeps files small enough to comfortably commit to GitHub.

Run from the project root:
    python scripts/05_export_for_tableau.py
"""

import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/processed/ems_cleaned.csv")
OUT_DIR = Path("data/tableau")


def main():
    df = pd.read_csv(DATA_PATH, parse_dates=["Timestamp"])
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Monthly trend, split by region and incident type
    monthly = (
        df.assign(YearMonth=df["Timestamp"].dt.to_period("M").astype(str))
        .groupby(["YearMonth", "Region_Type", "Incident_Type"], observed=True)
        .agg(Incident_Count=("Response_Time", "size"),
             Avg_Response_Time=("Response_Time", "mean"))
        .reset_index()
    )
    monthly.to_csv(OUT_DIR / "monthly_trends.csv", index=False)

    # 2. Region-level summary
    region_summary = (
        df.groupby("Region_Type", observed=True)
        .agg(Incident_Count=("Response_Time", "size"),
             Avg_Response_Time=("Response_Time", "mean"),
             Median_Response_Time=("Response_Time", "median"),
             P90_Response_Time=("Response_Time", lambda x: x.quantile(0.9)))
        .reset_index()
    )
    region_summary.to_csv(OUT_DIR / "region_summary.csv", index=False)

    # 3. Hour-of-day x day-of-week incident volume (staffing heatmap source)
    heatmap = (
        df.groupby(["DayOfWeek", "Hour"], observed=True)
        .size().reset_index(name="Incident_Count")
    )
    heatmap.to_csv(OUT_DIR / "hour_dow_heatmap.csv", index=False)

    # 4. Dispatch mode summary by region and incident type
    dispatch_mix = (
        df.groupby(["Region_Type", "Incident_Type", "Label"], observed=True)
        .size().reset_index(name="Incident_Count")
    )
    dispatch_mix.to_csv(OUT_DIR / "dispatch_mode_mix.csv", index=False)

    # 5. AI vs Human coordinator comparison
    coordinator = (
        df.groupby(["Dispatch_Coordinator", "Region_Type"], observed=True)
        .agg(Incident_Count=("Response_Time", "size"),
             Avg_Response_Time=("Response_Time", "mean"))
        .reset_index()
    )
    coordinator.to_csv(OUT_DIR / "coordinator_summary.csv", index=False)

    print("Tableau-ready tables written to data/tableau/:")
    for f in sorted(OUT_DIR.glob("*.csv")):
        print(f"  {f.name}  ({f.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
