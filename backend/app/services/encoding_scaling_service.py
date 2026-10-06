import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, OrdinalEncoder

class EncodingScalingService:

    @classmethod
    def fit_encoders_and_scalers(
        cls,
        X_train: pd.DataFrame,
        encoding_strategy: str = "onehot",
        scaling_strategy: str = "standard"
    ) -> Tuple[Dict[str, Any], List[str], List[str]]:
        
        numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = X_train.select_dtypes(exclude=[np.number]).columns.tolist()

        artifacts = {}

        # 1. Fit Categorical Encoder
        if categorical_cols:
            if encoding_strategy == "onehot":
                encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
            else:
                encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
            encoder.fit(X_train[categorical_cols])
            artifacts["encoder"] = encoder
            artifacts["encoding_strategy"] = encoding_strategy

        # 2. Fit Scaler (strictly on training set)
        if numeric_cols:
            if scaling_strategy == "minmax":
                scaler = MinMaxScaler()
            else:
                scaler = StandardScaler()
            scaler.fit(X_train[numeric_cols])
            artifacts["scaler"] = scaler
            artifacts["scaling_strategy"] = scaling_strategy

        return artifacts, numeric_cols, categorical_cols

    @classmethod
    def transform_features(
        cls,
        X: pd.DataFrame,
        artifacts: Dict[str, Any],
        numeric_cols: List[str],
        categorical_cols: List[str]
    ) -> pd.DataFrame:
        X_out = X.copy()

        # 1. Apply Numerical Scaling
        if numeric_cols and "scaler" in artifacts:
            scaler = artifacts["scaler"]
            scaled_arr = scaler.transform(X_out[numeric_cols])
            X_scaled_df = pd.DataFrame(scaled_arr, columns=numeric_cols, index=X_out.index)
        else:
            X_scaled_df = X_out[numeric_cols].copy() if numeric_cols else pd.DataFrame(index=X_out.index)

        # 2. Apply Categorical Encoding
        if categorical_cols and "encoder" in artifacts:
            encoder = artifacts["encoder"]
            strategy = artifacts.get("encoding_strategy", "onehot")
            encoded_arr = encoder.transform(X_out[categorical_cols])
            
            if strategy == "onehot" and hasattr(encoder, 'get_feature_names_out'):
                feature_names = encoder.get_feature_names_out(categorical_cols)
                X_cat_df = pd.DataFrame(encoded_arr, columns=feature_names, index=X_out.index)
            else:
                X_cat_df = pd.DataFrame(encoded_arr, columns=categorical_cols, index=X_out.index)
        else:
            X_cat_df = pd.DataFrame(index=X_out.index)

        # Combine scaled numeric and encoded categorical features
        if X_scaled_df.empty:
            final_df = X_cat_df
        elif X_cat_df.empty:
            final_df = X_scaled_df
        else:
            final_df = pd.concat([X_scaled_df, X_cat_df], axis=1)

        return final_df
