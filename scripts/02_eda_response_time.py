"""
02_eda_response_time.py
------------------------
Exploratory analysis of response times, incident volumes, and
geographic (region-level) trends. Saves chart images to
reports/figures/ and a text summary to reports/eda_summary.md.

Run from the project root:
    python scripts/02_eda_response_time.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

DATA_PATH = Path("data/processed/ems_cleaned.csv")
FIG_DIR = Path("reports/figures")
SUMMARY_PATH = Path("reports/eda_summary.md")

sns.set_theme(style="whitegrid")
FIG_DIR.mkdir(parents=True, exist_ok=True)

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def savefig(fig, name):
    path = FIG_DIR / name
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  saved {path}")


def main():
    df = pd.read_csv(DATA_PATH, parse_dates=["Timestamp"])
    lines = []
    lines.append("# Exploratory Data Analysis Summary\n")
    lines.append(f"Dataset: {len(df):,} dispatch records, "
                  f"{df['Timestamp'].min().date()} to {df['Timestamp'].max().date()}\n")

    # ---------- 1. Overall response time distribution ----------
    print("Chart 1: response time distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["Response_Time"], bins=40, kde=True, ax=ax)
    ax.set_title("Distribution of Response Times")
    ax.set_xlabel("Response Time (minutes)")
    savefig(fig, "01_response_time_distribution.png")

    rt = df["Response_Time"]
    lines.append("## Response Time Overview\n")
    lines.append(f"- Mean: {rt.mean():.2f} min\n- Median: {rt.median():.2f} min\n"
                  f"- 90th percentile: {rt.quantile(0.90):.2f} min\n"
                  f"- 95th percentile: {rt.quantile(0.95):.2f} min\n"
                  f"- Std dev: {rt.std():.2f} min\n")

    # ---------- 2. Response time by region (geographic trend) ----------
    print("Chart 2: response time by region")
    fig, ax = plt.subplots(figsize=(7, 5))
    order = df.groupby("Region_Type", observed=True)["Response_Time"].median().sort_values().index
    sns.boxplot(data=df, x="Region_Type", y="Response_Time", order=order, ax=ax)
    ax.set_title("Response Time by Region Type")
    ax.set_ylabel("Response Time (minutes)")
    savefig(fig, "02_response_time_by_region.png")

    region_stats = df.groupby("Region_Type", observed=True)["Response_Time"].agg(
        ["count", "mean", "median"]).round(2).sort_values("median")
    lines.append("## Response Time by Region\n")
    lines.append(region_stats.to_markdown() + "\n")

    # ---------- 3. Response time by incident type & severity ----------
    print("Chart 3: response time by incident type")
    fig, ax = plt.subplots(figsize=(8, 5))
    order = df.groupby("Incident_Type", observed=True)["Response_Time"].median().sort_values().index
    sns.boxplot(data=df, x="Incident_Type", y="Response_Time", order=order, ax=ax)
    ax.set_title("Response Time by Incident Type")
    ax.set_ylabel("Response Time (minutes)")
    savefig(fig, "03_response_time_by_incident_type.png")

    # ---------- 4. Incident volume over time (monthly trend) ----------
    print("Chart 4: monthly incident volume trend")
    monthly = df.set_index("Timestamp").resample("ME").size()
    fig, ax = plt.subplots(figsize=(11, 5))
    monthly.plot(ax=ax)
    ax.set_title("Monthly Incident Volume, 2018-2024")
    ax.set_ylabel("Number of Incidents")
    ax.set_xlabel("Month")
    savefig(fig, "04_monthly_incident_volume.png")

    # ---------- 5. Incident volume by hour of day (staffing pattern) ----------
    print("Chart 5: incident volume by hour")
    hourly = df.groupby("Hour", observed=True).size()
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(x=hourly.index, y=hourly.values, ax=ax, color="steelblue")
    ax.set_title("Incident Volume by Hour of Day")
    ax.set_xlabel("Hour (24h)")
    ax.set_ylabel("Number of Incidents")
    savefig(fig, "05_incidents_by_hour.png")

    # ---------- 6. Incident volume by day of week ----------
    print("Chart 6: incident volume by day of week")
    dow = df.groupby("DayOfWeek", observed=True).size().reindex(DAY_ORDER)
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(x=dow.index, y=dow.values, ax=ax, color="darkorange")
    ax.set_title("Incident Volume by Day of Week")
    ax.set_ylabel("Number of Incidents")
    plt.xticks(rotation=30)
    savefig(fig, "06_incidents_by_dayofweek.png")

    # ---------- 7. Dispatch mode mix by region (geographic + operational) ----------
    print("Chart 7: dispatch mode mix by region")
    mix = pd.crosstab(df["Region_Type"], df["Label"], normalize="index") * 100
    fig, ax = plt.subplots(figsize=(8, 5))
    mix.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
    ax.set_title("Dispatch Mode Mix by Region Type")
    ax.set_ylabel("% of Incidents")
    ax.legend(title="Dispatch Mode", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.xticks(rotation=0)
    savefig(fig, "07_dispatch_mode_by_region.png")

    # ---------- 8. AI vs Human dispatch coordinator ----------
    print("Chart 8: response time by dispatch coordinator")
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(data=df, x="Dispatch_Coordinator", y="Response_Time", ax=ax)
    ax.set_title("Response Time: AI vs Human Dispatch Coordinator")
    ax.set_ylabel("Response Time (minutes)")
    savefig(fig, "08_response_time_ai_vs_human.png")

    coord_stats = df.groupby("Dispatch_Coordinator", observed=True)["Response_Time"].agg(
        ["count", "mean", "median"]).round(2)
    lines.append("## Response Time: AI vs Human Dispatch Coordinator\n")
    lines.append(coord_stats.to_markdown() + "\n")

    # ---------- 9. Apparatus/resource availability impact ----------
    print("Chart 9: response time by traffic congestion")
    fig, ax = plt.subplots(figsize=(7, 5))
    order = ["Low", "Moderate", "High"]
    sns.boxplot(data=df, x="Traffic_Congestion", y="Response_Time", order=order, ax=ax)
    ax.set_title("Response Time by Traffic Congestion Level")
    ax.set_ylabel("Response Time (minutes)")
    savefig(fig, "09_response_time_by_traffic.png")

    SUMMARY_PATH.write_text("\n".join(lines))
    print(f"\nSaved summary -> {SUMMARY_PATH}")
    print("All figures saved to reports/figures/")


if __name__ == "__main__":
    main()
