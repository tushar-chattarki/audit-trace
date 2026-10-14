"""Turn raw model output into human-readable, per-transaction explanations."""
from __future__ import annotations

import numpy as np
import pandas as pd

from app.analysis.anomaly import FEATURE_NAMES
from app.analysis.benford import leading_digit
from app.analysis.heuristics import flag_duplicates, flag_round_numbers
from app.utils.parsing import ParsedLedger

FEATURE_LABELS = {
    "amount": "transaction amount",
    "abs_amount": "transaction size",
    "log_abs_amount": "transaction size (log-scaled)",
    "zscore_amount": "deviation from the dataset's average amount",
    "day_of_week": "day of week",
    "day_of_month": "day of month",
    "is_round_number": "round-number amount",
    "is_duplicate": "duplicate posting",
    "amount_frequency": "how often this exact amount recurs",
}


def _top_shap_reasons(shap_row: np.ndarray, feature_row: pd.Series, top_k: int = 3) -> list[str]:
    order = np.argsort(-np.abs(shap_row))[:top_k]
    reasons = []
    for idx in order:
        contribution = shap_row[idx]
        if contribution <= 0:
            continue
        name = FEATURE_NAMES[idx]
        label = FEATURE_LABELS.get(name, name)
        value = feature_row[name]
        reasons.append(f"{label} strongly influenced the anomaly score (value={value:.2f}, SHAP={contribution:.3f})")
    return reasons


def build_flagged_transactions(
    parsed: ParsedLedger,
    anomaly_result: dict,
    benford_result: dict,
    top_n: int = 200,
) -> list[dict]:
    df = parsed.df
    features = anomaly_result["features"]
    risk_score = anomaly_result["risk_score"]
    is_anomaly = anomaly_result["is_anomaly"]
    shap_values = anomaly_result["shap_values"]

    duplicates = flag_duplicates(parsed)
    round_numbers = flag_round_numbers(parsed)
    deviating_digits = set(benford_result.get("deviating_digits", [])) if benford_result.get("applicable") else set()

    records = []
    for i in df.index:
        reasons: list[str] = []
        row_is_anomaly = bool(is_anomaly[i])

        if shap_values is not None and row_is_anomaly:
            reasons.extend(_top_shap_reasons(shap_values[df.index.get_loc(i)], features.loc[i]))

        if bool(duplicates.loc[i]):
            reasons.append("Matches another transaction on amount/date/description — possible duplicate posting.")
        if bool(round_numbers.loc[i]):
            reasons.append("Suspiciously round amount (multiple of 100 or 1000) — common in fabricated entries.")

        amount = df.loc[i, parsed.amount_col]
        ld = leading_digit(amount)
        if ld in deviating_digits:
            reasons.append(
                f"Leading digit {ld} is over/under-represented dataset-wide relative to Benford's Law expectation."
            )

        z = features.loc[i, "zscore_amount"]
        if abs(z) >= 3:
            reasons.append(f"Amount is an extreme outlier ({z:+.1f} standard deviations from the mean).")

        if not row_is_anomaly and not reasons:
            continue

        record = {
            "row_index": int(i),
            "amount": float(amount),
            "risk_score": float(risk_score[df.index.get_loc(i)]),
            "is_model_anomaly": row_is_anomaly,
            "is_duplicate": bool(duplicates.loc[i]),
            "is_round_number": bool(round_numbers.loc[i]),
            "reasons": reasons or ["Flagged by heuristic checks."],
        }
        if parsed.date_col:
            val = df.loc[i, parsed.date_col]
            record["date"] = None if pd.isna(val) else str(val.date())
        if parsed.desc_col:
            record["description"] = str(df.loc[i, parsed.desc_col])
        if parsed.account_col:
            record["account"] = str(df.loc[i, parsed.account_col])
        if parsed.category_col:
            record["category"] = str(df.loc[i, parsed.category_col])

        records.append(record)

    records.sort(key=lambda r: r["risk_score"], reverse=True)
    return records[:top_n]
