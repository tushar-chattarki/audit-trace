"""Generates a synthetic ledger CSV with a mix of normal and anomalous
transactions, for demoing AuditTrail AI. Run: python generate_sample.py
"""
from __future__ import annotations

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

random.seed(7)
np.random.seed(7)

VENDORS = [
    "Office Depot", "AWS", "Delta Airlines", "Uber", "Staples",
    "Google Workspace", "Regional Utility Co", "City Water Dept",
    "Marriott Hotels", "FedEx", "Slack", "Adobe", "Zoom", "LinkedIn Ads",
]
ACCOUNTS = ["1000-OPEX", "2000-TRAVEL", "3000-MARKETING", "4000-UTILITIES", "5000-PAYROLL"]
CATEGORIES = ["Expense", "Payroll", "Utilities", "Travel", "Marketing"]

start = datetime(2025, 1, 1)
rows = []

# Benford-conforming "normal" population: log-uniform amounts.
n_normal = 950
for _ in range(n_normal):
    amount = round(float(np.exp(np.random.uniform(np.log(5), np.log(9000)))), 2)
    date = start + timedelta(days=random.randint(0, 240))
    rows.append(
        {
            "date": date.strftime("%Y-%m-%d"),
            "description": random.choice(VENDORS),
            "amount": amount,
            "account": random.choice(ACCOUNTS),
            "category": random.choice(CATEGORIES),
        }
    )

# Round-number bias anomalies (common in fabricated entries).
for _ in range(25):
    date = start + timedelta(days=random.randint(0, 240))
    rows.append(
        {
            "date": date.strftime("%Y-%m-%d"),
            "description": random.choice(VENDORS),
            "amount": float(random.choice([500, 1000, 1500, 2000, 5000, 10000])),
            "account": random.choice(ACCOUNTS),
            "category": random.choice(CATEGORIES),
        }
    )

# Duplicate postings.
dup_base = rows[:15]
for r in dup_base:
    rows.append(dict(r))

# Extreme outliers.
for _ in range(10):
    date = start + timedelta(days=random.randint(0, 240))
    rows.append(
        {
            "date": date.strftime("%Y-%m-%d"),
            "description": random.choice(VENDORS),
            "amount": round(float(np.random.uniform(45000, 120000)), 2),
            "account": random.choice(ACCOUNTS),
            "category": random.choice(CATEGORIES),
        }
    )

df = pd.DataFrame(rows).sample(frac=1, random_state=7).reset_index(drop=True)
df.to_csv("sample_transactions.csv", index=False)
print(f"Wrote {len(df)} rows to sample_transactions.csv")
