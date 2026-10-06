import numpy as np
import pandas as pd
from typing import Dict, Any, List
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, precision_recall_curve, auc, confusion_matrix, brier_score_loss
)

class ExperimentComparisonService:

    @classmethod
    def evaluate_binary_classifier(
        cls,
        model: Any,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        threshold: float = 0.5
    ) -> Dict[str, Any]:
        """
        Evaluates a model once on the isolated test set.
        Returns complete metrics dictionary including Confusion Matrix and ROC/PR AUC.
        """
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X_test)[:, 1]
        elif hasattr(model, "decision_function"):
            df = model.decision_function(X_test)
            probs = 1.0 / (1.0 + np.exp(-df))
        else:
            probs = model.predict(X_test)

        preds = (probs >= threshold).astype(int)

        cm = confusion_matrix(y_test, preds)
        tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)

        # Precision-Recall curve AUC
        prec_arr, rec_arr, _ = precision_recall_curve(y_test, probs)
        pr_auc = float(auc(rec_arr, prec_arr))

        roc_auc = float(roc_auc_score(y_test, probs))
        brier = float(brier_score_loss(y_test, probs))

        return {
            "accuracy": round(float(accuracy_score(y_test, preds)), 4),
            "precision": round(float(precision_score(y_test, preds, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, preds, zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_test, preds, zero_division=0)), 4),
            "roc_auc": round(roc_auc, 4),
            "pr_auc": round(pr_auc, 4),
            "brier_score": round(brier, 4),
            "threshold_used": round(float(threshold), 2),
            "confusion_matrix": {
                "tp": int(tp),
                "fp": int(fp),
                "tn": int(tn),
                "fn": int(fn)
            }
        }

    @classmethod
    def build_comparison_report(
        cls,
        independent_results: Dict[str, Dict[str, Any]],
        multitask_results: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generates a comparative analysis table between Independent Disease Models
        and Multi-Task Shared Representation Architecture.
        """
        summary_rows = []
        for disease in ["diabetes", "cardio", "ckd"]:
            ind = independent_results.get(disease, {})
            mt = multitask_results.get(disease, {})

            ind_roc = ind.get("roc_auc", 0.0)
            mt_roc = mt.get("roc_auc", 0.0)
            winner = "Multi-Task" if mt_roc > ind_roc + 0.005 else "Independent" if ind_roc > mt_roc + 0.005 else "Comparable"

            summary_rows.append({
                "disease": disease.upper(),
                "independent_model": ind.get("model_type", "Best Independent"),
                "independent_roc_auc": ind_roc,
                "independent_recall": ind.get("recall", 0.0),
                "independent_f1": ind.get("f1_score", 0.0),
                "multitask_roc_auc": mt_roc,
                "multitask_recall": mt.get("recall", 0.0),
                "multitask_f1": mt.get("f1_score", 0.0),
                "winning_architecture": winner
            })

        return {
            "comparison_table": summary_rows,
            "conclusion_summary": "Empirical comparison completed. Disease models selected based on validation ROC-AUC and Recall trade-offs."
        }
