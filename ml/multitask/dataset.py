"""
SmartCare AI - Multi-Task Dataset Manager & Feature Harmonization
Harmonizes T2D, CVD, and CKD datasets into a unified 30-feature shared representation,
strictly handles unavailable features via leakage-free training-fitted median imputation,
applies RobustScaler fitted strictly on training data, and manages task-masked multi-task batching.
"""

import os
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List, Optional
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
import joblib

from .config import MTLConfig


class MTLDatasetManager:
    """
    Manages loading, feature harmonization, leakage-free imputation, scaling,
    and task-masked multi-task dataset generation across T2D, CVD, and CKD cohorts.
    """

    def __init__(self, config: Optional[MTLConfig] = None):
        self.config = config or MTLConfig()
        self.feature_names: List[str] = self.config.all_features
        assert len(self.feature_names) == 30, f"Expected 30 features, got {len(self.feature_names)}"
        self.imputer: Optional[SimpleImputer] = None
        self.scaler: Optional[RobustScaler] = None

    # -------------------------------------------------------------------------
    # 1. RAW DATASET LOADERS & DATA CLEANING
    # -------------------------------------------------------------------------
    @staticmethod
    def _clean_ckd(df: pd.DataFrame) -> pd.DataFrame:
        """Cleans malformed strings and coerces types in the UCI CKD dataset."""
        df = df.copy()
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.strip().str.replace('\t', '')
                df[col] = df[col].replace({'?': np.nan, 'nan': np.nan, 'NaN': np.nan, '': np.nan, 'None': np.nan})

        numeric_cols = ['age', 'bp', 'sg', 'al', 'su', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        if 'classification' in df.columns:
            df['classification'] = df['classification'].replace({'ckd': 1, 'notckd': 0, 'ckd\t': 1})
            df = df.dropna(subset=['classification'])
            df['classification'] = df['classification'].astype(int)

        return df

    def load_raw_cohorts(self) -> Dict[str, Tuple[pd.DataFrame, pd.Series]]:
        """Loads and returns raw dataframes and target series for all three cohorts."""
        t2d_path = os.path.join(self.config.raw_data_dir, "diabetes_binary_5050split_health_indicators_BRFSS2015.csv")
        cvd_path = os.path.join(self.config.raw_data_dir, "cardio_data_processed.csv")
        ckd_path = os.path.join(self.config.raw_data_dir, "kidney_disease.csv")

        # Fallback to root or alternative file names if needed
        if not os.path.exists(t2d_path):
            t2d_path = os.path.abspath("diabetes_binary_5050split_health_indicators_BRFSS2015.csv")
        if not os.path.exists(cvd_path):
            cvd_path = os.path.abspath("cardio_data_processed.csv")
        if not os.path.exists(ckd_path):
            ckd_path = os.path.abspath("kidney_disease (1).csv")

        df_t2d = pd.read_csv(t2d_path)
        df_cvd = pd.read_csv(cvd_path)
        df_ckd = pd.read_csv(ckd_path)

        df_ckd = self._clean_ckd(df_ckd)
        if 'Diabetes_binary' in df_t2d.columns:
            df_t2d['Diabetes_binary'] = df_t2d['Diabetes_binary'].astype(int)
        if 'cardio' in df_cvd.columns:
            df_cvd['cardio'] = df_cvd['cardio'].astype(int)

        y_t2d = df_t2d['Diabetes_binary']
        X_t2d = df_t2d.drop(columns=['Diabetes_binary'])

        y_cvd = df_cvd['cardio']
        X_cvd = df_cvd.drop(columns=['cardio', 'id'], errors='ignore')

        y_ckd = df_ckd['classification']
        X_ckd = df_ckd.drop(columns=['classification', 'id'], errors='ignore')

        return {
            "t2d": (X_t2d, y_t2d),
            "cvd": (X_cvd, y_cvd),
            "ckd": (X_ckd, y_ckd)
        }

    # -------------------------------------------------------------------------
    # 2. FEATURE HARMONIZATION TO 30-DIMENSIONAL COMMON SCHEMA
    # -------------------------------------------------------------------------
    @staticmethod
    def _age_to_years(age_bin: float) -> float:
        """Converts BRFSS 1-13 ordinal age category to approximate midpoint years."""
        age_map = {
            1.0: 21.0, 2.0: 27.0, 3.0: 32.0, 4.0: 37.0, 5.0: 42.0,
            6.0: 47.0, 7.0: 52.0, 8.0: 57.0, 9.0: 62.0, 10.0: 67.0,
            11.0: 72.0, 12.0: 77.0, 13.0: 82.0
        }
        return age_map.get(float(age_bin), np.nan)

    def harmonize_t2d_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Maps T2D (BRFSS 2015) dataset to the 30-dimensional shared feature schema.
        Distinguishes directly observed, legitimately derived, and unavailable features (represented as np.nan).
        """
        out = pd.DataFrame(index=df.index)

        # Demographics
        out["age_years"] = df["Age"].apply(self._age_to_years) if "Age" in df.columns else np.nan
        out["gender"] = df["Sex"].astype(float) if "Sex" in df.columns else np.nan
        out["education"] = df["Education"].astype(float) if "Education" in df.columns else np.nan
        out["income"] = df["Income"].astype(float) if "Income" in df.columns else np.nan

        # Vitals & Anthropometrics
        out["bmi"] = df["BMI"].astype(float) if "BMI" in df.columns else np.nan
        out["high_bp"] = df["HighBP"].astype(float) if "HighBP" in df.columns else np.nan
        # SBP and DBP are NOT measured in BRFSS survey (unavailable, handled via training imputer)
        out["ap_hi"] = np.nan
        out["ap_lo"] = np.nan
        out["pulse_pressure"] = np.nan
        out["mean_arterial_pressure"] = np.nan

        # Laboratory & Biomarkers
        out["cholesterol"] = df["HighChol"].astype(float) if "HighChol" in df.columns else np.nan
        # Glucose is NOT measured in BRFSS (unavailable, NOT fabricated from cholesterol)
        out["glucose"] = np.nan
        out["serum_creatinine"] = np.nan
        out["blood_urea"] = np.nan
        out["hemoglobin"] = np.nan
        out["albumin_level"] = np.nan
        out["specific_gravity"] = np.nan
        out["bun_creatinine_ratio"] = np.nan
        out["egfr_proxy"] = np.nan
        out["anemia_flag"] = np.nan

        # Lifestyle & Behavioral
        out["smoker"] = df["Smoker"].astype(float) if "Smoker" in df.columns else np.nan
        out["phys_activity"] = df["PhysActivity"].astype(float) if "PhysActivity" in df.columns else np.nan
        out["alcohol_consumption"] = df["HvyAlcoholConsump"].astype(float) if "HvyAlcoholConsump" in df.columns else np.nan
        out["fruits"] = df["Fruits"].astype(float) if "Fruits" in df.columns else np.nan
        out["veggies"] = df["Veggies"].astype(float) if "Veggies" in df.columns else np.nan

        # History & Comorbidities
        out["heart_disease_or_attack"] = df["HeartDiseaseorAttack"].astype(float) if "HeartDiseaseorAttack" in df.columns else np.nan
        out["stroke"] = df["Stroke"].astype(float) if "Stroke" in df.columns else np.nan
        out["diff_walk"] = df["DiffWalk"].astype(float) if "DiffWalk" in df.columns else np.nan
        out["gen_hlth"] = df["GenHlth"].astype(float) if "GenHlth" in df.columns else np.nan
        out["combined_vascular_risk"] = (
            out["high_bp"].fillna(0.0)
            + out["cholesterol"].fillna(0.0)
            + out["smoker"].fillna(0.0)
            + out["stroke"].fillna(0.0)
            + out["heart_disease_or_attack"].fillna(0.0)
        )

        assert list(out.columns) == self.feature_names or set(out.columns) == set(self.feature_names)
        return out[self.feature_names]

    def harmonize_cvd_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Maps CVD (Kaggle Cardio) dataset to the 30-dimensional shared feature schema.
        Distinguishes directly observed, legitimately derived, and unavailable features (represented as np.nan).
        """
        out = pd.DataFrame(index=df.index)

        # Demographics
        if "age_years" in df.columns:
            out["age_years"] = df["age_years"].astype(float)
        elif "age" in df.columns:
            out["age_years"] = (df["age"] / 365.25).astype(float)
        else:
            out["age_years"] = np.nan

        if "gender" in df.columns:
            # Kaggle Cardio: 1 = Female (0.0), 2 = Male (1.0)
            out["gender"] = df["gender"].apply(lambda g: 1.0 if g == 2 else (0.0 if g == 1 else np.nan))
        else:
            out["gender"] = np.nan

        out["education"] = np.nan
        out["income"] = np.nan

        # Vitals & Anthropometrics
        if "bmi" in df.columns:
            out["bmi"] = df["bmi"].astype(float)
        elif "height" in df.columns and "weight" in df.columns:
            h_m = df["height"].replace(0, np.nan) / 100.0
            out["bmi"] = (df["weight"] / (h_m ** 2)).astype(float)
        else:
            out["bmi"] = np.nan

        out["ap_hi"] = df["ap_hi"].clip(lower=80, upper=220).astype(float) if "ap_hi" in df.columns else np.nan
        out["ap_lo"] = df["ap_lo"].clip(lower=50, upper=140).astype(float) if "ap_lo" in df.columns else np.nan
        out["pulse_pressure"] = out["ap_hi"] - out["ap_lo"]
        out["mean_arterial_pressure"] = out["ap_lo"] + out["pulse_pressure"] / 3.0
        out["high_bp"] = ((out["ap_hi"] >= 140.0) | (out["ap_lo"] >= 90.0)).astype(float)

        # Laboratory & Biomarkers
        out["cholesterol"] = df["cholesterol"].astype(float) if "cholesterol" in df.columns else np.nan
        if "gluc" in df.columns:
            # 1: Normal (<120 mg/dL) -> 100, 2: Above Normal (120-180 mg/dL) -> 140, 3: High (>180 mg/dL) -> 200
            gluc_map = {1: 100.0, 2: 140.0, 3: 200.0}
            out["glucose"] = df["gluc"].map(gluc_map).astype(float)
        else:
            out["glucose"] = np.nan

        out["serum_creatinine"] = np.nan
        out["blood_urea"] = np.nan
        out["hemoglobin"] = np.nan
        out["albumin_level"] = np.nan
        out["specific_gravity"] = np.nan
        out["bun_creatinine_ratio"] = np.nan
        out["egfr_proxy"] = np.nan
        out["anemia_flag"] = np.nan

        # Lifestyle & Behavioral
        out["smoker"] = df["smoke"].astype(float) if "smoke" in df.columns else np.nan
        out["phys_activity"] = df["active"].astype(float) if "active" in df.columns else np.nan
        out["alcohol_consumption"] = df["alco"].astype(float) if "alco" in df.columns else np.nan
        out["fruits"] = np.nan
        out["veggies"] = np.nan

        # History & Comorbidities
        # Prior heart attack/disease is NOT recorded in Kaggle CVD (unavailable; NOT derived from ap_hi)
        out["heart_disease_or_attack"] = np.nan
        out["stroke"] = np.nan
        out["diff_walk"] = np.nan
        out["gen_hlth"] = np.nan
        out["combined_vascular_risk"] = (
            out["high_bp"].fillna(0.0)
            + (out["cholesterol"] > 1.0).astype(float)
            + out["smoker"].fillna(0.0)
        )

        assert list(out.columns) == self.feature_names or set(out.columns) == set(self.feature_names)
        return out[self.feature_names]

    def harmonize_ckd_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Maps CKD (UCI Kidney Disease) dataset to the 30-dimensional shared feature schema.
        Distinguishes directly observed, legitimately derived, and unavailable features (represented as np.nan).
        """
        out = pd.DataFrame(index=df.index)

        # Demographics
        out["age_years"] = df["age"].astype(float) if "age" in df.columns else np.nan
        # Sex/gender is NOT recorded in UCI CKD dataset (unavailable; NOT defaulted to male 1.0)
        out["gender"] = np.nan
        out["education"] = np.nan
        out["income"] = np.nan

        # Vitals & Anthropometrics
        # BMI is NOT recorded in UCI CKD dataset (unavailable; NOT defaulted to 26.0)
        out["bmi"] = np.nan
        if "htn" in df.columns:
            out["high_bp"] = df["htn"].astype(str).str.lower().isin(["yes", "1", "true"]).astype(float)
        else:
            out["high_bp"] = np.nan

        out["ap_hi"] = df["bp"].astype(float) if "bp" in df.columns else np.nan
        out["ap_lo"] = np.nan
        out["pulse_pressure"] = np.nan
        out["mean_arterial_pressure"] = np.nan

        # Laboratory & Biomarkers
        out["cholesterol"] = np.nan
        out["glucose"] = df["bgr"].astype(float) if "bgr" in df.columns else np.nan
        out["serum_creatinine"] = df["sc"].clip(lower=0.4, upper=15.0).astype(float) if "sc" in df.columns else np.nan
        out["blood_urea"] = df["bu"].clip(lower=5.0, upper=200.0).astype(float) if "bu" in df.columns else np.nan
        out["hemoglobin"] = df["hemo"].clip(lower=3.0, upper=20.0).astype(float) if "hemo" in df.columns else np.nan
        out["albumin_level"] = df["al"].astype(float) if "al" in df.columns else np.nan
        out["specific_gravity"] = df["sg"].astype(float) if "sg" in df.columns else np.nan

        # Derived renal metrics with division safety
        sc_safe = out["serum_creatinine"].replace(0, 0.1)
        out["bun_creatinine_ratio"] = np.where(
            out["blood_urea"].notna() & out["serum_creatinine"].notna(),
            (out["blood_urea"] / sc_safe).clip(upper=100.0),
            np.nan
        )
        # Simplified MDRD eGFR proxy equation (documented as proxy index)
        out["egfr_proxy"] = np.where(
            out["serum_creatinine"].notna() & out["age_years"].notna(),
            (175.0 * (sc_safe ** -1.154) * (out["age_years"].clip(lower=18.0) ** -0.203)).round(1),
            np.nan
        )
        if "ane" in df.columns:
            out["anemia_flag"] = np.where(
                df["ane"].astype(str).str.lower().isin(["yes", "1", "true"]),
                1.0,
                np.where(out["hemoglobin"].notna(), (out["hemoglobin"] < 12.0).astype(float), np.nan)
            )
        elif "hemo" in df.columns:
            out["anemia_flag"] = np.where(out["hemoglobin"].notna(), (out["hemoglobin"] < 12.0).astype(float), np.nan)
        else:
            out["anemia_flag"] = np.nan

        # Lifestyle & Behavioral
        # Smoking status is NOT recorded in UCI CKD (unavailable; NOT mapped from CAD!)
        out["smoker"] = np.nan
        out["phys_activity"] = np.nan
        out["alcohol_consumption"] = np.nan
        out["fruits"] = np.nan
        out["veggies"] = np.nan

        # History & Comorbidities
        if "cad" in df.columns:
            out["heart_disease_or_attack"] = df["cad"].astype(str).str.lower().isin(["yes", "1", "true"]).astype(float)
        else:
            out["heart_disease_or_attack"] = np.nan

        out["stroke"] = np.nan
        out["diff_walk"] = np.nan
        out["gen_hlth"] = np.nan

        dm_flag = df["dm"].astype(str).str.lower().isin(["yes", "1", "true"]).astype(float) if "dm" in df.columns else 0.0
        out["combined_vascular_risk"] = (
            out["high_bp"].fillna(0.0)
            + dm_flag
            + out["heart_disease_or_attack"].fillna(0.0)
        )

        assert list(out.columns) == self.feature_names or set(out.columns) == set(self.feature_names)
        return out[self.feature_names]

    # -------------------------------------------------------------------------
    # 3. SINGLE PATIENT INFERENCE INPUT HARMONIZATION
    # -------------------------------------------------------------------------
    def harmonize_patient_input(self, patient_dict: Dict[str, Any]) -> pd.DataFrame:
        """
        Harmonizes a patient dictionary payload into the standardized 30-dimensional
        feature representation, applying training-fitted imputation and RobustScaler.
        """
        mapped = pd.DataFrame(index=[0])

        def safe_float(val, default=0.0):
            if val is None or val == "":
                return float(default)
            try:
                return float(val)
            except (ValueError, TypeError):
                return float(default)

        # Demographics
        age = safe_float(patient_dict.get("age"), 50.0)
        mapped["age_years"] = age
        mapped["gender"] = safe_float(patient_dict.get("sex"), 1.0)
        mapped["education"] = safe_float(patient_dict.get("education"), 4.0)
        mapped["income"] = safe_float(patient_dict.get("income"), 5.0)

        # Vitals & Anthropometrics
        bmi = patient_dict.get("bmi")
        if bmi is None or str(bmi) == "" or safe_float(bmi, 0.0) <= 0:
            h_cm = safe_float(patient_dict.get("height_cm"), 170.0)
            w_kg = safe_float(patient_dict.get("weight_kg"), 70.0)
            bmi = w_kg / ((h_cm / 100.0) ** 2) if h_cm > 0 else 24.5
        mapped["bmi"] = safe_float(bmi, 24.5)

        ap_hi = safe_float(patient_dict.get("ap_hi"), 120.0)
        ap_lo = safe_float(patient_dict.get("ap_lo"), 80.0)
        mapped["ap_hi"] = ap_hi
        mapped["ap_lo"] = ap_lo
        mapped["pulse_pressure"] = ap_hi - ap_lo
        mapped["mean_arterial_pressure"] = ap_lo + (ap_hi - ap_lo) / 3.0

        high_bp = safe_float(patient_dict.get("high_bp"), 1.0 if ap_hi >= 140 or ap_lo >= 90 else 0.0)
        mapped["high_bp"] = high_bp

        # Laboratory & Biomarkers
        mapped["cholesterol"] = safe_float(patient_dict.get("cholesterol"), 2.0 if patient_dict.get("high_chol", 0) else 1.0)
        mapped["glucose"] = safe_float(patient_dict.get("glucose"), 100.0)

        sc = safe_float(patient_dict.get("serum_creatinine"), 1.0)
        bu = safe_float(patient_dict.get("blood_urea"), 28.0)
        hemo = safe_float(patient_dict.get("hemoglobin"), 14.0)
        mapped["serum_creatinine"] = sc
        mapped["blood_urea"] = bu
        mapped["hemoglobin"] = hemo
        mapped["albumin_level"] = safe_float(patient_dict.get("albumin_level"), 0.0)
        mapped["specific_gravity"] = safe_float(patient_dict.get("specific_gravity"), 1.020)

        sc_safe = max(0.1, sc)
        mapped["bun_creatinine_ratio"] = bu / sc_safe
        mapped["egfr_proxy"] = round(float(175.0 * (sc_safe ** -1.154) * (max(18.0, age) ** -0.203)), 1)
        mapped["anemia_flag"] = 1.0 if hemo < 12.0 or patient_dict.get("anemia") in ["yes", 1] else 0.0

        # Lifestyle & Behavioral
        mapped["smoker"] = safe_float(patient_dict.get("smoker"), 0.0)
        mapped["phys_activity"] = safe_float(patient_dict.get("phys_activity"), 1.0)
        mapped["alcohol_consumption"] = safe_float(patient_dict.get("hvy_alcohol_consump"), 0.0)
        mapped["fruits"] = safe_float(patient_dict.get("fruits"), 1.0)
        mapped["veggies"] = safe_float(patient_dict.get("veggies"), 1.0)

        # History & Comorbidities
        mapped["heart_disease_or_attack"] = safe_float(patient_dict.get("heart_disease_or_attack"), 0.0)
        mapped["stroke"] = safe_float(patient_dict.get("stroke"), 0.0)
        mapped["diff_walk"] = safe_float(patient_dict.get("diff_walk"), 0.0)
        mapped["gen_hlth"] = safe_float(patient_dict.get("gen_hlth"), 2.0)
        mapped["combined_vascular_risk"] = (
            high_bp
            + safe_float(patient_dict.get("high_chol"), 0.0)
            + mapped["smoker"].iloc[0]
            + mapped["stroke"].iloc[0]
            + mapped["heart_disease_or_attack"].iloc[0]
        )

        aligned = mapped[self.feature_names]

        # Apply training-fitted imputer if available
        if self.imputer is not None:
            aligned_imp = pd.DataFrame(self.imputer.transform(aligned), columns=self.feature_names)
        else:
            aligned_imp = aligned.fillna(0.0)

        # Apply training-fitted scaler if available
        if self.scaler is not None:
            arr_scaled = self.scaler.transform(aligned_imp)
            return pd.DataFrame(arr_scaled, columns=self.feature_names)

        return aligned_imp

    # -------------------------------------------------------------------------
    # 4. SPLIT, IMPUTATION & SCALER FIT (STRICT LEAKAGE PREVENTION)
    # -------------------------------------------------------------------------
    def prepare_multitask_data(
        self,
        train_ratio: float = 0.70,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        random_seed: int = 42
    ) -> Dict[str, Any]:
        """
        Loads raw cohorts, harmonizes features into the unified 30-feature space,
        performs stratified Train/Val/Test splits (70/15/15) strictly before fitting preprocessing,
        fits SimpleImputer(strategy='median') ONLY on combined training partitions,
        fits RobustScaler ONLY on imputed training partitions, and returns leakage-free scaled splits.
        """
        cohorts = self.load_raw_cohorts()

        splits = {}
        val_test_sum = val_ratio + test_ratio
        val_rel = val_ratio / val_test_sum

        for disease in ["t2d", "cvd", "ckd"]:
            X_raw, y_raw = cohorts[disease]

            # Harmonize to 30-dimensional schema (with np.nan for unavailable features)
            if disease == "t2d":
                X_harm = self.harmonize_t2d_features(X_raw)
            elif disease == "cvd":
                X_harm = self.harmonize_cvd_features(X_raw)
            else:
                X_harm = self.harmonize_ckd_features(X_raw)

            # Stratified Train / Temp Split
            X_tr, X_tmp, y_tr, y_tmp = train_test_split(
                X_harm, y_raw, test_size=val_test_sum, random_state=random_seed, stratify=y_raw
            )
            # Stratified Val / Test Split
            X_va, X_te, y_va, y_te = train_test_split(
                X_tmp, y_tmp, test_size=(1.0 - val_rel), random_state=random_seed, stratify=y_tmp
            )

            splits[disease] = {
                "train": (X_tr.reset_index(drop=True), y_tr.reset_index(drop=True)),
                "val": (X_va.reset_index(drop=True), y_va.reset_index(drop=True)),
                "test": (X_te.reset_index(drop=True), y_te.reset_index(drop=True))
            }

        # Fit Imputer ONLY on combined training data
        X_train_combined = pd.concat([
            splits["t2d"]["train"][0],
            splits["cvd"]["train"][0],
            splits["ckd"]["train"][0]
        ], axis=0, ignore_index=True)

        self.imputer = SimpleImputer(strategy="median")
        self.imputer.fit(X_train_combined)

        # Impute all partitions using training-fitted imputer
        imputed_splits = {}
        for disease in ["t2d", "cvd", "ckd"]:
            imputed_splits[disease] = {}
            for partition in ["train", "val", "test"]:
                X_part, y_part = splits[disease][partition]
                X_imp = pd.DataFrame(
                    self.imputer.transform(X_part),
                    columns=self.feature_names
                )
                imputed_splits[disease][partition] = (X_imp, y_part)

        # Fit RobustScaler ONLY on imputed training data
        X_train_imputed_combined = pd.concat([
            imputed_splits["t2d"]["train"][0],
            imputed_splits["cvd"]["train"][0],
            imputed_splits["ckd"]["train"][0]
        ], axis=0, ignore_index=True)

        self.scaler = RobustScaler()
        self.scaler.fit(X_train_imputed_combined)

        # Transform all partitions using training-fitted scaler
        scaled_splits = {}
        for disease in ["t2d", "cvd", "ckd"]:
            scaled_splits[disease] = {}
            for partition in ["train", "val", "test"]:
                X_imp, y_part = imputed_splits[disease][partition]
                X_scaled = pd.DataFrame(
                    self.scaler.transform(X_imp),
                    columns=self.feature_names
                )
                scaled_splits[disease][partition] = (X_scaled, y_part)

        return {
            "scaled_splits": scaled_splits,
            "raw_splits": splits,
            "imputed_splits": imputed_splits,
            "imputer": self.imputer,
            "scaler": self.scaler,
            "feature_names": self.feature_names
        }


class TaskBalancedBatchIterator:
    """
    Mini-batch generator with Task Masking and Task-Balanced Sampling.
    Samples CKD cohort proportionally (e.g. 20% of mini-batch with replacement on training partition only)
    so its gradient contributes actively to the shared representation in every epoch.
    """

    def __init__(
        self,
        t2d_data: Tuple[pd.DataFrame, pd.Series],
        cvd_data: Tuple[pd.DataFrame, pd.Series],
        ckd_data: Tuple[pd.DataFrame, pd.Series],
        batch_size: int = 256,
        ckd_ratio: float = 0.20,
        random_seed: int = 42
    ):
        self.X_t2d, self.y_t2d = t2d_data[0].values, t2d_data[1].values
        self.X_cvd, self.y_cvd = cvd_data[0].values, cvd_data[1].values
        self.X_ckd, self.y_ckd = ckd_data[0].values, ckd_data[1].values

        self.n_t2d = len(self.X_t2d)
        self.n_cvd = len(self.X_cvd)
        self.n_ckd = len(self.X_ckd)

        self.batch_size = batch_size
        self.n_ckd_batch = max(4, int(batch_size * ckd_ratio))
        remaining = batch_size - self.n_ckd_batch
        self.n_t2d_batch = remaining // 2
        self.n_cvd_batch = remaining - self.n_t2d_batch

        self.rng = np.random.default_rng(random_seed)
        self.num_batches_per_epoch = max(self.n_t2d, self.n_cvd) // (self.n_t2d_batch + self.n_cvd_batch)

    def __iter__(self):
        self.idx_t2d = self.rng.permutation(self.n_t2d)
        self.idx_cvd = self.rng.permutation(self.n_cvd)
        self.ptr_t2d = 0
        self.ptr_cvd = 0
        self.batch_count = 0
        return self

    def __next__(self) -> Tuple[np.ndarray, Dict[str, np.ndarray], Dict[str, np.ndarray]]:
        """
        Returns:
            X_batch: (batch_size, input_dim)
            y_dict: {'t2d': array, 'cvd': array, 'ckd': array}
            mask_dict: {'t2d': mask_array, 'cvd': mask_array, 'ckd': mask_array}
        """
        if self.batch_count >= self.num_batches_per_epoch:
            raise StopIteration

        # Sample T2D
        if self.ptr_t2d + self.n_t2d_batch > self.n_t2d:
            self.idx_t2d = self.rng.permutation(self.n_t2d)
            self.ptr_t2d = 0
        batch_idx_t2d = self.idx_t2d[self.ptr_t2d:self.ptr_t2d + self.n_t2d_batch]
        self.ptr_t2d += self.n_t2d_batch

        # Sample CVD
        if self.ptr_cvd + self.n_cvd_batch > self.n_cvd:
            self.idx_cvd = self.rng.permutation(self.n_cvd)
            self.ptr_cvd = 0
        batch_idx_cvd = self.idx_cvd[self.ptr_cvd:self.ptr_cvd + self.n_cvd_batch]
        self.ptr_cvd += self.n_cvd_batch

        # Sample CKD (with replacement on training split only to ensure 20% representation in mini-batch)
        batch_idx_ckd = self.rng.choice(self.n_ckd, size=self.n_ckd_batch, replace=True)

        X_t = self.X_t2d[batch_idx_t2d]
        y_t = self.y_t2d[batch_idx_t2d]

        X_c = self.X_cvd[batch_idx_cvd]
        y_c = self.y_cvd[batch_idx_cvd]

        X_k = self.X_ckd[batch_idx_ckd]
        y_k = self.y_ckd[batch_idx_ckd]

        # Combine into unified mini-batch
        X_batch = np.vstack([X_t, X_c, X_k])
        N = len(X_batch)

        y_dict = {
            "t2d": np.zeros(N, dtype=np.float32),
            "cvd": np.zeros(N, dtype=np.float32),
            "ckd": np.zeros(N, dtype=np.float32),
        }
        mask_dict = {
            "t2d": np.zeros(N, dtype=np.float32),
            "cvd": np.zeros(N, dtype=np.float32),
            "ckd": np.zeros(N, dtype=np.float32),
        }

        # T2D slice: 0 .. len(X_t)
        n_t = len(X_t)
        n_c = len(X_c)
        n_k = len(X_k)

        y_dict["t2d"][:n_t] = y_t
        mask_dict["t2d"][:n_t] = 1.0

        # CVD slice: n_t .. n_t + n_c
        y_dict["cvd"][n_t:n_t + n_c] = y_c
        mask_dict["cvd"][n_t:n_t + n_c] = 1.0

        # CKD slice: n_t + n_c .. N
        y_dict["ckd"][n_t + n_c:] = y_k
        mask_dict["ckd"][n_t + n_c:] = 1.0

        # Randomly shuffle inside the batch
        perm = self.rng.permutation(N)
        X_batch = X_batch[perm]
        for task in ["t2d", "cvd", "ckd"]:
            y_dict[task] = y_dict[task][perm]
            mask_dict[task] = mask_dict[task][perm]

        self.batch_count += 1
        return X_batch, y_dict, mask_dict
