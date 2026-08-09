# Predictive Model: Dispatch Mode Classification

**Goal:** predict which dispatch mode (Drone Only / Ambulance Only / Hybrid Dispatch) should be used for an incoming incident, based on incident and operational conditions known at dispatch time.

**Why not Response_Time:** statistical testing (see `statistical_analysis.md`) found no significant relationship between Response_Time and any available feature, so it isn't a usable modeling target in this dataset. Predicting dispatch mode is both statistically viable and operationally realistic.

## Model: Random Forest Classifier

- Train rows: 294,452, Test rows: 73,613

- Overall accuracy: 0.499

```
                 precision    recall  f1-score   support

 Ambulance Only      0.474     0.001     0.003     29505
     Drone Only      0.499     0.999     0.666     36738
Hybrid Dispatch      0.000     0.000     0.000      7370

       accuracy                          0.499     73613
      macro avg      0.324     0.333     0.223     73613
   weighted avg      0.439     0.499     0.333     73613

```

**Baseline (always predict the majority class):** 0.499 accuracy. The model beats this baseline by 0.000.

## Top Predictive Features

|                      |     0 |
|:---------------------|------:|
| Fuel_Level           | 0.214 |
| Distance_to_Incident | 0.212 |
| Hospital_Capacity    | 0.15  |
| Incident_Type        | 0.045 |
| Number_of_Injuries   | 0.041 |
| Air_Traffic          | 0.038 |
| Incident_Severity    | 0.037 |
| Traffic_Congestion   | 0.036 |
