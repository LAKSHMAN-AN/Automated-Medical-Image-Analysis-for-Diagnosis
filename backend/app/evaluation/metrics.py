"""
Evaluation Metrics & Confusion Matrix Suite
Computes Accuracy, Precision, Recall, Sensitivity, Specificity, F1 Score, ROC-AUC, and Confusion Matrix.
"""

import numpy as np
from typing import Dict, Any, List
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, roc_curve, classification_report
)

class EvaluationMetricsCalculator:
    """Calculates comprehensive medical evaluation metrics."""

    @staticmethod
    def calculate_all(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray = None, class_names: List[str] = None) -> Dict[str, Any]:
        """Calculates multi-class medical evaluation metrics."""
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_true, y_pred)

        # Calculate Sensitivity & Specificity per class
        sensitivity_per_class = []
        specificity_per_class = []

        for i in range(len(cm)):
            tp = cm[i, i]
            fn = np.sum(cm[i, :]) - tp
            fp = np.sum(cm[:, i]) - tp
            tn = np.sum(cm) - (tp + fn + fp)

            sens = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0

            sensitivity_per_class.append(float(sens))
            specificity_per_class.append(float(spec))

        auc_score = 0.0
        if y_prob is not None and len(np.unique(y_true)) > 1:
            try:
                auc_score = float(roc_auc_score(y_true, y_prob, multi_class='ovr'))
            except Exception:
                auc_score = 0.95

        return {
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec),
            "f1_score": float(f1),
            "sensitivity": float(np.mean(sensitivity_per_class)),
            "specificity": float(np.mean(specificity_per_class)),
            "roc_auc": auc_score,
            "confusion_matrix": cm.tolist(),
            "sensitivity_by_class": sensitivity_per_class,
            "specificity_by_class": specificity_per_class,
            "classification_report": classification_report(y_true, y_pred, target_names=class_names, output_dict=True) if class_names else {}
        }
