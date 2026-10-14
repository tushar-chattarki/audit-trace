# AuditTrail AI

Automated financial statement anomaly & fraud signal detector for small accounting firms, auditors-in-training, and finance students.

Small accounting firms and SMBs usually can't afford enterprise fraud-detection tooling. AuditTrail AI ingests a transaction ledger (CSV), runs it through classical forensic-accounting statistics and unsupervised machine learning, and returns an explainable, ranked list of anomalies plus a downloadable PDF audit report — in seconds.

## Features

- **CSV upload** — drag-and-drop a transaction ledger (auto-detects amount/date/description/account columns)
- **Benford's Law analysis** — chi-square goodness-of-fit test on leading-digit distribution, the classic forensic-accounting screen
- **Unsupervised anomaly detection** — Isolation Forest scores every transaction's "outlier-ness" without needing labeled fraud examples
- **Explainable flags** — a SHAP-explained surrogate classifier plus duplicate-posting and round-number-bias heuristics generate plain-English reasons for every flag
- **Downloadable audit report** — a formatted PDF summary suitable for handing to a reviewing partner or client
- **React dashboard** — Benford chart, risk-ranked transaction table, summary KPIs

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Python, FastAPI, Pandas, scikit-learn, SHAP, ReportLab |
| Frontend | React, Vite, Recharts |
| ML | Isolation Forest (unsupervised), RandomForest surrogate + SHAP (explainability), Benford's Law / duplicate / round-number heuristics |
| Deployment | Docker, Render |

## How the anomaly detection works

1. Engineer numeric features per transaction: amount, log-amount, z-score vs. dataset mean, calendar features, duplicate flag, round-number flag, amount frequency.
2. Fit an **Isolation Forest** — an unsupervised model that isolates outliers by how few random splits it takes to separate them from the rest of the data. No fraud labels needed, which matters because real-world fraud labels are almost never available to a small firm.
3. Isolation Forest isn't natively SHAP-explainable, so a small **RandomForestClassifier surrogate** is trained to reproduce the isolation forest's anomaly/normal labels. **SHAP's TreeExplainer** runs on that surrogate to produce faithful, per-transaction feature attributions — a standard "explain the black box with a white box" pattern.
4. Results are combined with **Benford's Law** deviation, **duplicate posting** detection, and **round-number bias** heuristics into a single 0–100 risk score with human-readable reasons.

## Project structure

```
AuditTrailAI/
├── backend/
│   ├── app/
│   │   ├── analysis/       # Benford's Law, Isolation Forest, heuristics, explainability
│   │   ├── report/         # PDF report generation
│   │   ├── utils/          # CSV parsing & column detection
│   │   └── main.py         # FastAPI app
│   ├── sample_data/        # Synthetic demo ledger generator
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/     # FileUpload, SummaryCards, BenfordChart, AnomalyTable, ReportDownload
│   │   └── App.jsx
│   └── package.json
├── docker-compose.yml
└── render.yaml
```

## Running locally

### Backend

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python sample_data/generate_sample.py   # optional: generate a demo CSV
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000` (interactive docs at `/docs`).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

### With Docker Compose

```bash
docker-compose up --build
```

## API

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Health check |
| `/api/analyze` | POST | Upload a CSV (`multipart/form-data`, field `file`), returns summary + Benford results + flagged transactions |
| `/api/report/{report_id}/pdf` | GET | Download the generated PDF audit report |

## Expected CSV format

At minimum, an amount column. Optional columns are auto-detected:

| Column | Aliases recognized |
|---|---|
| amount (required) | `amount`, `transaction_amount`, `value`, `debit`, `credit`, `amt`, `total` |
| date | `date`, `transaction_date`, `posted_date`, `txn_date`, `timestamp` |
| description | `description`, `memo`, `narrative`, `details`, `vendor`, `payee` |
| account | `account`, `account_id`, `account_number`, `acct`, `gl_account` |
| category | `category`, `type`, `transaction_type`, `class` |

A synthetic sample ledger is included at `backend/sample_data/sample_transactions.csv`.

## Disclaimer

This tool is a screening aid, not a conclusive fraud determination. Flagged transactions should always be reviewed by a qualified professional.
