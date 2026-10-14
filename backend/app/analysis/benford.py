"""Benford's Law first-digit analysis, a classic forensic-accounting test.

Naturally occurring transaction amounts follow a logarithmic distribution of
leading digits (digit 1 appears ~30.1% of the time, digit 9 only ~4.6%).
Fabricated or manipulated figures tend to deviate from this distribution,
which is why auditors use it as a first-pass screen.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import stats

BENFORD_EXPECTED = {d: math.log10(1 + 1 / d) for d in range(1, 10)}


def leading_digit(value: float) -> int | None:
    value = abs(value)
    if value == 0 or not math.isfinite(value):
        return None
    while value < 1:
        value *= 10
    while value >= 10:
        value /= 10
    return int(value)


def analyze_benford(amounts: pd.Series) -> dict:
    digits = amounts.map(leading_digit).dropna().astype(int)
    n = len(digits)
    if n < 10:
        return {
            "applicable": False,
            "reason": "Not enough non-zero transactions (need >= 10) for a reliable Benford's Law test.",
            "n": n,
        }

    observed_counts = digits.value_counts().reindex(range(1, 10), fill_value=0).sort_index()
    observed_pct = (observed_counts / n * 100).round(2)
    expected_pct = pd.Series({d: round(p * 100, 2) for d, p in BENFORD_EXPECTED.items()})

    expected_counts = np.array([BENFORD_EXPECTED[d] * n for d in range(1, 10)])
    chi_sq, p_value = stats.chisquare(f_obs=observed_counts.values, f_exp=expected_counts)

    # Mean Absolute Deviation is a scale-free measure commonly used alongside chi-square.
    mad = float(np.mean(np.abs(observed_pct.values / 100 - np.array(list(BENFORD_EXPECTED.values())))))
    if mad < 0.006:
        conformity = "Close conformity"
    elif mad < 0.012:
        conformity = "Acceptable conformity"
    elif mad < 0.015:
        conformity = "Marginally acceptable conformity"
    else:
        conformity = "Nonconformity"

    per_digit = []
    deviating_digits = []
    for d in range(1, 10):
        obs = float(observed_pct[d])
        exp = float(expected_pct[d])
        diff = round(obs - exp, 2)
        per_digit.append({"digit": d, "observed_pct": obs, "expected_pct": exp, "diff_pct": diff})
        if abs(diff) >= 5:
            deviating_digits.append(d)

    return {
        "applicable": True,
        "n": int(n),
        "chi_square": round(float(chi_sq), 3),
        "p_value": round(float(p_value), 5),
        "significant": bool(p_value < 0.05),
        "mean_absolute_deviation": round(mad, 5),
        "conformity": conformity,
        "per_digit": per_digit,
        "deviating_digits": deviating_digits,
        "summary": (
            f"Chi-square={chi_sq:.2f}, p={p_value:.4f} "
            f"({'deviates significantly from' if p_value < 0.05 else 'is consistent with'} Benford's Law); "
            f"{conformity} (MAD={mad:.4f})."
        ),
    }
