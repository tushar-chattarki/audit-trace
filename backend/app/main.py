from __future__ import annotations

import io
import os
import time
import uuid

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.analysis.anomaly import detect_anomalies
from app.analysis.benford import analyze_benford
from app.analysis.explain import build_flagged_transactions
from app.analysis.heuristics import round_number_rate
from app.report.pdf_report import generate_pdf_report
from app.utils.parsing import LedgerParseError, parse_ledger_csv

app = FastAPI(
    title="AuditTrail AI",
    description="Automated financial statement anomaly & fraud signal detector.",
    version="1.0.0",
)

allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allowed_origins == "*" else allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store of recent reports, keyed by report_id. Fine for a
# single-instance demo deployment; not intended for durable multi-user state.
_REPORT_STORE: dict[str, dict] = {}
_REPORT_TTL_SECONDS = 60 * 60
_MAX_UPLOAD_BYTES = 15 * 1024 * 1024


def _prune_report_store() -> None:
    cutoff = time.time() - _REPORT_TTL_SECONDS
    stale = [k for k, v in _REPORT_STORE.items() if v["created_at"] < cutoff]
    for k in stale:
        _REPORT_STORE.pop(k, None)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file.")

    raw = await file.read()
    if len(raw) > _MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File too large (max 15MB).")

    try:
        parsed = parse_ledger_csv(raw, filename=file.filename)
    except LedgerParseError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    benford_result = analyze_benford(parsed.df[parsed.amount_col])
    anomaly_result = detect_anomalies(parsed)
    flagged = build_flagged_transactions(parsed, anomaly_result, benford_result)

    n = len(parsed.df)
    n_flagged = len(flagged)
    n_model_anomalies = int(anomaly_result["is_anomaly"].sum())

    summary = {
        "Total transactions": n,
        "Rows dropped (invalid amount)": int(parsed.df.attrs.get("dropped_rows", 0)),
        "Flagged transactions": n_flagged,
        "Model-detected anomalies": n_model_anomalies,
        "Round-number rate": f"{round_number_rate(parsed) * 100:.1f}%",
        "Benford's Law conformity": benford_result.get("conformity", "N/A"),
        "Amount column detected": parsed.amount_col,
        "Date column detected": parsed.date_col or "none",
    }

    _prune_report_store()
    report_id = str(uuid.uuid4())
    _REPORT_STORE[report_id] = {
        "created_at": time.time(),
        "filename": file.filename,
        "summary": summary,
        "benford": benford_result,
        "flagged": flagged,
    }

    return {
        "report_id": report_id,
        "filename": file.filename,
        "summary": summary,
        "benford": benford_result,
        "flagged": flagged,
        "total_transactions": n,
    }


@app.get("/api/report/{report_id}/pdf")
def download_report(report_id: str):
    _prune_report_store()
    data = _REPORT_STORE.get(report_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Report not found or expired. Please re-run analysis.")

    pdf_bytes = generate_pdf_report(
        filename=data["filename"],
        summary=data["summary"],
        benford=data["benford"],
        flagged=data["flagged"],
    )
    headers = {"Content-Disposition": f'attachment; filename="audit_report_{report_id[:8]}.pdf"'}
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers=headers)
