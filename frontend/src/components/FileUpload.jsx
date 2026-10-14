import { useCallback, useRef, useState } from "react";

export default function FileUpload({ onFileSelected, disabled }) {
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef(null);

  const handleFiles = useCallback(
    (files) => {
      const file = files?.[0];
      if (!file) return;
      if (!file.name.toLowerCase().endsWith(".csv")) {
        alert("Please select a .csv file.");
        return;
      }
      onFileSelected(file);
    },
    [onFileSelected]
  );

  return (
    <div
      className={`dropzone ${isDragging ? "dropzone--active" : ""} ${disabled ? "dropzone--disabled" : ""}`}
      onClick={() => !disabled && inputRef.current?.click()}
      onDragOver={(e) => {
        e.preventDefault();
        if (!disabled) setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setIsDragging(false);
        if (!disabled) handleFiles(e.dataTransfer.files);
      }}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".csv"
        hidden
        onChange={(e) => handleFiles(e.target.files)}
        disabled={disabled}
      />
      <div className="dropzone__icon">📄</div>
      <p className="dropzone__title">Drop a transaction ledger CSV here</p>
      <p className="dropzone__subtitle">or click to browse — amount column required, date/description optional</p>
    </div>
  );
}
