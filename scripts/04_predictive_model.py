"""
04_predictive_model.py
------------------------
Predictive analytics component (job posting preferred qualification:
"experience developing ... predictive analytics models").

Response_Time showed no significant relationship with any feature in
03_statistical_analysis.py, so it is not a viable modeling target here.
Instead, this builds a classifier to predict the dispatch decision
(Label: Drone Only / Ambulance Only / Hybrid Dispatch) from incident
and operational conditions -- a realistic decision-support use case
for a dispatch center.

Run from the project root:
    python scripts/04_predictive_model.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

DATA_PATH = Path("data/processed/ems_cleaned.csv")
FIG_DIR = Path("reports/figures")
OUT_PATH = Path("reports/predictive_model.md")

FEATURES = [
    "Incident_Severity", "Incident_Type", "Region_Type", "Traffic_Congestion",
    "Weather_Condition", "Drone_Availability", "Ambulance_Availability",
    "Air_Traffic", "Hospital_Capacity", "Distance_to_Incident",
    "Number_of_Injuries", "Specialist_Availability", "Road_Type",
    "Emergency_Level", "Fuel_Level", "Weather_Impact",
]
TARGET = "Label"


def main():
    df = pd.read_csv(DATA_PATH)
    lines = ["# Predictive Model: Dispatch Mode Classification\n"]
    lines.append(
        "**Goal:** predict which dispatch mode (Drone Only / Ambulance Only / "
        "Hybrid Dispatch) should be used for an incoming incident, based on "
        "incident and operational conditions known at dispatch time.\n"
    )
    lines.append(
        "**Why not Response_Time:** statistical testing (see "
        "`statistical_analysis.md`) found no significant relationship between "
        "Response_Time and any available feature, so it isn't a usable "
        "modeling target in this dataset. Predicting dispatch mode is both "
        "statistically viable and operationally realistic.\n"
    )

    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    encoders = {}
    for col in X.select_dtypes(include="object").columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        encoders[col] = le

    target_le = LabelEncoder()
    y_enc = target_le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
    )

    clf = RandomForestClassifier(
        n_estimators=200, max_depth=12, random_state=42, n_jobs=-1
    )
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    report = classification_report(
        y_test, y_pred, target_names=target_le.classes_, digits=3
    )

    lines.append("## Model: Random Forest Classifier\n")
    lines.append(f"- Train rows: {len(X_train):,}, Test rows: {len(X_test):,}\n")
    lines.append(f"- Overall accuracy: {acc:.3f}\n")
    lines.append("```\n" + report + "\n```\n")

    baseline = y.value_counts(normalize=True).max()
    lines.append(
        f"**Baseline (always predict the majority class):** {baseline:.3f} accuracy. "
        f"The model {'beats' if acc > baseline else 'does not beat'} this baseline "
        f"by {abs(acc - baseline):.3f}.\n"
    )

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=target_le.classes_, yticklabels=target_le.classes_, ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix: Dispatch Mode Prediction")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "10_confusion_matrix.png", dpi=150)
    plt.close(fig)

    # Feature importance
    importances = pd.Series(clf.feature_importances_, index=FEATURES).sort_values()
    fig, ax = plt.subplots(figsize=(8, 6))
    importances.plot(kind="barh", ax=ax, color="teal")
    ax.set_title("Feature Importance: Predicting Dispatch Mode")
    ax.set_xlabel("Importance")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "11_feature_importance.png", dpi=150)
    plt.close(fig)

    lines.append("## Top Predictive Features\n")
    lines.append(importances.sort_values(ascending=False).head(8).round(3).to_markdown() + "\n")

    OUT_PATH.write_text("\n".join(lines))
    print(f"Saved -> {OUT_PATH}")
    print(f"Accuracy: {acc:.3f} (baseline: {baseline:.3f})")
    print("Top features:\n", importances.sort_values(ascending=False).head(8))


if __name__ == "__main__":
    main()
