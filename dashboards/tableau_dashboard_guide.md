# Tableau Public Dashboard Build Guide

This guide walks through building an executive dashboard from the files in
`data/tableau/` using Tableau Public. This mirrors the "ongoing reports and
dashboards" and "translating complex data into actionable insights" duties
in the job posting.

## 1. Connect your data

1. Open Tableau Public → **Connect > Text File**.
2. Navigate to `data/tableau/` and open `monthly_trends.csv`.
3. Use **Data > New Data Source** to also add `region_summary.csv`,
   `hour_dow_heatmap.csv`, `dispatch_mode_mix.csv`, and `coordinator_summary.csv`.
   (Each is small and purpose-built for one chart, so there's no need to
   join them into one giant table.)

## 2. Build these four sheets

**Sheet 1 — Incident Volume Trend**
- Source: `monthly_trends.csv`
- Columns: `YearMonth` → Rows: `SUM(Incident_Count)`
- Color by `Region_Type`. Chart type: line.
- This is your "how has volume changed over time" view.

**Sheet 2 — Response Time by Region**
- Source: `region_summary.csv`
- Columns: `Region_Type` → Rows: `Avg_Response_Time`, `P90_Response_Time`
- Chart type: bar. Add both fields as separate bars (dual axis or side-by-side)
  so viewers can see the average *and* the 90th-percentile tail.

**Sheet 3 — Incident Volume Heatmap (Staffing View)**
- Source: `hour_dow_heatmap.csv`
- Columns: `Hour` → Rows: `DayOfWeek` → Color: `SUM(Incident_Count)`
- Chart type: heatmap (highlight table). This is the "when do we need more
  staff on shift" view.

**Sheet 4 — Dispatch Mode Mix**
- Source: `dispatch_mode_mix.csv`
- Columns: `Region_Type` → Rows: `SUM(Incident_Count)` → Color: `Label`
- Chart type: 100% stacked bar.

## 3. Assemble the dashboard

1. **Dashboard > New Dashboard**, size "Automatic" or a fixed 1200x800.
2. Drag all four sheets onto the canvas (2x2 grid works well).
3. Add a title: *"Brunswick County EMS Dispatch Performance Dashboard"*.
4. Add a filter action: right-click `Region_Type` on Sheet 2 → **Use as Filter**,
   so clicking a region filters the other three sheets.
5. Add a text box at the bottom noting the data-quality caveat: response
   time showed no statistically significant relationship with operational
   factors in this dataset (see `reports/statistical_analysis.md`) — worth
   surfacing on the dashboard itself, not just burying it in a report.

## 4. Publish and link back

1. **File > Save to Tableau Public As...**, sign in, save.
2. Copy the shareable link Tableau gives you.
3. Paste that link into `README.md` in the "Live Dashboard" section
   (there's a placeholder waiting for it) and into `reports/executive_summary.md`.
4. Take a screenshot of the finished dashboard and save it as
   `dashboards/dashboard_screenshot.png` — GitHub renders images inline,
   so this lets visitors see the dashboard without opening Tableau.
