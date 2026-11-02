"""
Medical Dictionary & Abbreviation Expansion Module
"""

from typing import Dict

MEDICAL_ABBREVIATIONS: Dict[str, str] = {
    "cxr": "chest X-ray",
    "sob": "shortness of breath",
    "rll": "right lower lobe",
    "lul": "left upper lobe",
    "ggo": "ground-glass opacity",
    "tb": "tuberculosis",
    "ct": "computed tomography",
    "mri": "magnetic resonance imaging",
    "cbc": "complete blood count",
    "pao2": "partial pressure of oxygen",
    "spo2": "blood oxygen saturation",
    "hr": "heart rate",
    "bp": "blood pressure",
    "afeb": "afebrile",
    "wbc": "white blood cell count"
}

MEDICAL_TERMINOLOGY_MAP: Dict[str, str] = {
    "consolidation": "pulmonary fluid consolidation",
    "infiltrates": "pulmonary cellular infiltrates",
    "effusion": "pleural effusion fluid",
    "opacity": "radiodense opacity",
    "lesion": "focal anatomical lesion"
}

def expand_abbreviations(text: str) -> str:
    """Expands clinical acronyms into full terminology."""
    words = text.split()
    expanded = []
    for w in words:
        clean_w = w.lower().strip(".,;:()")
        if clean_w in MEDICAL_ABBREVIATIONS:
            expanded.append(MEDICAL_ABBREVIATIONS[clean_w])
        else:
            expanded.append(w)
    return " ".join(expanded)
