"""Classical audit heuristics: duplicate detection and round-number bias.

These are cheap, explainable checks that complement the statistical (Benford)
and ML-based (isolation forest) signals.
"""
from __future__ import annotations

import pandas as pd

from app.utils.parsing import ParsedLedger


def flag_duplicates(parsed: ParsedLedger) -> pd.Series:
    """Rows that share the same amount (+ date/description if available) as
    another row are flagged as potential duplicate postings."""
    df = parsed.df
    key_cols = [parsed.amount_col]
    if parsed.date_col:
        key_cols.append(parsed.date_col)
    if parsed.desc_col:
        key_cols.append(parsed.desc_col)

    group_sizes = df.groupby(key_cols)[parsed.amount_col].transform("size")
    return group_sizes > 1


def flag_round_numbers(parsed: ParsedLedger) -> pd.Series:
    """Amounts that are suspiciously 'round' (multiples of 100/1000) occur far
    more often in fabricated figures than genuine, itemized transactions."""
    amounts = parsed.df[parsed.amount_col].abs()
    is_nonzero = amounts > 0
    is_round_100 = (amounts % 100 == 0) & is_nonzero
    is_round_1000 = (amounts % 1000 == 0) & is_nonzero
    return is_round_100 | is_round_1000


def round_number_rate(parsed: ParsedLedger) -> float:
    flags = flag_round_numbers(parsed)
    return float(flags.mean()) if len(flags) else 0.0
