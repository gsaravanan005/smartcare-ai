import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, accuracy_score
from .model_training_service import ModelTrainingService

class TuningCVService:

    @classmethod
    def evaluate_model_cv(
        cls,
        model_type: str,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        param_grid: Dict[str, List[Any]],
        n_splits: int = 5,
        random_seed: int = 42
    ) -> Dict[str, Any]:
        """
        Performs Stratified K-Fold CV and grid search over hyperparameter space.
        Executed strictly on the training set.
        """
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_seed)
        
        # Flatten grid search combinations
        param_combinations = cls._generate_param_combinations(param_grid)
        best_combo = None
        best_score = -1.0
        all_results = []

        for combo in param_combinations:
            cv_roc_aucs = []
            cv_recalls = []
            cv_f1s = []

            for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train)):
                X_tr, y_tr = X_train.iloc[train_idx], y_train.iloc[train_idx]
                X_va, y_va = X_train.iloc[val_idx], y_train.iloc[val_idx]

                if model_type == "logistic_regression":
                    model = ModelTrainingService.train_logistic_regression(
                        X_tr, y_tr,
                        c_val=combo.get('C', 1.0),
                        penalty=combo.get('penalty', 'l2'),
                        class_weight=combo.get('class_weight', 'balanced'),
                        random_seed=random_seed
                    )
                elif model_type == "random_forest":
                    model = ModelTrainingService.train_random_forest(
                        X_tr, y_tr,
                        n_estimators=combo.get('n_estimators', 100),
                        max_depth=combo.get('max_depth', 10),
                        min_samples_split=combo.get('min_samples_split', 5),
                        class_weight=combo.get('class_weight', 'balanced'),
                        random_seed=random_seed
                    )
                elif model_type == "xgboost":
                    model = ModelTrainingService.train_xgboost(
                        X_tr, y_tr,
                        n_estimators=combo.get('n_estimators', 100),
                        learning_rate=combo.get('learning_rate', 0.1),
                        max_depth=combo.get('max_depth', 6),
                        subsample=combo.get('subsample', 0.8),
                        random_seed=random_seed
                    )
                else:
                    raise ValueError(f"Unsupported model_type: {model_type}")

                y_prob = model.predict_proba(X_va)[:, 1]
                y_pred = (y_prob >= 0.5).astype(int)

                cv_roc_aucs.append(float(roc_auc_score(y_va, y_prob)))
                cv_recalls.append(float(recall_score(y_va, y_pred, zero_division=0)))
                cv_f1s.append(float(f1_score(y_va, y_pred, zero_division=0)))

            mean_roc = float(np.mean(cv_roc_aucs))
            std_roc = float(np.std(cv_roc_aucs))
            mean_recall = float(np.mean(cv_recalls))
            mean_f1 = float(np.mean(cv_f1s))

            combo_res = {
                "parameters": combo,
                "mean_roc_auc": mean_roc,
                "std_roc_auc": std_roc,
                "mean_recall": mean_recall,
                "mean_f1": mean_f1,
                "fold_roc_aucs": cv_roc_aucs
            }
            all_results.append(combo_res)

            # Prioritize ROC-AUC with recall tie-breaker
            score = mean_roc * 0.7 + mean_recall * 0.3
            if score > best_score:
                best_score = score
                best_combo = combo_res

        return {
            "model_type": model_type,
            "best_parameters": best_combo["parameters"],
            "best_cv_roc_auc": best_combo["mean_roc_auc"],
            "best_cv_std": best_combo["std_roc_auc"],
            "best_cv_recall": best_combo["mean_recall"],
            "best_cv_f1": best_combo["mean_f1"],
            "all_combinations_tested": len(all_results)
        }

    @classmethod
    def _generate_param_combinations(cls, param_grid: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
        import itertools
        keys = param_grid.keys()
        values = param_grid.values()
        combinations = []
        for instance in itertools.product(*values):
            combinations.append(dict(zip(keys, instance)))
        return combinations
