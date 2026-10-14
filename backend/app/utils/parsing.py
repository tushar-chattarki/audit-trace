"""CSV ingestion and column normalization for ledger uploads."""
from __future__ import annotations

import io
from dataclasses import dataclass

import pandas as pd

AMOUNT_ALIASES = ["amount", "transaction_amount", "value", "debit", "credit", "amt", "total"]
DATE_ALIASES = ["date", "transaction_date", "posted_date", "txn_date", "timestamp"]
DESC_ALIASES = ["description", "memo", "narrative", "details", "vendor", "payee", "particulars"]
ACCOUNT_ALIASES = ["account", "account_id", "account_number", "acct", "gl_account"]
CATEGORY_ALIASES = ["category", "type", "transaction_type", "class"]


class LedgerParseError(ValueError):
    pass


def _find_column(columns: list[str], aliases: list[str]) -> str | None:
    lowered = {c.lower().strip(): c for c in columns}
    for alias in aliases:
        if alias in lowered:
            return lowered[alias]
    for alias in aliases:
        for lc, original in lowered.items():
            if alias in lc:
                return original
    return None


@dataclass
class ParsedLedger:
    df: pd.DataFrame
    amount_col: str
    date_col: str | None
    desc_col: str | None
    account_col: str | None
    category_col: str | None


def parse_ledger_csv(file_bytes: bytes, filename: str = "upload.csv") -> ParsedLedger:
    if not file_bytes:
        raise LedgerParseError("Uploaded file is empty.")
    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
    except Exception as exc:  # noqa: BLE001
        raise LedgerParseError(f"Could not parse '{filename}' as CSV: {exc}") from exc

    if df.empty:
        raise LedgerParseError("The CSV has no rows.")

    df.columns = [str(c).strip() for c in df.columns]
    columns = list(df.columns)

    amount_col = _find_column(columns, AMOUNT_ALIASES)
    if amount_col is None:
        raise LedgerParseError(
            "Could not find an amount column. Expected one of: "
            + ", ".join(AMOUNT_ALIASES)
        )

    df[amount_col] = (
        df[amount_col]
        .astype(str)
        .str.replace(r"[,$\s]", "", regex=True)
        .str.replace(r"^\((.*)\)$", r"-\1", regex=True)
    )
    df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")
    before = len(df)
    df = df.dropna(subset=[amount_col]).reset_index(drop=True)
    dropped = before - len(df)

    if df.empty:
        raise LedgerParseError("No rows had a valid numeric amount.")

    date_col = _find_column(columns, DATE_ALIASES)
    if date_col:
        parsed_dates = pd.to_datetime(df[date_col], errors="coerce", infer_datetime_format=True)
        if parsed_dates.notna().sum() == 0:
            date_col = None
        else:
            df[date_col] = parsed_dates

    desc_col = _find_column(columns, DESC_ALIASES)
    account_col = _find_column(columns, ACCOUNT_ALIASES)
    category_col = _find_column(columns, CATEGORY_ALIASES)

    df.attrs["dropped_rows"] = dropped
    return ParsedLedger(
        df=df,
        amount_col=amount_col,
        date_col=date_col,
        desc_col=desc_col,
        account_col=account_col,
        category_col=category_col,
    )
