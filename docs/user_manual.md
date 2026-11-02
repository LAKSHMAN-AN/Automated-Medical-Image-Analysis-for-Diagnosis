# Clinical User & Radiologist Manual

Welcome to the **RadAI Automated Medical Image Analysis & Diagnostics Platform**.

---

## 📋 End-to-End Clinical Diagnostic Workflow

### 1. Authentication
1. Open `http://localhost` (or `http://localhost:3000` in dev mode).
2. Click **Launch Clinical Portal**.
3. Sign in using your radiologist credentials (`radiologist@hospital.org` / `RadioSecret2026!`).

### 2. Upload Radiological Image Scan
1. Navigate to **Upload Medical Scan** in the sidebar.
2. Select target patient record (`PAT-2026-001`).
3. Select scan modality (`Chest X-Ray`, `Brain MRI`, or `Lung CT`).
4. Drag and drop a PNG, JPEG, or DICOM scan file up to 50MB.
5. Click **Analyze Image Scan**.

### 3. Inspect AI Diagnostics & Grad-CAM Heatmap
1. View predicted disease category (`NORMAL`, `COVID-19`, `PNEUMONIA`, `TUBERCULOSIS`) and confidence percentage.
2. Toggle the **Grad-CAM Overlay** switch to visually verify highlighted lesion regions.
3. Review class probability distribution.

### 4. Generate SLM Report & Doctor Approval
1. Click **Generate Contextual Clinical Report** to generate Phi-3 SLM technical summary and patient-friendly explanations.
2. Review the multi-agent reasoning breakdown under **Agentic AI Assistant**.
3. Click **Approve** or **Reject** to confirm the diagnosis and record feedback in audit logs.
