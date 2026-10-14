import { Fragment, useState } from "react";

function riskClass(score) {
  if (score >= 75) return "risk risk--high";
  if (score >= 40) return "risk risk--medium";
  return "risk risk--low";
}

export default function AnomalyTable({ flagged }) {
  const [expanded, setExpanded] = useState(null);

  if (!flagged?.length) {
    return (
      <div className="panel">
        <h3>Flagged Transactions</h3>
        <p className="muted">No transactions were flagged in this dataset.</p>
      </div>
    );
  }

  return (
    <div className="panel">
      <h3>Flagged Transactions ({flagged.length})</h3>
      <div className="table-wrap">
        <table className="table">
          <thead>
            <tr>
              <th>Risk</th>
              <th>Amount</th>
              <th>Date</th>
              <th>Description</th>
              <th>Signals</th>
            </tr>
          </thead>
          <tbody>
            {flagged.map((f, idx) => (
              <Fragment key={f.row_index}>
                <tr
                  className="table__row"
                  onClick={() => setExpanded(expanded === idx ? null : idx)}
                >
                  <td>
                    <span className={riskClass(f.risk_score)}>{f.risk_score.toFixed(0)}</span>
                  </td>
                  <td>{f.amount.toLocaleString(undefined, { style: "currency", currency: "USD" })}</td>
                  <td>{f.date || "—"}</td>
                  <td>{f.description || "—"}</td>
                  <td>
                    {f.is_duplicate && <span className="tag tag--dup">duplicate</span>}
                    {f.is_round_number && <span className="tag tag--round">round #</span>}
                    {f.is_model_anomaly && <span className="tag tag--model">ML anomaly</span>}
                  </td>
                </tr>
                {expanded === idx && (
                  <tr className="table__detail-row">
                    <td colSpan={5}>
                      <ul className="reason-list">
                        {f.reasons.map((r, i) => (
                          <li key={i}>{r}</li>
                        ))}
                      </ul>
                    </td>
                  </tr>
                )}
              </Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
