export type Role = 'ADMIN' | 'RADIOLOGIST' | 'DOCTOR' | 'PATIENT';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: Role;
  is_active: boolean;
  created_at: string;
}

export interface Patient {
  id: string;
  patient_code: string;
  age: number;
  gender: 'MALE' | 'FEMALE' | 'OTHER';
  medical_history?: string;
  created_at: string;
}

export interface MedicalImage {
  id: string;
  patient_id: string;
  image_url: string;
  modality: 'CHEST_XRAY' | 'BRAIN_MRI' | 'LUNG_CT';
  width?: number;
  height?: number;
  file_hash: string;
  uploaded_at: string;
}

export interface Prediction {
  id: string;
  image_id: string;
  model_name: string;
  model_version: string;
  predicted_class: 'NORMAL' | 'COVID' | 'PNEUMONIA' | 'TUBERCULOSIS';
  confidence_score: number;
  class_probabilities: Record<string, number>;
  heatmap_url?: string;
  execution_time_ms: number;
  predicted_at: string;
}

export interface DiagnosticReport {
  id: string;
  prediction_id: string;
  nlp_extracted_entities?: string;
  slm_clinical_summary: string;
  slm_patient_explanation: string;
  status: 'DRAFT' | 'PENDING_REVIEW' | 'APPROVED' | 'REJECTED';
  generated_at: string;
}

export interface Feedback {
  id: string;
  report_id: string;
  doctor_id: string;
  doctor_action: 'APPROVED' | 'MODIFIED' | 'REJECTED';
  corrected_class?: string;
  doctor_notes?: string;
  submitted_at: string;
}

export interface AnalyticsSummary {
  total_scans: number;
  total_patients: number;
  total_predictions: number;
  total_approved_reports: number;
  class_distribution: Record<string, number>;
  model_performance: Record<string, {
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
    roc_auc: number;
  }>;
  confusion_matrix: number[][];
}

export interface AgentDecision {
  agent_id: string;
  primary_diagnosis: string;
  confidence_score: number;
  differential_diagnoses: Array<{ pathology: string; probability: number }>;
  reasoning_summary: string;
  recommended_actions: string[];
  requires_hitl_approval: boolean;
}
