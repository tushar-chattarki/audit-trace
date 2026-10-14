"""Unsupervised anomaly detection with SHAP-based explainability.

Approach
--------
1. Engineer numeric features per transaction (amount, log-amount, z-score,
   calendar features, round-number/duplicate flags).
2. Fit an IsolationForest (unsupervised) to score each transaction's
   "outlier-ness" -- this needs no labels, which matters because real fraud
   labels are almost never available to a small firm.
3. IsolationForest itself isn't easily SHAP-explainable, so we train a small
   surrogate RandomForestClassifier to reproduce the isolation forest's
   flagged/not-flagged labels, then run shap.TreeExplainer on the surrogate.
   This "explain the black box with a white box" pattern is a standard,
   well-documented way to get faithful, per-transaction SHAP explanations for
   a model family SHAP doesn't support natively.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import shap
from sklearn.ensemble import IsolationForest, RandomForestClassifier

from app.analysis.heuristics import flag_duplicates, flag_round_numbers
from app.utils.parsing import ParsedLedger

FEATURE_NAMES = [
    "amount",
    "abs_amount",
    "log_abs_amount",
    "zscore_amount",
    "day_of_week",
    "day_of_month",
    "is_round_number",
    "is_duplicate",
    "amount_frequency",
]


def build_features(parsed: ParsedLedger) -> pd.DataFrame:
    df = parsed.df
    amounts = df[parsed.amount_col].astype(float)

    feat = pd.DataFrame(index=df.index)
    feat["amount"] = amounts
    feat["abs_amount"] = amounts.abs()
    feat["log_abs_amount"] = np.log1p(feat["abs_amount"])

    std = amounts.std(ddof=0)
    mean = amounts.mean()
    feat["zscore_amount"] = 0.0 if std == 0 or np.isnan(std) else (amounts - mean) / std

    if parsed.date_col:
        dt = df[parsed.date_col]
        feat["day_of_week"] = dt.dt.dayofweek.fillna(-1)
        feat["day_of_month"] = dt.dt.day.fillna(-1)
    else:
        feat["day_of_week"] = -1
        feat["day_of_month"] = -1

    feat["is_round_number"] = flag_round_numbers(parsed).astype(int)
    feat["is_duplicate"] = flag_duplicates(parsed).astype(int)

    freq = amounts.round(2).map(amounts.round(2).value_counts())
    feat["amount_frequency"] = freq

    return feat[FEATURE_NAMES].fillna(0.0)


def detect_anomalies(parsed: ParsedLedger, contamination: float = 0.07) -> dict:
    features = build_features(parsed)
    n = len(features)

    contamination = min(max(contamination, 0.01), 0.3)
    iso = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=42,
        max_samples="auto",
    )
    iso.fit(features)

    raw_scores = iso.decision_function(features)  # higher = more normal
    predictions = iso.predict(features)  # -1 anomaly, 1 normal
    is_anomaly = predictions == -1

    # Normalize the raw isolation score to an intuitive 0-100 risk score.
    score_min, score_max = raw_scores.min(), raw_scores.max()
    span = (score_max - score_min) or 1.0
    risk_score = ((score_max - raw_scores) / span * 100).round(1)

    shap_values = None
    surrogate_used = False
    if is_anomaly.sum() > 0 and is_anomaly.sum() < n:
        try:
            surrogate = RandomForestClassifier(
                n_estimators=150, random_state=42, max_depth=8, class_weight="balanced"
            )
            surrogate.fit(features, is_anomaly.astype(int))
            explainer = shap.TreeExplainer(surrogate)
            raw_shap = explainer.shap_values(features)
            # shap returns a list per class for classifiers; take the "anomaly" class (index 1).
            if isinstance(raw_shap, list):
                shap_values = raw_shap[1] if len(raw_shap) > 1 else raw_shap[0]
            else:
                shap_values = raw_shap[:, :, 1] if raw_shap.ndim == 3 else raw_shap
            surrogate_used = True
        except Exception:  # noqa: BLE001
            shap_values = None

    return {
        "features": features,
        "risk_score": risk_score,
        "is_anomaly": is_anomaly,
        "shap_values": shap_values,
        "surrogate_used": surrogate_used,
        "contamination": contamination,
    }
