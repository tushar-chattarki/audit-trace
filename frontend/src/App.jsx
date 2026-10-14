import { useState } from "react";
import FileUpload from "./components/FileUpload.jsx";
import SummaryCards from "./components/SummaryCards.jsx";
import BenfordChart from "./components/BenfordChart.jsx";
import AnomalyTable from "./components/AnomalyTable.jsx";
import ReportDownload from "./components/ReportDownload.jsx";
import { analyzeCsv } from "./api";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fileName, setFileName] = useState(null);

  async function handleFile(file) {
    setLoading(true);
    setError(null);
    setResult(null);
    setFileName(file.name);
    try {
      const data = await analyzeCsv(file);
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong analyzing the file.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header__brand">
          <span className="header__logo">🛡️</span>
          <div>
            <h1>AuditTrace AI</h1>
            <p className="header__tagline">Automated financial statement anomaly & fraud signal detector</p>
          </div>
        </div>
      </header>

      <main className="main">
        <section className="upload-section">
          <FileUpload onFileSelected={handleFile} disabled={loading} />
          {fileName && <p className="muted">Selected: {fileName}</p>}
          {loading && <p className="loading">Analyzing transactions…</p>}
          {error && <p className="error">⚠ {error}</p>}
        </section>

        {result && (
          <>
            <section className="toolbar">
              <ReportDownload reportId={result.report_id} filename={result.filename} />
            </section>

            <section>
              <SummaryCards summary={result.summary} />
            </section>

            <section className="grid-2">
              <BenfordChart benford={result.benford} />
              <div className="panel">
                <h3>How this works</h3>
                <ul className="how-list">
                  <li>
                    <strong>Benford's Law:</strong> checks whether leading digits of amounts follow the
                    naturally-expected logarithmic distribution.
                  </li>
                  <li>
                    <strong>Isolation Forest:</strong> an unsupervised ML model scores each transaction's
                    outlier-ness across engineered features (amount, z-score, calendar, duplicates).
                  </li>
                  <li>
                    <strong>SHAP explainability:</strong> a surrogate classifier trained on the isolation
                    forest's flags is explained with SHAP to surface which features drove each flag.
                  </li>
                  <li>
                    <strong>Heuristics:</strong> duplicate postings and round-number bias are checked
                    directly, the way a human auditor would.
                  </li>
                </ul>
              </div>
            </section>

            <section>
              <AnomalyTable flagged={result.flagged} />
            </section>
          </>
        )}

        {!result && !loading && (
          <section className="empty-state">
            <p>Upload a transaction ledger CSV to get started.</p>
            <p className="muted">
              Expected columns: an amount column (required), plus optional date, description/vendor,
              account, and category columns.
            </p>
          </section>
        )}
      </main>

      <footer className="footer">
        <p>For screening purposes only — not a substitute for professional audit judgment.</p>
      </footer>
    </div>
  );
}
