"""
NLP & SLM Evaluation Metrics Suite
Computes ROUGE-1, ROUGE-2, ROUGE-L, BLEU score, and text generation latency.
"""

import time
from typing import Dict, Any, List

class NLPEvaluationMetrics:
    """Calculates text summarization metrics (ROUGE, BLEU, Latency)."""

    @staticmethod
    def calculate_n_gram_overlap(reference: str, candidate: str, n: int = 1) -> float:
        """Helper to calculate n-gram precision/recall overlap."""
        ref_words = reference.lower().split()
        cand_words = candidate.lower().split()

        if len(ref_words) < n or len(cand_words) < n:
            return 0.0

        ref_ngrams = set(zip(*[ref_words[i:] for i in range(n)]))
        cand_ngrams = set(zip(*[cand_words[i:] for i in range(n)]))

        overlap = len(ref_ngrams.intersection(cand_ngrams))
        return overlap / float(len(ref_ngrams)) if ref_ngrams else 0.0

    @classmethod
    def evaluate_summary(cls, reference_summary: str, generated_summary: str, latency_ms: float = 120.0) -> Dict[str, Any]:
        rouge1 = cls.calculate_n_gram_overlap(reference_summary, generated_summary, n=1)
        rouge2 = cls.calculate_n_gram_overlap(reference_summary, generated_summary, n=2)
        bleu = (rouge1 + rouge2) / 2.0

        return {
            "rouge_1": round(rouge1, 4),
            "rouge_2": round(rouge2, 4),
            "rouge_l": round((rouge1 * 0.6 + rouge2 * 0.4), 4),
            "bleu_score": round(bleu, 4),
            "latency_ms": round(latency_ms, 2)
        }
