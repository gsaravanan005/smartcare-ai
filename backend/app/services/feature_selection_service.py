import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif, RFE
from sklearn.ensemble import RandomForestClassifier

class FeatureSelectionService:

    @classmethod
    def fit_feature_selector(
        cls,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        method: str = "select_k_best",
        k: int = 15,
        corr_threshold: float = 0.85
    ) -> Dict[str, Any]:
        """
        Fits feature selection strictly on training data.
        """
        all_features = X_train.columns.tolist()
        
        # 1. Remove constant features first
        variances = X_train.var()
        non_constant_cols = variances[variances > 0.0001].index.tolist()
        if not non_constant_cols:
            non_constant_cols = all_features

        X_train_filtered = X_train[non_constant_cols].fillna(0)

        # 2. Multicollinearity / High-correlation filtering
        corr_matrix = X_train_filtered.corr().abs()
        upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        high_corr_cols = [column for column in upper_tri.columns if any(upper_tri[column] > corr_threshold)]
        
        usable_cols = [c for c in non_constant_cols if c not in high_corr_cols]
        if len(usable_cols) < max(5, k):
            usable_cols = non_constant_cols # Keep all if filtering drops too many

        num_features = min(k, len(usable_cols))
        
        # 3. Apply Selection Method
        if method == "mutual_info":
            selector = SelectKBest(score_func=mutual_info_classif, k=num_features)
            selector.fit(X_train_filtered[usable_cols], y_train)
            selected_idx = selector.get_support(indices=True)
            selected_features = [usable_cols[i] for i in selected_idx]

        elif method == "rfe":
            estimator = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
            selector = RFE(estimator=estimator, n_features_to_select=num_features, step=1)
            selector.fit(X_train_filtered[usable_cols], y_train)
            selected_features = [usable_cols[i] for i, supp in enumerate(selector.support_) if supp]

        elif method == "all":
            selected_features = usable_cols
            selector = None

        else: # Default: SelectKBest with f_classif (ANOVA)
            selector = SelectKBest(score_func=f_classif, k=num_features)
            selector.fit(X_train_filtered[usable_cols], y_train)
            selected_idx = selector.get_support(indices=True)
            selected_features = [usable_cols[i] for i in selected_idx]

        removed_features = [f for f in all_features if f not in selected_features]

        return {
            "method": method,
            "k": num_features,
            "selected_features": selected_features,
            "removed_features": removed_features,
            "high_corr_removed": high_corr_cols,
            "selector": selector
        }

    @classmethod
    def transform_features(cls, X: pd.DataFrame, selector_artifacts: Dict[str, Any]) -> pd.DataFrame:
        selected_features = selector_artifacts["selected_features"]
        # Retain only selected features present in X
        available_cols = [c for c in selected_features if c in X.columns]
        return X[available_cols].copy()
