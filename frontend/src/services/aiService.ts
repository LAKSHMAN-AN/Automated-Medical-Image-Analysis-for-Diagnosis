import { api } from './api';
import { DiagnosticReport, AgentDecision } from '../types';

export const aiService = {
  async extractNLPEntities(clinicalText: string) {
    const res = await api.post('/nlp/extract', { clinical_text: clinicalText });
    return res.data;
  },

  async generateSLMReport(predictionId: string): Promise<DiagnosticReport> {
    const res = await api.post<DiagnosticReport>('/slm/generate-report', {
      prediction_id: predictionId,
      include_patient_summary: true,
    });
    return res.data;
  },

  async generateSyntheticScan(pathology: string = 'TUBERCULOSIS') {
    const res = await api.post('/genai/generate', { pathology });
    return res.data;
  },

  async runAgenticWorkflow(patientId: string, imageId: string): Promise<AgentDecision> {
    const res = await api.post<AgentDecision>('/agent/diagnose', {
      patient_id: patientId,
      image_id: imageId,
    });
    return res.data;
  },

  async submitDoctorFeedback(reportId: string, doctorAction: 'APPROVED' | 'MODIFIED' | 'REJECTED', notes?: string) {
    const res = await api.post('/feedback/submit', {
      report_id: reportId,
      doctor_action: doctorAction,
      doctor_notes: notes,
    });
    return res.data;
  }
};
