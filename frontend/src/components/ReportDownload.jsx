import { reportPdfUrl } from "../api";

export default function ReportDownload({ reportId, filename }) {
  if (!reportId) return null;
  return (
    <a className="download-btn" href={reportPdfUrl(reportId)} download>
      ⬇ Download Audit Report (PDF)
    </a>
  );
}
