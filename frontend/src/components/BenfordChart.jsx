import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  ComposedChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function BenfordChart({ benford }) {
  if (!benford?.applicable) {
    return (
      <div className="panel">
        <h3>Benford's Law Analysis</h3>
        <p className="muted">{benford?.reason || "Not applicable for this dataset."}</p>
      </div>
    );
  }

  const data = benford.per_digit.map((d) => ({
    digit: d.digit,
    Observed: d.observed_pct,
    Expected: d.expected_pct,
  }));

  return (
    <div className="panel">
      <h3>Benford's Law — Leading Digit Distribution</h3>
      <p className="muted">{benford.summary}</p>
      <ResponsiveContainer width="100%" height={280}>
        <ComposedChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
          <XAxis dataKey="digit" stroke="var(--muted)" />
          <YAxis stroke="var(--muted)" unit="%" />
          <Tooltip
            contentStyle={{ background: "var(--panel)", border: "1px solid var(--border)", color: "var(--text)" }}
          />
          <Legend />
          <Bar dataKey="Observed" fill="var(--accent)" radius={[4, 4, 0, 0]} />
          <Line type="monotone" dataKey="Expected" stroke="var(--danger)" strokeWidth={2} dot={{ r: 3 }} />
        </ComposedChart>
      </ResponsiveContainer>
      {benford.significant && (
        <p className="badge badge--warn">
          Distribution deviates significantly from Benford's Law (p &lt; 0.05) — worth a closer look.
        </p>
      )}
    </div>
  );
}
