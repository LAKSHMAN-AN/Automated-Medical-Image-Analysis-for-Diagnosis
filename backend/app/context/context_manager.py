"""
Clinical Context Manager
"""

from typing import Dict, Any, Optional

class ClinicalContextManager:
    """Maintains active patient context and historical diagnostic state."""

    def __init__(self):
        self._active_context: Dict[str, Any] = {}

    def set_context(self, patient_code: str, age: int, gender: str, medical_history: str, prediction: Dict[str, Any]):
        self._active_context = {
            "patient_code": patient_code,
            "age": age,
            "gender": gender,
            "medical_history": medical_history,
            "predicted_class": prediction.get("predicted_class", "NORMAL"),
            "confidence": prediction.get("confidence_score", 0.95),
            "model_name": prediction.get("model_name", "ResNet50")
        }

    def get_context(self) -> Dict[str, Any]:
        return self._active_context

    def clear(self):
        self._active_context = {}
