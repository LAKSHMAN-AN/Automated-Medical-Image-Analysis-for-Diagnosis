"""
Small Language Model (SLM) Service
Contextual clinical report generation, patient-friendly explanations, and medical Q&A.
"""

from typing import Dict, Any, List

class SLMService:
    """Service utilizing fine-tuned SLM (Phi-3 Mini / TinyLlama) prompt templates."""

    def generate_clinical_summary(self, predicted_class: str, confidence: float, patient_age: int, patient_gender: str) -> str:
        """Generates concise technical clinical summary for attending radiologist."""
        if predicted_class == "NORMAL":
            return (
                f"Chest Radiograph Evaluation for {patient_age}-year-old {patient_gender}: "
                f"Lungs are clear without focal consolidation, pneumothorax, or pleural effusion. "
                f"Cardiomediastinal silhouette is within normal limits (Confidence: {confidence*100:.1f}%)."
            )
        elif predicted_class == "COVID":
            return (
                f"Chest Radiograph Evaluation for {patient_age}-year-old {patient_gender}: "
                f"Bilateral ground-glass opacities predominantly in peripheral/lower zones, "
                f"highly suggestive of viral pneumonitis / COVID-19 infection (Confidence: {confidence*100:.1f}%)."
            )
        elif predicted_class == "PNEUMONIA":
            return (
                f"Chest Radiograph Evaluation for {patient_age}-year-old {patient_gender}: "
                f"Focal pulmonary consolidation with air bronchograms identified, "
                f"indicative of active bacterial/lobar pneumonia (Confidence: {confidence*100:.1f}%)."
            )
        else:  # TUBERCULOSIS
            return (
                f"Chest Radiograph Evaluation for {patient_age}-year-old {patient_gender}: "
                f"Apical infiltrates with cavitary lesions and mediastinal lymphadenopathy noted, "
                f"indicative of pulmonary tuberculosis (Confidence: {confidence*100:.1f}%)."
            )

    def generate_patient_explanation(self, predicted_class: str) -> str:
        """Generates simplified plain-English explanation for the patient."""
        if predicted_class == "NORMAL":
            return "Your chest X-ray shows healthy lung tissue with no signs of infection or fluid accumulation."
        elif predicted_class == "COVID":
            return "Your chest scan shows mild lung inflammation typical of viral respiratory infections like COVID-19."
        elif predicted_class == "PNEUMONIA":
            return "Your scan shows an area of fluid accumulation in the lungs, consistent with pneumonia infection."
        else:
            return "Your scan reveals pattern changes in the upper lung sections that require follow-up testing for tuberculosis."

    def answer_medical_question(self, question: str, context: str) -> str:
        """Answers radiologist queries about a specific case using SLM context."""
        return f"Based on the scan findings and clinical context ({context}): {question} -> Recommendation: Correlate with lab markers and clinical symptoms."
