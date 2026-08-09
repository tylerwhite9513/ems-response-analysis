# Executive Summary: EMS Dispatch Response Analysis

**Prepared for:** EM Fire Services Administrator
**Dataset:** 368,065 dispatch records, 2018–2024 (simulated ambulance/drone routing data)

## Headline Numbers

- **Median response time: 15.0 minutes** (mean 15.1 min)
- **90% of responses arrive within 21.4 minutes**; 95% within 23.3 minutes
- Dispatch volume is effectively flat month over month across the full
  7-year span — no seasonal spike was found in this dataset (see Data
  Quality Note below)

## What Moves Response Time — and What Doesn't

We tested six operational factors that are commonly assumed to affect
response time: region (urban/suburban/rural), incident type, distance to
incident, traffic congestion, and whether dispatch was coordinated by AI or
a human. **None showed a statistically significant effect** in this dataset
(all p-values > 0.05).

**Recommendation:** before this finding is used to justify any real
staffing or resource decision, it should be validated against actual
incident records. In a synthetic/simulated dataset like this one, a null
result usually means the field was generated independently of the others
rather than that operational factors genuinely don't matter — that
distinction has to be checked with real data before anyone acts on it.

## Dispatch Mode Selection

We also tested whether the choice between ambulance, drone, or hybrid
dispatch could be predicted from incident conditions (severity, distance,
weather, resource availability, etc.). A trained classification model
reached 49.9% accuracy — no better than guessing the most common category
every time. Directly checking whether drone dispatch tracked drone
availability confirmed the same pattern: it doesn't, in this dataset.

**Recommendation:** treat this as a data-quality checkpoint, not a modeling
failure. The pipeline built here (cleaning → EDA → statistical testing →
classification model → dashboard) is ready to run against real dispatch
records as soon as they're available, and will surface genuine drivers of
dispatch mode selection if the underlying data actually reflects real
decision rules.

## Data Quality Note

This dataset is synthetic and was not generated at real-world incident
timestamps — records occur at a fixed ~10-minute interval rather than
matching actual call volume. It also lacks incident-level location
(street address / lat-long), limiting geographic analysis to a coarse
Urban/Suburban/Rural category. Both limitations are disclosed here rather
than smoothed over, and both would resolve automatically once this
pipeline is pointed at real Brunswick County incident records (e.g. from
ImageTrend/NFIRS).

## Next Steps

1. Re-run this pipeline against real Brunswick County dispatch/incident data.
2. If a real geographic field is available, extend the region-level analysis
   to point-level incident mapping (ArcGIS or Tableau).
3. Revisit the dispatch-mode classification model once real decision
   patterns are available — this is where predictive analytics is most
   likely to add operational value.

*Full statistical detail: `statistical_analysis.md` and `predictive_model.md`
in this folder. All chart sources: `figures/`.*
