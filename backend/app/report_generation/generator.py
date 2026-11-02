"""
Automated Medical Report Generation Engine
Combines DL prediction outputs, GradCAM coordinates, and SLM templates.
"""

from typing import Dict, Any
from backend.app.prompts.templates import CLINICAL_SUMMARY_PROMPT, PATIENT_EXPLANATION_PROMPT

class MedicalReportGenerator:
    """Generates structured multi-audience diagnostic reports."""

    def generate_full_report(
        self,
        patient_code: str,
        age: int,
        gender: str,
        medical_history: str,
        predicted_class: str,
        confidence: float,
        modality: str = "CHEST_XRAY",
        affected_region: str = "Right Lower Lobe (x=45, y=60, w=110, h=95)"
    ) -> Dict[str, Any]:
        """Generates clinical summary, patient explanation, and follow-up recommendations."""
        
        # Format Clinical Summary
        if predicted_class == "NORMAL":
            clinical_summary = (
                f"Chest Radiograph Evaluation for {age}-year-old {gender} ({patient_code}): "
                f"Lungs are clear without focal consolidation, pneumothorax, or pleural effusion. "
                f"Cardiomediastinal silhouette is within normal limits (Confidence: {confidence*100:.1f}%)."
            )
            patient_explanation = "Your chest X-ray shows clear, healthy lung tissue with no signs of infection."
            recommendations = ["Routine clinical follow-up as indicated."]
            follow_up_tests = ["No immediate follow-up imaging required."]
        elif predicted_class == "COVID":
            clinical_summary = (
                f"Chest Radiograph Evaluation for {age}-year-old {gender} ({patient_code}): "
                f"Bilateral ground-glass opacities in peripheral zones ({affected_region}). "
                f"Findings highly suggestive of viral pneumonitis / COVID-19 infection (Confidence: {confidence*100:.1f}%)."
            )
            patient_explanation = "Your scan shows pattern changes typical of viral chest infection (COVID-19)."
            recommendations = ["Isolate patient according to clinical protocols", "Monitor SpO2 levels closely"]
            follow_up_tests = ["RT-PCR confirmation test", "High-Resolution CT Scan (HRCT) if dyspnea worsens"]
        elif predicted_class == "PNEUMONIA":
            clinical_summary = (
                f"Chest Radiograph Evaluation for {age}-year-old {gender} ({patient_code}): "
                f"Focal pulmonary consolidation with air bronchograms identified ({affected_region}), "
                f"indicative of active lobar pneumonia (Confidence: {confidence*100:.1f}%)."
            )
            patient_explanation = "Your scan shows fluid accumulation in the lung consistent with bacterial pneumonia."
            recommendations = ["Initiate empirical antibiotic regimen", "Ensure proper hydration and bed rest"]
            follow_up_tests = ["Complete Blood Count (CBC) with differential", "Repeat X-ray in 4-6 weeks"]
        else:  # TUBERCULOSIS
            clinical_summary = (
                f"Chest Radiograph Evaluation for {age}-year-old {gender} ({patient_code}): "
                f"Apical infiltrates with cavitary lesions ({affected_region}), "
                f"indicative of pulmonary tuberculosis (Confidence: {confidence*100:.1f}%)."
            )
            patient_explanation = "Your scan shows upper lung changes requiring specialized follow-up testing for tuberculosis."
            recommendations = ["Respiratory isolation", "Notify public health department"]
            follow_up_tests = ["Sputum Acid-Fast Bacilli (AFB) smear", "GeneXpert MTB/RIF assay"]

        disclaimer = "NOTICE: AI-generated reports are clinical decision support tools only and require attending radiologist verification."

        return {
            "patient_code": patient_code,
            "modality": modality,
            "predicted_class": predicted_class,
            "confidence_score": confidence,
            "affected_region": affected_region,
            "clinical_summary": clinical_summary,
            "patient_explanation": patient_explanation,
            "recommended_actions": recommendations,
            "follow_up_tests": follow_up_tests,
            "disclaimer": disclaimer
        }
