"""
Natural Language Processing (NLP) Service
Medical text cleaning, Named Entity Recognition (NER), and entity extraction.
"""

import re
from typing import Dict, List, Any

class NLPService:
    """Service for extracting medical entities from clinical notes."""

    @staticmethod
    def clean_text(text: str) -> str:
        """Removes special characters, extra whitespace, and standardizes text."""
        cleaned = re.sub(r'[\r\n\t]+', ' ', text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    def extract_entities(self, clinical_text: str) -> List[Dict[str, Any]]:
        """Extracts medical entities (Anatomy, Disease, Severity, Status) using regex/rules."""
        cleaned = self.clean_text(clinical_text)
        entities = []

        keywords = {
            "ANATOMY": ["lung", "chest", "lower lobe", "upper lobe", "pleural", "bronchial"],
            "PATHOLOGY": ["opacities", "infiltrates", "consolidation", "effusion", "nodule", "lesion", "pneumonia", "covid", "tuberculosis"],
            "SEVERITY": ["severe", "mild", "moderate", "acute", "chronic", "extensive"],
            "STATUS": ["normal", "clear", "unremarkable", "stable", "worsening"]
        }

        words = cleaned.lower().split()
        for category, kw_list in keywords.items():
            for kw in kw_list:
                if kw in cleaned.lower():
                    entities.append({
                        "entity": kw.title(),
                        "category": category,
                        "confidence": 0.95
                    })

        return entities
