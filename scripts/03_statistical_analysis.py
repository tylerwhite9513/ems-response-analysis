"""
03_statistical_analysis.py
----------------------------
Applies inferential statistics to test whether observed differences
in response time are statistically significant, not just visual.

Tests:
  1. Independent t-test: AI vs Human dispatch coordinator response times
  2. One-way ANOVA: Response time across Region_Type (Urban/Suburban/Rural)
  3. One-way ANOVA: Response time across Incident_Type
  4. Pearson correlation: Distance_to_Incident vs Response_Time
  5. Pearson correlation: Traffic_Congestion (ordinal-encoded) vs Response_Time
  6. Chi-square test: Region_Type independence from dispatch Label

Run from the project root:
    python scripts/03_statistical_analysis.py
"""

import pandas as pd
from scipy import stats
from pathlib import Path

DATA_PATH = Path("data/processed/ems_cleaned.csv")
OUT_PATH = Path("reports/statistical_analysis.md")


def fmt_p(p):
    return "< 0.001" if p < 0.001 else f"{p:.4f}"


def main():
    df = pd.read_csv(DATA_PATH)
    lines = ["# Statistical Analysis\n",
             "All tests use alpha = 0.05. Response times are in minutes.\n"]

    # 1. AI vs Human t-test
    ai = df.loc[df["Dispatch_Coordinator"] == "AI", "Response_Time"]
    human = df.loc[df["Dispatch_Coordinator"] == "Human", "Response_Time"]
    t_stat, p_val = stats.ttest_ind(ai, human, equal_var=False)
    lines.append("## 1. AI vs Human Dispatch Coordinator (Independent t-test)\n")
    lines.append(f"- AI mean response time: {ai.mean():.3f} min (n={len(ai):,})\n"
                  f"- Human mean response time: {human.mean():.3f} min (n={len(human):,})\n"
                  f"- t-statistic: {t_stat:.3f}, p-value: {fmt_p(p_val)}\n"
                  f"- **Conclusion:** {'Statistically significant difference' if p_val < 0.05 else 'No statistically significant difference'} "
                  f"between AI and human dispatch coordinator response times.\n")

    # 2. ANOVA across Region_Type
    groups = [g["Response_Time"].values for _, g in df.groupby("Region_Type", observed=True)]
    f_stat, p_val = stats.f_oneway(*groups)
    lines.append("## 2. Response Time Across Region Type (One-way ANOVA)\n")
    lines.append(f"- F-statistic: {f_stat:.3f}, p-value: {fmt_p(p_val)}\n"
                  f"- **Conclusion:** {'Statistically significant' if p_val < 0.05 else 'No statistically significant'} "
                  f"difference in response time across Urban/Suburban/Rural regions in this dataset.\n")

    # 3. ANOVA across Incident_Type
    groups = [g["Response_Time"].values for _, g in df.groupby("Incident_Type", observed=True)]
    f_stat, p_val = stats.f_oneway(*groups)
    lines.append("## 3. Response Time Across Incident Type (One-way ANOVA)\n")
    lines.append(f"- F-statistic: {f_stat:.3f}, p-value: {fmt_p(p_val)}\n"
                  f"- **Conclusion:** {'Statistically significant' if p_val < 0.05 else 'No statistically significant'} "
                  f"difference in response time across incident types.\n")

    # 4. Correlation: Distance vs Response Time
    r, p_val = stats.pearsonr(df["Distance_to_Incident"], df["Response_Time"])
    lines.append("## 4. Distance to Incident vs Response Time (Pearson correlation)\n")
    lines.append(f"- r = {r:.3f}, p-value: {fmt_p(p_val)}\n"
                  f"- **Conclusion:** {'A statistically significant' if p_val < 0.05 else 'No statistically significant'} "
                  f"{'positive' if r > 0 else 'negative'} linear relationship "
                  f"({'weak' if abs(r) < 0.3 else 'moderate' if abs(r) < 0.6 else 'strong'} in strength).\n")

    # 5. Correlation: Traffic Congestion (ordinal) vs Response Time
    traffic_map = {"Low": 0, "Moderate": 1, "High": 2}
    traffic_num = df["Traffic_Congestion"].map(traffic_map)
    r, p_val = stats.pearsonr(traffic_num, df["Response_Time"])
    lines.append("## 5. Traffic Congestion vs Response Time (Pearson correlation, ordinal-encoded)\n")
    lines.append(f"- r = {r:.3f}, p-value: {fmt_p(p_val)}\n"
                  f"- **Conclusion:** {'A statistically significant' if p_val < 0.05 else 'No statistically significant'} "
                  f"{'positive' if r > 0 else 'negative'} relationship between traffic congestion level and response time.\n")

    # 6. Chi-square: Region_Type vs Label independence
    contingency = pd.crosstab(df["Region_Type"], df["Label"])
    chi2, p_val, dof, expected = stats.chi2_contingency(contingency)
    lines.append("## 6. Region Type vs Dispatch Mode (Chi-square test of independence)\n")
    lines.append(f"- Chi-square statistic: {chi2:.3f}, degrees of freedom: {dof}, p-value: {fmt_p(p_val)}\n"
                  f"- **Conclusion:** {'Dispatch mode selection is significantly associated with region type' if p_val < 0.05 else 'Dispatch mode selection appears independent of region type'} "
                  f"in this dataset.\n")

    OUT_PATH.write_text("\n".join(lines))
    print(f"Saved -> {OUT_PATH}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
