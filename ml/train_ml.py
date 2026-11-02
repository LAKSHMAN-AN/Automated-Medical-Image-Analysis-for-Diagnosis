"""
Machine Learning Baseline Pipeline
Extracts GLCM + HOG features, trains Random Forest & SVM classifiers,
and outputs performance metrics (Accuracy, Precision, Recall, F1, Confusion Matrix, ROC-AUC).
"""
import os
import joblib
import numpy as np
from pathlib import Path
from typing import Tuple, Dict
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SV 
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler

from ml.feature_extraction.glcm_extractor import GLCMFeatureExtractor
from ml.feature_extraction.hog_extractor import HOGFeatureExtractor
class MLBaselinePipeline:
    """End-to-End Machine Learning Baseline Classifier Pipeline."""

    def __init__(self, dataset_dir: str):
        self.dataset_dir = Path(dataset_dir)
        self.classes = ['NORMAL', 'COVID', 'PNEUMONIA', 'TUBERCULOSIS']
        self.label_map = {cls: idx for idx, cls in enumerate(self.classes)}
        self.glcm = GLCMFeatureExtractor()
        self.hog = HOGFeatureExtractor()
        self.scaler = StandardScaler()
        self.rf_model = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, class_weight='balanced')
        self.svm_model = SVC(kernel='rbf', C=1.0, probability=True, random_state=42, class_weight='balanced')

    def _extract_dataset_features(self, split: str) -> Tuple[np.ndarray, np.ndarray]:
        """Extracts combined GLCM + HOG feature vectors for all images in split."""
        X, y = [], []
        split_dir = self.dataset_dir / split
        
        for cls in self.classes:
            cls_dir = split_dir / cls
            if not cls_dir.exists():
                continue
            for img_file in cls_dir.iterdir():
                if img_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                    try:
                        glcm_feat = self.glcm.extract(str(img_file))
                        hog_feat = self.hog.extract(str(img_file))
                        combined = np.hstack([glcm_feat, hog_feat])
                        X.append(combined)
                        y.append(self.label_map[cls])
                    except Exception as e:
                        print(f"Skipping corrupt image {img_file}: {e}")

        return np.array(X, dtype=np.float32), np.array(y, dtype=np.int64)

    def train_and_evaluate(self, model_save_dir: str = "ml/models") -> Dict:
        """Trains models on 'train' split and evaluates on 'test' split."""
        print("Extracting features from Training set...")
        X_train, y_train = self._extract_dataset_features('train')
        print(f"Train samples: {len(X_train)}")

        print("Extracting features from Testing set...")
        X_test, y_test = self._extract_dataset_features('test')
        print(f"Test samples: {len(X_test)}")

        if len(X_train) == 0:
            print("No training images found in dataset path. Place images under datasets/chest_xray/train/")
            return {}

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train Random Forest
        print("Training Random Forest Classifier...")
        self.rf_model.fit(X_train_scaled, y_train)
        rf_preds = self.rf_model.predict(X_test_scaled)
        rf_probs = self.rf_model.predict_proba(X_test_scaled)

        # Train SVM
        print("Training SVM Classifier...")
        self.svm_model.fit(X_train_scaled, y_train)
        svm_preds = self.svm_model.predict(X_test_scaled)
        svm_probs = self.svm_model.predict_proba(X_test_scaled)

        # Save artifacts
        os.makedirs(model_save_dir, exist_ok=True)
        joblib.dump(self.rf_model, os.path.join(model_save_dir, "random_forest_baseline.pkl"))
        joblib.dump(self.svm_model, os.path.join(model_save_dir, "svm_baseline.pkl"))
        joblib.dump(self.scaler, os.path.join(model_save_dir, "scaler.pkl"))

        metrics = {
            "random_forest": {
                "report": classification_report(y_test, rf_preds, target_names=self.classes, output_dict=True),
                "confusion_matrix": confusion_matrix(y_test, rf_preds).tolist(),
            },
            "svm": {
                "report": classification_report(y_test, svm_preds, target_names=self.classes, output_dict=True),
                "confusion_matrix": confusion_matrix(y_test, svm_preds).tolist(),
            }
        }
        return metrics

if __name__ == "__main__":
    pipeline = MLBaselinePipeline("datasets/chest_xray")
    results = pipeline.train_and_evaluate()
    print("Baseline Training Results:", results)
