import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any
from sklearn.utils.class_weight import compute_class_weight

class ImbalanceService:

    @classmethod
    def analyze_distribution(cls, y: pd.Series) -> Dict[str, Any]:
        counts = y.value_counts().to_dict()
        total = len(y)
        pos = counts.get(1, 0)
        neg = counts.get(0, 0)
        return {
            "total_samples": total,
            "positive_samples": int(pos),
            "negative_samples": int(neg),
            "positive_pct": float(pos / total * 100) if total > 0 else 0.0,
            "negative_pct": float(neg / total * 100) if total > 0 else 0.0,
            "imbalance_ratio": float(neg / pos) if pos > 0 else 0.0
        }

    @classmethod
    def apply_imbalance_handling(
        cls,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        method: str = "smote",
        random_seed: int = 42
    ) -> Tuple[pd.DataFrame, pd.Series, Dict[str, Any]]:
        """
        Executed ONLY on training split to prevent data leakage.
        """
        orig_dist = cls.analyze_distribution(y_train)

        if method == "smote":
            try:
                from imblearn.over_sampling import SMOTE
                smote = SMOTE(random_state=random_seed)
                X_res, y_res = smote.fit_resample(X_train.fillna(0), y_train)
                X_res = pd.DataFrame(X_res, columns=X_train.columns)
                y_res = pd.Series(y_res, name=y_train.name)
            except ImportError:
                # Fallback to random oversampling if imblearn not available
                X_res, y_res = cls._random_oversample(X_train, y_train, random_seed)

        elif method == "oversampling":
            X_res, y_res = cls._random_oversample(X_train, y_train, random_seed)

        elif method == "undersampling":
            X_res, y_res = cls._random_undersample(X_train, y_train, random_seed)

        elif method == "class_weights":
            # Compute class weights without altering dataset rows
            classes = np.unique(y_train)
            weights = compute_class_weight(class_weight="balanced", classes=classes, y=y_train)
            class_weight_dict = {int(c): float(w) for c, w in zip(classes, weights)}
            return X_train.copy(), y_train.copy(), {
                "method": "class_weights",
                "class_weights": class_weight_dict,
                "original_distribution": orig_dist,
                "new_distribution": orig_dist
            }

        else: # None / keep original
            X_res, y_res = X_train.copy(), y_train.copy()

        new_dist = cls.analyze_distribution(y_res)
        return X_res, y_res, {
            "method": method,
            "original_distribution": orig_dist,
            "new_distribution": new_dist
        }

    @classmethod
    def _random_oversample(cls, X: pd.DataFrame, y: pd.Series, seed: int) -> Tuple[pd.DataFrame, pd.Series]:
        np.random.seed(seed)
        counts = y.value_counts()
        max_count = counts.max()
        
        df_concat = pd.concat([X, y], axis=1)
        resampled_dfs = []
        
        for class_val, count in counts.items():
            class_df = df_concat[df_concat[y.name] == class_val]
            if count < max_count:
                extra = class_df.sample(n=max_count - count, replace=True, random_state=seed)
                class_df = pd.concat([class_df, extra], axis=0)
            resampled_dfs.append(class_df)

        final_df = pd.concat(resampled_dfs, axis=0).sample(frac=1, random_state=seed).reset_index(drop=True)
        return final_df.drop(columns=[y.name]), final_df[y.name]

    @classmethod
    def _random_undersample(cls, X: pd.DataFrame, y: pd.Series, seed: int) -> Tuple[pd.DataFrame, pd.Series]:
        np.random.seed(seed)
        counts = y.value_counts()
        min_count = counts.min()
        
        df_concat = pd.concat([X, y], axis=1)
        resampled_dfs = []
        
        for class_val, count in counts.items():
            class_df = df_concat[df_concat[y.name] == class_val].sample(n=min_count, replace=False, random_state=seed)
            resampled_dfs.append(class_df)

        final_df = pd.concat(resampled_dfs, axis=0).sample(frac=1, random_state=seed).reset_index(drop=True)
        return final_df.drop(columns=[y.name]), final_df[y.name]
