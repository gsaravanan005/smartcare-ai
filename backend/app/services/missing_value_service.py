import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional, List
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

class MissingValueService:

    @classmethod
    def analyze_missingness_patterns(cls, df: pd.DataFrame) -> Dict[str, Any]:
        null_counts = df.isnull().sum()
        cols_with_missing = null_counts[null_counts > 0]
        
        missing_matrix = df.isnull()
        co_occurrence = missing_matrix.T.dot(missing_matrix)
        
        total_rows = len(df)
        complete_cases = int(df.dropna().shape[0])
        rows_with_missing = total_rows - complete_cases
        
        pattern_notes = []
        if len(cols_with_missing) == 0:
            pattern_notes.append("No missing values detected in dataset.")
        else:
            pattern_notes.append(f"{len(cols_with_missing)} features contain missing values.")
            pattern_notes.append(f"{rows_with_missing} out of {total_rows} records ({rows_with_missing/total_rows*100:.2f}%) contain at least one missing value.")
            
        return {
            "features_with_missing": cols_with_missing.to_dict(),
            "complete_cases": complete_cases,
            "rows_with_missing": rows_with_missing,
            "rows_with_missing_pct": float(rows_with_missing / total_rows * 100) if total_rows > 0 else 0.0,
            "co_occurrence_matrix": co_occurrence.to_dict(),
            "pattern_notes": pattern_notes
        }

    @classmethod
    def inject_controlled_missingness(
        cls,
        df: pd.DataFrame,
        scenario: str = "scenario_a",
        rate: float = 0.10,
        random_seed: int = 42
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        np.random.seed(random_seed)
        df_injected = df.copy()
        
        candidate_cols = [c for c in df_injected.columns if c.lower() not in ['id', 'diabetes_binary', 'cardio', 'classification']]
        numeric_cols = df_injected[candidate_cols].select_dtypes(include=[np.number]).columns.tolist()
        
        total_injected = 0
        injected_details = {}

        if scenario == "scenario_a":
            target_cols = np.random.choice(numeric_cols, size=max(1, len(numeric_cols)//4), replace=False)
            for col in target_cols:
                mask = np.random.rand(len(df_injected)) < rate
                df_injected.loc[mask, col] = np.nan
                cnt = int(mask.sum())
                total_injected += cnt
                injected_details[col] = cnt

        elif scenario == "scenario_b":
            high_rate = min(rate * 1.5, 0.30)
            target_cols = np.random.choice(numeric_cols, size=max(1, len(numeric_cols)//3), replace=False)
            for col in target_cols:
                mask = np.random.rand(len(df_injected)) < high_rate
                df_injected.loc[mask, col] = np.nan
                cnt = int(mask.sum())
                total_injected += cnt
                injected_details[col] = cnt

        elif scenario == "scenario_c":
            target_cols = np.random.choice(numeric_cols, size=max(1, len(numeric_cols)//2), replace=False)
            for col in target_cols:
                mask = np.random.rand(len(df_injected)) < rate
                df_injected.loc[mask, col] = np.nan
                cnt = int(mask.sum())
                total_injected += cnt
                injected_details[col] = cnt

        elif scenario == "scenario_d":
            target_cols = [c for c in numeric_cols if c in ['ap_hi', 'ap_lo', 'glucose', 'serum_creatinine', 'blood_urea', 'sc', 'bu', 'hemo', 'BMI', 'GenHlth']]
            if not target_cols:
                target_cols = numeric_cols[:3]
            for col in target_cols:
                mask = np.random.rand(len(df_injected)) < rate
                df_injected.loc[mask, col] = np.nan
                cnt = int(mask.sum())
                total_injected += cnt
                injected_details[col] = cnt

        experiment_info = {
            "scenario": scenario,
            "rate": rate,
            "random_seed": random_seed,
            "total_values_removed": total_injected,
            "injected_details": injected_details
        }

        return df_injected, experiment_info

    @classmethod
    def fit_imputer(cls, X_train: pd.DataFrame, method: str = "median") -> Tuple[Any, List[str], List[str]]:
        numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = X_train.select_dtypes(exclude=[np.number]).columns.tolist()

        if method == "mean":
            imputer = SimpleImputer(strategy="mean")
        elif method == "median":
            imputer = SimpleImputer(strategy="median")
        elif method == "mode" or method == "most_frequent":
            imputer = SimpleImputer(strategy="most_frequent")
        elif method == "knn":
            imputer = KNNImputer(n_neighbors=5)
        elif method == "iterative" or method == "mice":
            imputer = IterativeImputer(random_state=42, max_iter=10)
        else:
            imputer = SimpleImputer(strategy="median")

        if numeric_cols:
            imputer.fit(X_train[numeric_cols])

        return imputer, numeric_cols, categorical_cols

    @classmethod
    def transform_imputation(cls, imputer: Any, X: pd.DataFrame, numeric_cols: List[str], categorical_cols: List[str]) -> pd.DataFrame:
        X_out = X.copy()
        
        # Ensure all numeric columns exist
        available_num_cols = [c for c in numeric_cols if c in X_out.columns]
        missing_num_cols = [c for c in numeric_cols if c not in X_out.columns]
        for mc in missing_num_cols:
            X_out[mc] = 0.0

        if numeric_cols and hasattr(imputer, 'transform'):
            imputed_arr = imputer.transform(X_out[numeric_cols])
            X_out[numeric_cols] = pd.DataFrame(imputed_arr, columns=numeric_cols, index=X_out.index)
        
        for c in categorical_cols:
            if c not in X_out.columns:
                X_out[c] = "normal"
            elif X_out[c].isnull().sum() > 0:
                mode_val = X_out[c].mode()[0] if not X_out[c].mode().empty else "normal"
                X_out[c] = X_out[c].fillna(mode_val)

        return X_out
