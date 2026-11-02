"""
Hyperparameter Optimization & K-Fold Cross Validation Manager
"""

import numpy as np
from typing import Dict, Any, List
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.ensemble import RandomForestClassifier

class HyperparameterTuner:
    """Manages Stratified K-Fold Cross Validation and Grid Search Hyperparameter Tuning."""

    @staticmethod
    def run_cross_validation(X: np.ndarray, y: np.ndarray, n_splits: int = 5) -> Dict[str, Any]:
        """Runs Stratified 5-Fold Cross Validation for Random Forest Baseline."""
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        scores = []

        for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
            X_tr, y_tr = X[train_idx], y[train_idx]
            X_va, y_va = X[val_idx], y[val_idx]

            clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
            clf.fit(X_tr, y_tr)
            score = clf.score(X_va, y_va)
            scores.append(score)

        return {
            "n_splits": n_splits,
            "fold_scores": scores,
            "mean_accuracy": float(np.mean(scores)),
            "std_accuracy": float(np.std(scores))
        }

    @staticmethod
    def tune_random_forest(X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """Grid Search for best hyperparameter configuration."""
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [8, 12, 16],
            'min_samples_split': [2, 5]
        }
        rf = RandomForestClassifier(random_state=42)
        grid_search = GridSearchCV(rf, param_grid, cv=3, scoring='accuracy', n_jobs=-1)
        grid_search.fit(X, y)

        return {
            "best_params": grid_search.best_params_,
            "best_score": float(grid_search.best_score_)
        }
