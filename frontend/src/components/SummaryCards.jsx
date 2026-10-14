export default function SummaryCards({ summary }) {
  const entries = Object.entries(summary || {});
  return (
    <div className="summary-grid">
      {entries.map(([label, value]) => (
        <div className="summary-card" key={label}>
          <div className="summary-card__value">{String(value)}</div>
          <div className="summary-card__label">{label}</div>
        </div>
      ))}
    </div>
  );
}
