"""
SmartCare AI - Multi-Task Post-Training Probability Calibration
Performs Platt Sigmoid / Isotonic calibration separately on the validation split for each disease head.
Computes Brier Score, Expected Calibration Error (ECE), Calibration-in-the-Large, and threshold tuning.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional
from sklearn.linear_model import LogisticRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss, recall_score, precision_score, f1_score


class DiseaseCalibrator:
    """Calibrator for an individual task head."""
    def __init__(self, method: str = "sigmoid"):
        self.method = method
        self.calibrator = None
        self.is_fitted = False

    def fit(self, uncalibrated_probs: np.ndarray, y_val: np.ndarray):
        p_val = np.clip(uncalibrated_probs, 1e-6, 1.0 - 1e-6)
        if self.method == "sigmoid":
            # Platt scaling: fit logistic regression on log-odds
            log_odds = np.log(p_val / (1.0 - p_val)).reshape(-1, 1)
            self.calibrator = LogisticRegression(C=1.0, solver="lbfgs")
            self.calibrator.fit(log_odds, y_val)
        else:
            self.calibrator = IsotonicRegression(out_of_bounds="clip")
            self.calibrator.fit(p_val, y_val)
        self.is_fitted = True

    def predict_proba(self, uncalibrated_probs: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            return uncalibrated_probs
        p = np.clip(uncalibrated_probs, 1e-6, 1.0 - 1e-6)
        if self.method == "sigmoid":
            log_odds = np.log(p / (1.0 - p)).reshape(-1, 1)
            return self.calibrator.predict_proba(log_odds)[:, 1]
        else:
            return self.calibrator.predict(p)


class MultiTaskCalibrator:
    """
    Manages probability calibration across all three disease heads (T2D, CVD, CKD).
    """

    def __init__(self, method: str = "sigmoid"):
        self.method = method
        self.calibrators: Dict[str, DiseaseCalibrator] = {
            "t2d": DiseaseCalibrator(method=method),
            "cvd": DiseaseCalibrator(method=method),
            "ckd": DiseaseCalibrator(method=method),
        }
        self.optimal_thresholds: Dict[str, float] = {
            "t2d": 0.40,
            "cvd": 0.35,
            "ckd": 0.35
        }

    @staticmethod
    def calculate_ece(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
        """Calculates Expected Calibration Error (ECE)."""
        bin_edges = np.linspace(0, 1, n_bins + 1)
        ece = 0.0
        n = len(y_true)

        for i in range(n_bins):
            bin_mask = (y_prob > bin_edges[i]) & (y_prob <= bin_edges[i + 1])
            if np.sum(bin_mask) > 0:
                bin_acc = np.mean(y_true[bin_mask])
                bin_conf = np.mean(y_prob[bin_mask])
                bin_weight = np.sum(bin_mask) / n
                ece += bin_weight * np.abs(bin_acc - bin_conf)

        return float(round(ece, 4))

    @staticmethod
    def calculate_calibration_in_the_large(y_true: np.ndarray, y_prob: np.ndarray) -> float:
        """Calculates Calibration-in-the-large (mean predicted probability minus observed event rate)."""
        mean_pred = float(np.mean(y_prob))
        mean_obs = float(np.mean(y_true))
        return float(round(mean_pred - mean_obs, 4))

    def fit_and_evaluate(
        self,
        model: Any,
        val_splits: Dict[str, Tuple[pd.DataFrame, pd.Series]],
        min_recall_targets: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Fits calibration models on the validation split and tunes disease-specific decision thresholds.
        """
        min_recall = min_recall_targets or {"t2d": 0.75, "cvd": 0.75, "ckd": 0.85}
        calibration_reports = {}

        for disease in ["t2d", "cvd", "ckd"]:
            X_val, y_val = val_splits[disease]
            y_val_arr = y_val.values if hasattr(y_val, "values") else np.asarray(y_val)

            # 1. Uncalibrated predictions
            probs_raw = model.forward(X_val, training=False)[0][disease]
            uncalib_brier = float(brier_score_loss(y_val_arr, probs_raw))
            uncalib_ece = self.calculate_ece(y_val_arr, probs_raw)
            uncalib_citl = self.calculate_calibration_in_the_large(y_val_arr, probs_raw)

            # 2. Fit Calibrator
            self.calibrators[disease].fit(probs_raw, y_val_arr)
            calib_probs = self.calibrators[disease].predict_proba(probs_raw)

            calib_brier = float(brier_score_loss(y_val_arr, calib_probs))
            calib_ece = self.calculate_ece(y_val_arr, calib_probs)
            calib_citl = self.calculate_calibration_in_the_large(y_val_arr, calib_probs)

            # 3. Calibration Curve
            prob_true, prob_pred = calibration_curve(y_val_arr, calib_probs, n_bins=10)

            # 4. Optimal Threshold Search on Val Split
            target_rec = min_recall.get(disease, 0.75)
            best_th = 0.50
            best_f1 = 0.0

            for th in np.linspace(0.15, 0.75, 61):
                preds = (calib_probs >= th).astype(int)
                rec = recall_score(y_val_arr, preds, zero_division=0)
                if rec >= target_rec:
                    f1 = f1_score(y_val_arr, preds, zero_division=0)
                    if f1 > best_f1:
                        best_f1 = f1
                        best_th = float(round(th, 2))

            # Fallback if constraint too tight
            if best_f1 == 0.0:
                best_th = 0.40 if disease == "t2d" else 0.35

            self.optimal_thresholds[disease] = best_th

            calibration_reports[disease] = {
                "disease": disease.upper(),
                "method": self.method,
                "uncalibrated_brier": round(uncalib_brier, 4),
                "calibrated_brier": round(calib_brier, 4),
                "brier_improvement": round(uncalib_brier - calib_brier, 4),
                "uncalibrated_ece": uncalib_ece,
                "calibrated_ece": calib_ece,
                "calibration_in_the_large": calib_citl,
                "optimal_threshold": best_th,
                "val_target_recall": target_rec,
                "val_optimized_f1": round(best_f1, 4),
                "calibration_curve": {
                    "prob_true": [round(float(x), 4) for x in prob_true],
                    "prob_pred": [round(float(x), 4) for x in prob_pred]
                }
            }

        return calibration_reports

    def calibrate(self, uncalibrated_probs_dict: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Calibrates dictionary of probabilities."""
        return {
            disease: self.calibrators[disease].predict_proba(uncalibrated_probs_dict[disease])
            for disease in ["t2d", "cvd", "ckd"]
        }
