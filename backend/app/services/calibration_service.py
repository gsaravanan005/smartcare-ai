import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss, recall_score, precision_score, f1_score, accuracy_score

class CalibrationService:

    @classmethod
    def calibrate_model(
        cls,
        model: Any,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        method: str = "sigmoid"
    ) -> Tuple[Any, Dict[str, Any]]:
        """
        Calibrates model probability estimates using Validation data.
        Method: 'sigmoid' (Platt scaling) or 'isotonic'.
        """
        try:
            calibrated_model = CalibratedClassifierCV(estimator=model, method=method, cv=3)
            calibrated_model.fit(X_val, y_val)
        except Exception:
            calibrated_model = model

        # Evaluate raw vs calibrated Brier score on validation split
        if hasattr(model, 'predict_proba'):
            raw_probs = model.predict_proba(X_val)[:, 1]
        else:
            raw_probs = np.zeros(len(y_val))

        if hasattr(calibrated_model, 'predict_proba'):
            cal_probs = calibrated_model.predict_proba(X_val)[:, 1]
        else:
            cal_probs = raw_probs

        raw_brier = float(brier_score_loss(y_val, raw_probs))
        cal_brier = float(brier_score_loss(y_val, cal_probs))

        # Generate calibration curve (reliability diagram points)
        prob_true, prob_pred = calibration_curve(y_val, cal_probs, n_bins=10)

        curve_data = {
            "predicted_probabilities": [round(float(p), 4) for p in prob_pred],
            "observed_frequencies": [round(float(p), 4) for p in prob_true]
        }

        metrics = {
            "calibration_method": method,
            "raw_brier_score": round(raw_brier, 4),
            "calibrated_brier_score": round(cal_brier, 4),
            "brier_improvement": round(raw_brier - cal_brier, 4),
            "calibration_curve": curve_data
        }

        return calibrated_model, metrics

    @classmethod
    def find_optimal_threshold(
        cls,
        model: Any,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        min_recall_target: float = 0.70
    ) -> Dict[str, Any]:
        """
        Finds optimal classification threshold on Validation split.
        Prioritizes medical recall (sensitivity) while maximizing F1 score.
        """
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(X_val)[:, 1]
        else:
            probs = np.zeros(len(y_val))

        thresholds = np.linspace(0.1, 0.9, 81)
        
        best_threshold = 0.5
        best_f1 = -1.0
        best_metrics = {}

        for th in thresholds:
            preds = (probs >= th).astype(int)
            rec = recall_score(y_val, preds, zero_division=0)
            prec = precision_score(y_val, preds, zero_division=0)
            f1 = f1_score(y_val, preds, zero_division=0)
            acc = accuracy_score(y_val, preds)

            if rec >= min_recall_target and f1 > best_f1:
                best_f1 = f1
                best_threshold = float(th)
                best_metrics = {
                    "threshold": round(float(th), 2),
                    "recall": round(float(rec), 4),
                    "precision": round(float(prec), 4),
                    "f1_score": round(float(f1), 4),
                    "accuracy": round(float(acc), 4)
                }

        if not best_metrics:
            for th in thresholds:
                preds = (probs >= th).astype(int)
                f1 = f1_score(y_val, preds, zero_division=0)
                if f1 > best_f1:
                    best_f1 = f1
                    best_threshold = float(th)
                    best_metrics = {
                        "threshold": round(float(th), 2),
                        "recall": round(float(recall_score(y_val, preds, zero_division=0)), 4),
                        "precision": round(float(precision_score(y_val, preds, zero_division=0)), 4),
                        "f1_score": round(float(f1), 4),
                        "accuracy": round(float(accuracy_score(y_val, preds)), 4)
                    }

        return best_metrics
