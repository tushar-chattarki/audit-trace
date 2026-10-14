const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function analyzeCsv(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Analysis failed (${res.status})`);
  }
  return res.json();
}

export function reportPdfUrl(reportId) {
  return `${API_BASE}/api/report/${reportId}/pdf`;
}
