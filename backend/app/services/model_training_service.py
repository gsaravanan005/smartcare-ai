import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List, Optional
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import xgboost as xgb

class ModelTrainingService:

    @classmethod
    def train_logistic_regression(
        cls,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        C: float = 1.0,
        class_weight: str = 'balanced',
        random_seed: int = 42,
        **kwargs
    ) -> LogisticRegression:
        c_value = kwargs.get('c_val', C)
        model = LogisticRegression(
            C=c_value,
            class_weight=class_weight if class_weight != 'none' else None,
            solver='liblinear',
            random_state=random_seed,
            max_iter=1000
        )
        model.fit(X_train, y_train)
        return model

    @classmethod
    def train_random_forest(
        cls,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        n_estimators: int = 100,
        max_depth: Optional[int] = 10,
        min_samples_split: int = 5,
        min_samples_leaf: int = 2,
        class_weight: str = 'balanced',
        random_seed: int = 42,
        **kwargs
    ) -> RandomForestClassifier:
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            class_weight=class_weight if class_weight != 'none' else None,
            random_state=random_seed,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        return model

    @classmethod
    def train_xgboost(
        cls,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 6,
        subsample: float = 0.8,
        colsample_bytree: float = 0.8,
        scale_pos_weight: float = 1.0,
        random_seed: int = 42,
        **kwargs
    ) -> xgb.XGBClassifier:
        model = xgb.XGBClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            subsample=subsample,
            colsample_bytree=colsample_bytree,
            scale_pos_weight=scale_pos_weight,
            random_state=random_seed,
            eval_metric='logloss',
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        return model

    @classmethod
    def train_multitask_neural_network(
        cls,
        X_train_shared: pd.DataFrame,
        Y_train_multi: np.ndarray,
        hidden_layer_sizes: Tuple[int, ...] = (64, 32),
        learning_rate_init: float = 0.001,
        max_iter: int = 300,
        random_seed: int = 42,
        **kwargs
    ) -> MLPClassifier:
        model = MLPClassifier(
            hidden_layer_sizes=hidden_layer_sizes,
            activation='relu',
            solver='adam',
            learning_rate_init=learning_rate_init,
            max_iter=max_iter,
            random_state=random_seed,
            early_stopping=True,
            n_iter_no_change=10
        )
        model.fit(X_train_shared, Y_train_multi)
        return model
