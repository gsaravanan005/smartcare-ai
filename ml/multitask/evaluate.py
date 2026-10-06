"""
SmartCare AI - Multi-Task Model Evaluation & Comparative Analysis Engine
Computes comprehensive metrics: Accuracy, Precision, Recall, Specificity, F1, ROC-AUC, PR-AUC,
Brier, ECE, Calibration-in-the-large, Confusion Matrix, Subgroups (Age, Sex), DCA, Baseline comparison, and Ablation study.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List, Optional
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, precision_recall_curve, auc, confusion_matrix, brier_score_loss
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb

from .config import MTLConfig
from .calibration import MultiTaskCalibrator


class MultiTaskEvaluator:
    """
    Evaluates Multi-Task Neural Network against all clinical metrics, baselines, subgroups, and ablations.
    """

    @classmethod
    def evaluate_task_test_split(
        cls,
        probs: np.ndarray,
        y_test: np.ndarray,
        threshold: float = 0.5
    ) -> Dict[str, Any]:
        """Calculates all 10 core clinical metrics on a held-out test split."""
        y_arr = np.asarray(y_test).astype(int)
        preds = (probs >= threshold).astype(int)

        cm = confusion_matrix(y_arr, preds)
        if cm.shape == (2, 2):
            tn, fp, fn, tp = cm.ravel()
        else:
            tn, fp, fn, tp = (0, 0, 0, 0)

        # Specificity: TN / (TN + FP)
        specificity = float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0

        # PR-AUC
        prec_arr, rec_arr, _ = precision_recall_curve(y_arr, probs)
        pr_auc = float(auc(rec_arr, prec_arr))

        roc_auc = float(roc_auc_score(y_arr, probs))
        brier = float(brier_score_loss(y_arr, probs))
        ece = MultiTaskCalibrator.calculate_ece(y_arr, probs)
        citl = MultiTaskCalibrator.calculate_calibration_in_the_large(y_arr, probs)

        return {
            "accuracy": round(float(accuracy_score(y_arr, preds)), 4),
            "precision": round(float(precision_score(y_arr, preds, zero_division=0)), 4),
            "recall": round(float(recall_score(y_arr, preds, zero_division=0)), 4),
            "sensitivity": round(float(recall_score(y_arr, preds, zero_division=0)), 4),
            "specificity": round(specificity, 4),
            "f1_score": round(float(f1_score(y_arr, preds, zero_division=0)), 4),
            "roc_auc": round(roc_auc, 4),
            "pr_auc": round(pr_auc, 4),
            "brier_score": round(brier, 4),
            "ece": ece,
            "calibration_in_the_large": citl,
            "threshold_used": round(float(threshold), 2),
            "confusion_matrix": {
                "tp": int(tp), "fp": int(fp), "tn": int(tn), "fn": int(fn)
            }
        }

    @classmethod
    def evaluate_model_on_test_splits(
        cls,
        model: Any,
        test_splits: Dict[str, Tuple[pd.DataFrame, pd.Series]],
        calibrator: Optional[MultiTaskCalibrator] = None,
        thresholds: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """Evaluates the MTL model across all 3 held-out test sets."""
        th_dict = thresholds or {"t2d": 0.40, "cvd": 0.35, "ckd": 0.35}
        results = {}

        for disease in ["t2d", "cvd", "ckd"]:
            X_test, y_test = test_splits[disease]
            raw_probs = model.forward(X_test, training=False)[0][disease]

            if calibrator is not None and calibrator.calibrators[disease].is_fitted:
                calib_probs = calibrator.calibrators[disease].predict_proba(raw_probs)
            else:
                calib_probs = raw_probs

            th = th_dict.get(disease, 0.5)
            metrics = cls.evaluate_task_test_split(calib_probs, y_test, threshold=th)
            metrics["disease"] = disease.upper()
            metrics["model_architecture"] = "MultiTaskSharedEncoder"
            results[disease] = metrics

        return results

    # -------------------------------------------------------------------------
    # SUBGROUP FAIRNESS & PERFORMANCE ANALYSIS
    # -------------------------------------------------------------------------
    @classmethod
    def perform_subgroup_analysis(
        cls,
        model: Any,
        test_splits: Dict[str, Tuple[pd.DataFrame, pd.Series]],
        calibrator: Optional[MultiTaskCalibrator] = None,
        thresholds: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """Evaluates model performance across Age (<50 vs >=50) and Sex (Male vs Female) subgroups."""
        subgroup_results = {}
        th_dict = thresholds or {"t2d": 0.40, "cvd": 0.35, "ckd": 0.35}

        for disease in ["t2d", "cvd", "ckd"]:
            X_test, y_test = test_splits[disease]
            raw_probs = model.forward(X_test, training=False)[0][disease]
            if calibrator is not None and calibrator.calibrators[disease].is_fitted:
                probs = calibrator.calibrators[disease].predict_proba(raw_probs)
            else:
                probs = raw_probs

            th = th_dict.get(disease, 0.5)

            # Age subgroup (age_years feature normalized)
            # In RobustScaler, ~50 is near median 0.0
            age_raw = X_test["age_years"].values
            mask_young = age_raw < np.median(age_raw)
            mask_old = ~mask_young

            # Sex subgroup (gender feature: 1.0 male vs 0.0 female)
            gender_raw = X_test["gender"].values
            mask_male = gender_raw > np.median(gender_raw)
            mask_female = ~mask_male

            subgroup_results[disease] = {
                "age_under_50": cls.evaluate_task_test_split(probs[mask_young], y_test.values[mask_young], threshold=th) if np.sum(mask_young) > 5 else {},
                "age_50_and_above": cls.evaluate_task_test_split(probs[mask_old], y_test.values[mask_old], threshold=th) if np.sum(mask_old) > 5 else {},
                "sex_male": cls.evaluate_task_test_split(probs[mask_male], y_test.values[mask_male], threshold=th) if np.sum(mask_male) > 5 else {},
                "sex_female": cls.evaluate_task_test_split(probs[mask_female], y_test.values[mask_female], threshold=th) if np.sum(mask_female) > 5 else {}
            }

        return subgroup_results

    # -------------------------------------------------------------------------
    # DECISION CURVE ANALYSIS (DCA)
    # -------------------------------------------------------------------------
    @classmethod
    def compute_decision_curve_analysis(
        cls,
        probs: np.ndarray,
        y_true: np.ndarray,
        threshold_range: Optional[np.ndarray] = None
    ) -> Dict[str, List[float]]:
        """
        Computes Net Benefit across decision threshold probabilities:
        Net Benefit = (TP / N) - (FP / N) * (p_t / (1 - p_t))
        """
        if threshold_range is None:
            threshold_range = np.linspace(0.05, 0.85, 30)

        y_arr = np.asarray(y_true).astype(int)
        N = len(y_arr)
        event_rate = float(np.mean(y_arr))

        model_net_benefit = []
        treat_all_net_benefit = []
        treat_none_net_benefit = [0.0] * len(threshold_range)

        for pt in threshold_range:
            preds = (probs >= pt).astype(int)
            tp = float(np.sum((preds == 1) & (y_arr == 1)))
            fp = float(np.sum((preds == 1) & (y_arr == 0)))
            weight = pt / (1.0 - pt)

            nb_model = (tp / N) - (fp / N) * weight
            nb_all = event_rate - (1.0 - event_rate) * weight

            model_net_benefit.append(round(float(nb_model), 4))
            treat_all_net_benefit.append(round(float(nb_all), 4))

        return {
            "thresholds": [round(float(x), 4) for x in threshold_range],
            "model_net_benefit": model_net_benefit,
            "treat_all_net_benefit": treat_all_net_benefit,
            "treat_none_net_benefit": treat_none_net_benefit
        }

    # -------------------------------------------------------------------------
    # BASELINE MODEL COMPARISON
    # -------------------------------------------------------------------------
    @classmethod
    def train_and_evaluate_baselines(
        cls,
        train_splits: Dict[str, Tuple[pd.DataFrame, pd.Series]],
        test_splits: Dict[str, Tuple[pd.DataFrame, pd.Series]],
        random_seed: int = 42
    ) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Trains Logistic Regression, Random Forest, and XGBoost independently on the exact
        same training splits and evaluates on the exact same test splits.
        """
        baseline_results = {}

        for disease in ["t2d", "cvd", "ckd"]:
            X_tr, y_tr = train_splits[disease]
            X_te, y_te = test_splits[disease]

            baseline_results[disease] = {}

            # 1. Logistic Regression
            lr = LogisticRegression(C=1.0, class_weight="balanced", max_iter=1000, random_state=random_seed)
            lr.fit(X_tr, y_tr)
            p_lr = lr.predict_proba(X_te)[:, 1]
            baseline_results[disease]["Logistic Regression"] = cls.evaluate_task_test_split(p_lr, y_te, threshold=0.5)

            # 2. Random Forest
            rf = RandomForestClassifier(n_estimators=100, max_depth=8, class_weight="balanced", random_state=random_seed, n_jobs=-1)
            rf.fit(X_tr, y_tr)
            p_rf = rf.predict_proba(X_te)[:, 1]
            baseline_results[disease]["Random Forest"] = cls.evaluate_task_test_split(p_rf, y_te, threshold=0.5)

            # 3. XGBoost
            xgb_m = xgb.XGBClassifier(n_estimators=100, learning_rate=0.08, max_depth=5, eval_metric="logloss", random_state=random_seed, n_jobs=-1)
            xgb_m.fit(X_tr, y_tr)
            p_xgb = xgb_m.predict_proba(X_te)[:, 1]
            baseline_results[disease]["XGBoost"] = cls.evaluate_task_test_split(p_xgb, y_te, threshold=0.5)

        return baseline_results
