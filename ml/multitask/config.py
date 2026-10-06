"""
SmartCare AI - Multi-Task Learning Configuration
Defines hyperparameters, feature schema, task weights, and paths.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple
import os

@dataclass
class MTLConfig:
    # Feature Schema Definitions (Exactly 30 unified features in deterministic order)
    DEMOGRAPHIC_FEATURES: List[str] = field(default_factory=lambda: [
        "age_years", "gender", "education", "income"
    ])
    VITAL_FEATURES: List[str] = field(default_factory=lambda: [
        "bmi", "high_bp", "ap_hi", "ap_lo", "pulse_pressure", "mean_arterial_pressure"
    ])
    LABORATORY_FEATURES: List[str] = field(default_factory=lambda: [
        "cholesterol", "glucose", "serum_creatinine", "blood_urea", "hemoglobin",
        "albumin_level", "specific_gravity", "bun_creatinine_ratio", "egfr_proxy", "anemia_flag"
    ])
    LIFESTYLE_FEATURES: List[str] = field(default_factory=lambda: [
        "smoker", "phys_activity", "alcohol_consumption", "fruits", "veggies"
    ])
    HISTORY_FEATURES: List[str] = field(default_factory=lambda: [
        "heart_disease_or_attack", "stroke", "diff_walk", "gen_hlth", "combined_vascular_risk"
    ])

    @property
    def all_features(self) -> List[str]:
        feats = (
            self.DEMOGRAPHIC_FEATURES
            + self.VITAL_FEATURES
            + self.LABORATORY_FEATURES
            + self.LIFESTYLE_FEATURES
            + self.HISTORY_FEATURES
        )
        assert len(feats) == 30, f"Expected exactly 30 features, got {len(feats)}"
        return feats

    @property
    def input_dim(self) -> int:
        return len(self.all_features)
    shared_hidden_dims: Tuple[int, ...] = (64, 32)
    task_hidden_dim: int = 16
    dropout_rate: float = 0.15
    use_batch_norm: bool = True
    l2_reg: float = 1e-4

    # Optimization Hyperparameters
    learning_rate: float = 0.002
    lr_decay_step: int = 20
    lr_decay_gamma: float = 0.8
    batch_size: int = 256
    epochs: int = 60
    early_stopping_patience: int = 10
    random_seed: int = 42

    # Task Loss Weights (w_T2D, w_CVD, w_CKD)
    # Balanced to ensure CKD contributes meaningfully without being overwhelmed
    task_weights: Dict[str, float] = field(default_factory=lambda: {
        "t2d": 1.0,
        "cvd": 1.0,
        "ckd": 2.5
    })

    # CKD Oversampling factor in multi-task mini-batches to balance dataset sizes
    ckd_batch_sample_ratio: float = 0.20  # ~20% of mini-batch draws from CKD cohort

    # Initial and Optimized Decision Thresholds
    default_thresholds: Dict[str, float] = field(default_factory=lambda: {
        "t2d": 0.40,
        "cvd": 0.35,
        "ckd": 0.35
    })

    # File Paths
    artifacts_dir: str = os.path.abspath("artifacts")
    models_dir: str = os.path.abspath("models/multitask")
    processed_data_dir: str = os.path.abspath("data/processed")
    raw_data_dir: str = os.path.abspath("data/raw")
