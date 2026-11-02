"""
Machine Learning Classifiers Module
Logistic Regression, Decision Trees, Random Forest, Support Vector Machines, Gradient Boosting.
"""

import os
import joblib
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support

class MLClassifierSuite:
    """Manages baseline machine learning models for radiological triage."""

    def __init__(self, model_dir: str = "ml/models"):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)
        self.scaler = StandardScaler()
        self.models = {
            "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
            "decision_tree": DecisionTreeClassifier(max_depth=10, random_state=42),
            "random_forest": RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, class_weight='balanced'),
            "svm": SVC(kernel='rbf', C=1.0, probability=True, random_state=42, class_weight='balanced'),
            "gradient_boosting": GradientBoostingClassifier(n_estimators=100, random_state=42)
        }

    def train_all(self, X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, class_names: list) -> Dict[str, Any]:
        """Trains all ML classifiers, evaluates on test set, and returns comparison dictionary."""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        comparison_results = {}

        for name, model in self.models.items():
            model.fit(X_train_scaled, y_train)
            preds = model.predict(X_test_scaled)
            probs = model.predict_proba(X_test_scaled) if hasattr(model, "predict_proba") else None

            acc = accuracy_score(y_test, preds)
            prec, rec, f1, _ = precision_recall_fscore_support(y_test, preds, average='weighted')

            comparison_results[name] = {
                "accuracy": float(acc),
                "precision": float(prec),
                "recall": float(rec),
                "f1_score": float(f1),
                "report": classification_report(y_test, preds, target_names=class_names, output_dict=True)
            }

            # Save model checkpoint
            joblib.dump(model, os.path.join(self.model_dir, f"{name}.pkl"))

        joblib.dump(self.scaler, os.path.join(self.model_dir, "scaler.pkl"))
        return comparison_results

    def predict(self, model_name: str, feature_vector: np.ndarray) -> Tuple[int, float, np.ndarray]:
        """Predicts class and confidence using a loaded ML model."""
        model_path = os.path.join(self.model_dir, f"{model_name}.pkl")
        scaler_path = os.path.join(self.model_dir, "scaler.pkl")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model {model_name} not found at {model_path}")

        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)

        scaled_feat = scaler.transform(feature_vector.reshape(1, -1))
        pred_idx = int(model.predict(scaled_feat)[0])
        probs = model.predict_proba(scaled_feat)[0] if hasattr(model, "predict_proba") else np.zeros(4)
        confidence = float(probs[pred_idx]) if hasattr(model, "predict_proba") else 1.0

        return pred_idx, confidence, probs
