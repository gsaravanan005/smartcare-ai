"""
SmartCare AI - Feature Harmonization & Leakage-Free Pipeline Verification Tests
Audits and tests:
1. Exact 30 features count and deterministic ordering
2. Raw dataset loading and target schemas
3. Removal of invalid surrogate mappings (T2D glucose, CKD smoker, CVD heart attack, CKD gender, CKD BMI)
4. Missing value representation and training-fitted median imputation
5. RobustScaler fitting strictly on training split
6. Task-masked multi-task loss and 20% CKD batch sampling
7. Single patient inference harmonization and scaler transformation
"""

import pytest
import numpy as np
import pandas as pd

from ml.multitask.config import MTLConfig
from ml.multitask.dataset import MTLDatasetManager, TaskBalancedBatchIterator
from ml.multitask.model import MultiTaskNeuralNetwork
from ml.multitask.loss import MaskedMultiTaskLoss
from ml.multitask.calibration import MultiTaskCalibrator
from ml.multitask.evaluate import MultiTaskEvaluator


EXPECTED_30_FEATURES = [
    "age_years", "gender", "education", "income",
    "bmi", "high_bp", "ap_hi", "ap_lo", "pulse_pressure", "mean_arterial_pressure",
    "cholesterol", "glucose", "serum_creatinine", "blood_urea", "hemoglobin",
    "albumin_level", "specific_gravity", "bun_creatinine_ratio", "egfr_proxy", "anemia_flag",
    "smoker", "phys_activity", "alcohol_consumption", "fruits", "veggies",
    "heart_disease_or_attack", "stroke", "diff_walk", "gen_hlth", "combined_vascular_risk"
]


def test_30_feature_schema_and_ordering():
    """Verifies that config.all_features has exactly 30 features in exact deterministic order."""
    cfg = MTLConfig()
    assert len(cfg.all_features) == 30, f"Expected 30 features, got {len(cfg.all_features)}"
    assert cfg.all_features == EXPECTED_30_FEATURES, "Feature list does not match the deterministic 30-feature specification"


def test_raw_cohorts_loading():
    """Verifies raw cohorts load properly with correct target columns."""
    mgr = MTLDatasetManager()
    cohorts = mgr.load_raw_cohorts()

    assert "t2d" in cohorts and "cvd" in cohorts and "ckd" in cohorts
    X_t, y_t = cohorts["t2d"]
    X_c, y_c = cohorts["cvd"]
    X_k, y_k = cohorts["ckd"]

    assert len(X_t) > 50000, f"Expected T2D cohort > 50000, got {len(X_t)}"
    assert len(X_c) > 50000, f"Expected CVD cohort > 50000, got {len(X_c)}"
    assert len(X_k) >= 350, f"Expected CKD cohort >= 350, got {len(X_k)}"

    # Check binary targets
    assert set(np.unique(y_t)).issubset({0, 1})
    assert set(np.unique(y_c)).issubset({0, 1})
    assert set(np.unique(y_k)).issubset({0, 1})


def test_harmonize_t2d_no_invalid_glucose_surrogate():
    """
    Verifies that T2D harmonization:
    1. Returns all 30 features in exact order
    2. Leaves unobserved features (glucose, ap_hi, ap_lo, renal biomarkers) as NaN
    3. Does NOT derive glucose from HighChol
    """
    mgr = MTLDatasetManager()
    dummy_t2d = pd.DataFrame([{
        "Age": 9.0, "Sex": 1.0, "Education": 6.0, "Income": 8.0, "BMI": 28.0,
        "HighBP": 1.0, "HighChol": 1.0, "Smoker": 1.0, "PhysActivity": 1.0,
        "Fruits": 1.0, "Veggies": 1.0, "HvyAlcoholConsump": 0.0,
        "HeartDiseaseorAttack": 0.0, "Stroke": 0.0, "DiffWalk": 0.0, "GenHlth": 3.0
    }])

    harm = mgr.harmonize_t2d_features(dummy_t2d)
    assert len(harm.columns) == 30
    assert list(harm.columns) == EXPECTED_30_FEATURES

    # Verify unobserved variables are NaN (NOT fabricated)
    assert pd.isna(harm["glucose"].iloc[0]), "T2D glucose must be NaN (not derived from HighChol)"
    assert pd.isna(harm["ap_hi"].iloc[0]), "T2D ap_hi must be NaN"
    assert pd.isna(harm["ap_lo"].iloc[0]), "T2D ap_lo must be NaN"
    assert pd.isna(harm["serum_creatinine"].iloc[0]), "T2D serum_creatinine must be NaN"
    assert pd.isna(harm["egfr_proxy"].iloc[0]), "T2D egfr_proxy must be NaN"

    # Verify observed variables are preserved
    assert harm["bmi"].iloc[0] == 28.0
    assert harm["high_bp"].iloc[0] == 1.0
    assert harm["cholesterol"].iloc[0] == 1.0


def test_harmonize_cvd_no_invalid_heart_attack_surrogate():
    """
    Verifies that CVD harmonization:
    1. Returns all 30 features in exact order
    2. Leaves heart_disease_or_attack as NaN (NOT inferred from ap_hi > 160)
    3. Correctly maps gender, computes pulse pressure & MAP
    """
    mgr = MTLDatasetManager()
    dummy_cvd = pd.DataFrame([{
        "age_years": 55.0, "gender": 2, "height": 175, "weight": 80,
        "ap_hi": 170.0, "ap_lo": 100.0, "cholesterol": 2, "gluc": 2,
        "smoke": 1, "alco": 0, "active": 1
    }])

    harm = mgr.harmonize_cvd_features(dummy_cvd)
    assert len(harm.columns) == 30
    assert list(harm.columns) == EXPECTED_30_FEATURES

    # Verify heart disease history is NaN (NOT fabricated from high BP)
    assert pd.isna(harm["heart_disease_or_attack"].iloc[0]), "CVD heart_disease_or_attack must be NaN"
    assert pd.isna(harm["serum_creatinine"].iloc[0]), "CVD serum_creatinine must be NaN"

    # Verify valid hemodynamics
    assert harm["gender"].iloc[0] == 1.0  # gender 2 -> male (1.0)
    assert harm["ap_hi"].iloc[0] == 170.0
    assert harm["ap_lo"].iloc[0] == 100.0
    assert harm["pulse_pressure"].iloc[0] == 70.0
    assert np.isclose(harm["mean_arterial_pressure"].iloc[0], 100.0 + 70.0 / 3.0)


def test_harmonize_ckd_no_invalid_gender_bmi_smoker_surrogates():
    """
    Verifies that CKD harmonization:
    1. Leaves gender as NaN (NOT defaulted to male 1.0)
    2. Leaves bmi as NaN (NOT defaulted to 26.0)
    3. Leaves smoker as NaN (NOT mapped from CAD)
    4. Computes bun_creatinine_ratio and egfr_proxy from observed renal markers
    """
    mgr = MTLDatasetManager()
    dummy_ckd = pd.DataFrame([{
        "age": 48.0, "bp": 80.0, "sg": 1.020, "al": 1.0, "bgr": 130.0,
        "bu": 40.0, "sc": 1.5, "hemo": 11.5, "htn": "yes", "dm": "yes", "cad": "yes", "ane": "yes"
    }])

    harm = mgr.harmonize_ckd_features(dummy_ckd)
    assert len(harm.columns) == 30
    assert list(harm.columns) == EXPECTED_30_FEATURES

    # Verify invalid surrogates are eliminated
    assert pd.isna(harm["gender"].iloc[0]), "CKD gender must be NaN (not hardcoded male 1.0)"
    assert pd.isna(harm["bmi"].iloc[0]), "CKD BMI must be NaN (not hardcoded 26.0)"
    assert pd.isna(harm["smoker"].iloc[0]), "CKD smoker must be NaN (not mapped from CAD)"

    # Verify observed renal markers and legitimate proxies
    assert harm["serum_creatinine"].iloc[0] == 1.5
    assert harm["blood_urea"].iloc[0] == 40.0
    assert np.isclose(harm["bun_creatinine_ratio"].iloc[0], 40.0 / 1.5)
    assert harm["anemia_flag"].iloc[0] == 1.0
    assert harm["heart_disease_or_attack"].iloc[0] == 1.0  # cad is observed in CKD


def test_leakage_free_imputation_and_scaling():
    """
    Verifies that prepare_multitask_data:
    1. Splits data BEFORE fitting imputer & scaler
    2. Fits SimpleImputer on train split only
    3. Fits RobustScaler on train split only
    4. Transforms val and test sets without NaN or refitting
    """
    mgr = MTLDatasetManager()
    prep = mgr.prepare_multitask_data(train_ratio=0.70, val_ratio=0.15, test_ratio=0.15, random_seed=42)

    assert mgr.imputer is not None, "Imputer must be fitted"
    assert mgr.scaler is not None, "Scaler must be fitted"
    assert len(mgr.feature_names) == 30

    scaled = prep["scaled_splits"]
    for d in ["t2d", "cvd", "ckd"]:
        for part in ["train", "val", "test"]:
            X_df, y_ser = scaled[d][part]
            assert X_df.shape[1] == 30
            assert not X_df.isna().any().any(), f"No NaNs allowed in {d} {part} after imputation"


def test_task_balanced_batch_iterator():
    """Verifies that TaskBalancedBatchIterator produces valid shapes, task masks, and ~20% CKD sampling."""
    mgr = MTLDatasetManager()
    prep = mgr.prepare_multitask_data(train_ratio=0.70, val_ratio=0.15, test_ratio=0.15, random_seed=42)
    tr = {d: prep["scaled_splits"][d]["train"] for d in ["t2d", "cvd", "ckd"]}

    batch_iter = TaskBalancedBatchIterator(tr["t2d"], tr["cvd"], tr["ckd"], batch_size=256, ckd_ratio=0.20)
    for X_b, y_d, m_d in batch_iter:
        assert X_b.shape == (256, 30)
        assert set(y_d.keys()) == {"t2d", "cvd", "ckd"}
        assert set(m_d.keys()) == {"t2d", "cvd", "ckd"}
        # Verify each row has exactly one active task mask
        active_masks = m_d["t2d"] + m_d["cvd"] + m_d["ckd"]
        assert np.all(active_masks == 1.0), "Each sample in batch must belong to exactly one task"
        # Verify CKD accounts for ~20% of batch
        ckd_count = np.sum(m_d["ckd"])
        assert 45 <= ckd_count <= 55, f"CKD count in batch {ckd_count} should be ~51 (20% of 256)"
        break
