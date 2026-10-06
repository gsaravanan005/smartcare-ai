import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List, Optional

class OutlierService:

    @classmethod
    def fit_outlier_bounds(cls, X_train: pd.DataFrame, method: str = "iqr", factor: float = 1.5) -> Dict[str, Tuple[float, float]]:
        numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
        bounds = {}
        
        for col in numeric_cols:
            s = X_train[col].dropna()
            if len(s) == 0:
                continue
                
            if method == "iqr":
                q1 = s.quantile(0.25)
                q3 = s.quantile(0.75)
                iqr = q3 - q1
                lower = q1 - factor * iqr
                upper = q3 + factor * iqr
            elif method == "zscore":
                mean = s.mean()
                std = s.std()
                lower = mean - factor * std
                upper = mean + factor * std
            else: # Default IQR
                q1 = s.quantile(0.25)
                q3 = s.quantile(0.75)
                iqr = q3 - q1
                lower = q1 - factor * iqr
                upper = q3 + factor * iqr

            # Domain specific boundary constraints (e.g. non-negative for physiological measures)
            if col in ['age', 'height', 'weight', 'ap_hi', 'ap_lo', 'glucose', 'serum_creatinine', 'bu', 'sc', 'sod', 'pot', 'hemo', 'BMI']:
                lower = max(0.0, lower)

            bounds[col] = (float(lower), float(upper))

        return bounds

    @classmethod
    def apply_outlier_treatment(
        cls,
        X: pd.DataFrame,
        bounds: Dict[str, Tuple[float, float]],
        strategy: str = "iqr_capping"
    ) -> Tuple[pd.DataFrame, Dict[str, int]]:
        X_out = X.copy()
        outlier_counts = {}

        if strategy in ["iqr_capping", "zscore_capping", "capping"]:
            for col, (lower, upper) in bounds.items():
                if col in X_out.columns:
                    outliers_mask = (X_out[col] < lower) | (X_out[col] > upper)
                    outlier_counts[col] = int(outliers_mask.sum())
                    X_out[col] = np.clip(X_out[col], lower, upper)

        elif strategy == "removal":
            mask = pd.Series(True, index=X_out.index)
            for col, (lower, upper) in bounds.items():
                if col in X_out.columns:
                    col_mask = (X_out[col] >= lower) & (X_out[col] <= upper)
                    outlier_counts[col] = int((~col_mask).sum())
                    mask = mask & col_mask
            X_out = X_out[mask]

        elif strategy == "log_transform":
            for col, (lower, upper) in bounds.items():
                if col in X_out.columns and (X_out[col] > 0).all():
                    outliers_mask = (X_out[col] < lower) | (X_out[col] > upper)
                    outlier_counts[col] = int(outliers_mask.sum())
                    X_out[col] = np.log1p(X_out[col])

        else: # Keep as is
            for col, (lower, upper) in bounds.items():
                if col in X_out.columns:
                    outliers_mask = (X_out[col] < lower) | (X_out[col] > upper)
                    outlier_counts[col] = int(outliers_mask.sum())

        return X_out, outlier_counts
