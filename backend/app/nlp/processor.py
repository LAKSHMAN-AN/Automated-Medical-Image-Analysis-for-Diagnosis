"""
Medical NLP Text Processing & Entity Extraction Engine
"""

import re
from typing import Dict, List, Any
from backend.app.medical_dictionary.dictionary import expand_abbreviations

class MedicalNLPProcessor:
    """Parses clinical reports, expands medical acronyms, and extracts structured entities."""

    def clean_text(self, text: str) -> str:
        """Sanitizes input text and expands medical acronyms."""
        cleaned = re.sub(r'[\r\n\t]+', ' ', text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        expanded = expand_abbreviations(cleaned)
        return expanded

    def segment_sentences(self, text: str) -> List[str]:
        """Segments clinical text into individual sentences."""
        cleaned = self.clean_text(text)
        sentences = re.split(r'(?<=[.!?]) +', cleaned)
        return [s.strip() for s in sentences if s.strip()]

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extracts medical entities (Anatomy, Symptoms, Disease, Medication, Severity)."""
        cleaned = self.clean_text(text)
        entities = []

        entity_rules = {
            "ANATOMY": [r"lung[s]?", r"chest", r"lower lobe", r"upper lobe", r"pleural", r"apical"],
            "SYMPTOM": [r"fever", r"cough", r"shortness of breath", r"dyspnea", r"chest pain", r"fatigue"],
            "DISEASE": [r"pneumonia", r"covid-19", r"covid", r"tuberculosis", r"tumor", r"cancer", r"consolidation"],
            "SEVERITY": [r"severe", r"mild", r"moderate", r"acute", r"chronic", r"extensive"],
            "MEDICATION": [r"azithromycin", r"amoxicillin", r"paracetamol", r"remdesivir", r"corticosteroid"]
        }

        for category, patterns in entity_rules.items():
            for pat in patterns:
                matches = re.finditer(pat, cleaned, re.IGNORECASE)
                for m in matches:
                    entities.append({
                        "entity": m.group(0).title(),
                        "category": category,
                        "start": m.start(),
                        "end": m.end(),
                        "confidence": 0.95
                    })

        return entities

    def classify_severity(self, text: str) -> str:
        """Determines clinical risk/severity category (Low, Moderate, High, Critical)."""
        text_lower = text.lower()
        if any(k in text_lower for k in ["critical", "cavitary", "severe respiratory failure", "bilateral extensive"]):
            return "CRITICAL"
        elif any(k in text_lower for k in ["acute", "consolidation", "pneumonia", "covid"]):
            return "HIGH"
        elif any(k in text_lower for k in ["mild", "moderate", "infiltrate"]):
            return "MODERATE"
        return "LOW"
