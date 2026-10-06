import pandas as pd
import numpy as np
import warnings
from typing import Dict, Any, List
from statsmodels.stats.outliers_influence import variance_inflation_factor

class DatasetProfilerService:

    @classmethod
    def generate_full_profile(cls, name: str, df: pd.DataFrame, target_col: str) -> Dict[str, Any]:
        num_rows, num_cols = df.shape
        
        # 1. Feature type detection
        features = [c for c in df.columns if c != target_col]
        numerical_features = []
        categorical_features = []
        binary_features = []
        id_features = []
        
        for col in features:
            if col.lower() == 'id':
                id_features.append(col)
                continue
            n_unique = df[col].nunique(dropna=True)
            is_num = pd.api.types.is_numeric_dtype(df[col])
            
            if is_num:
                if n_unique <= 2:
                    binary_features.append(col)
                elif n_unique < 10 and df[col].dtype != float:
                    categorical_features.append(col)
                else:
                    numerical_features.append(col)
            else:
                if n_unique <= 2:
                    binary_features.append(col)
                categorical_features.append(col)

        # 2. Missing Value Analysis
        missing_counts = df.isnull().sum().to_dict()
        missing_pcts = (df.isnull().sum() / num_rows * 100).to_dict()

        # 3. Duplicate Detection
        duplicate_rows = int(df.duplicated().sum())

        # 4. Statistical Profiling for Numerical Features
        summary_stats = {}
        for col in numerical_features + binary_features:
            if pd.api.types.is_numeric_dtype(df[col]):
                s = df[col].dropna()
                if len(s) > 0:
                    q1 = float(s.quantile(0.25))
                    q3 = float(s.quantile(0.75))
                    summary_stats[col] = {
                        "count": int(len(s)),
                        "mean": float(s.mean()),
                        "std": float(s.std()) if len(s) > 1 else 0.0,
                        "min": float(s.min()),
                        "q1": q1,
                        "median": float(s.median()),
                        "q3": q3,
                        "max": float(s.max()),
                        "iqr": float(q3 - q1),
                        "skewness": float(s.skew()) if len(s) > 2 else 0.0
                    }

        # 5. Categorical Distributions
        categorical_summary = {}
        for col in categorical_features:
            counts = df[col].value_counts(dropna=False).to_dict()
            total = len(df[col])
            categorical_summary[col] = {
                "unique_count": df[col].nunique(),
                "value_counts": {str(k): int(v) for k, v in counts.items()},
                "value_pcts": {str(k): float(v/total*100) for k, v in counts.items()}
            }

        # 6. Target Distribution Analysis
        target_series = df[target_col].dropna()
        target_counts = target_series.value_counts().to_dict()
        total_target = len(target_series)
        
        pos_key = 1 if 1 in target_counts else max(target_counts.keys(), key=lambda k: target_counts[k]) if target_counts else None
        neg_key = 0 if 0 in target_counts else [k for k in target_counts.keys() if k != pos_key][0] if len(target_counts) > 1 else None

        pos_count = int(target_counts.get(pos_key, 0))
        neg_count = int(target_counts.get(neg_key, 0))

        target_summary = {
            "target_name": target_col,
            "unique_values": [str(k) for k in target_counts.keys()],
            "positive_class": str(pos_key),
            "negative_class": str(neg_key),
            "positive_count": pos_count,
            "negative_count": neg_count,
            "positive_percentage": float(pos_count / total_target * 100) if total_target > 0 else 0.0,
            "negative_percentage": float(neg_count / total_target * 100) if total_target > 0 else 0.0,
            "imbalance_ratio": float(neg_count / pos_count) if pos_count > 0 else 0.0
        }

        # 7. Correlation Matrix for STRICTLY Numeric Features
        numeric_df = df[numerical_features + [b for b in binary_features if pd.api.types.is_numeric_dtype(df[b])]].dropna()
        if not numeric_df.empty and numeric_df.shape[1] > 1:
            corr_matrix = numeric_df.corr().round(4).to_dict()
        else:
            corr_matrix = {}

        return {
            "dataset_name": name,
            "num_rows": num_rows,
            "num_columns": num_cols,
            "target_column": target_col,
            "columns": df.columns.tolist(),
            "dtypes": {c: str(df[c].dtype) for c in df.columns},
            "numerical_features": numerical_features,
            "categorical_features": categorical_features,
            "binary_features": binary_features,
            "id_features": id_features,
            "missing_summary": {c: int(missing_counts[c]) for c in df.columns},
            "missing_pcts": {c: float(missing_pcts[c]) for c in df.columns},
            "duplicate_count": duplicate_rows,
            "duplicate_pct": float(duplicate_rows / num_rows * 100),
            "summary_stats": summary_stats,
            "categorical_summary": categorical_summary,
            "target_distribution": target_summary,
            "correlation_matrix": corr_matrix
        }

    @classmethod
    def calculate_vif(cls, df: pd.DataFrame, features: List[str]) -> Dict[str, float]:
        numeric_df = df[features].select_dtypes(include=[np.number]).dropna()
        numeric_df = numeric_df.loc[:, numeric_df.nunique() > 1]
        
        if numeric_df.empty or numeric_df.shape[1] < 2:
            return {}

        vif_data = {}
        vals = numeric_df.values
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for i, col in enumerate(numeric_df.columns):
                try:
                    vif = variance_inflation_factor(vals, i)
                    vif_val = float(vif)
                    if np.isinf(vif_val) or np.isnan(vif_val) or vif_val > 100.0:
                        vif_data[col] = 99.99
                    else:
                        vif_data[col] = round(vif_val, 2)
                except Exception:
                    vif_data[col] = 1.00

        return vif_data
