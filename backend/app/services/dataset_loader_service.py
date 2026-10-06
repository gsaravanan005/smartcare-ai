import os
import shutil
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Any
from ..core.config import settings

class DatasetLoaderService:
    DATASET_FILES = {
        "diabetes": "diabetes_binary_5050split_health_indicators_BRFSS2015.csv",
        "cardio": "cardio_data_processed.csv",
        "ckd": "kidney_disease.csv"
    }

    TARGET_COLUMNS = {
        "diabetes": "Diabetes_binary",
        "cardio": "cardio",
        "ckd": "classification"
    }

    @classmethod
    def load_dataset(cls, name: str, from_working: bool = True) -> Tuple[pd.DataFrame, str]:
        if name not in cls.DATASET_FILES:
            raise ValueError(f"Unknown dataset '{name}'. Available: {list(cls.DATASET_FILES.keys())}")

        filename = cls.DATASET_FILES[name]
        raw_path = os.path.join(settings.RAW_DATA_DIR, filename)
        working_path = os.path.join(settings.WORKING_DATA_DIR, filename)

        if not os.path.exists(raw_path):
            raise FileNotFoundError(f"Raw dataset file not found at: {raw_path}")

        # Ensure working copy exists and raw file remains untouched
        if not os.path.exists(working_path) or not from_working:
            shutil.copy(raw_path, working_path)

        path_to_read = working_path if from_working else raw_path
        
        try:
            df = pd.read_csv(path_to_read)
        except Exception as e:
            raise RuntimeError(f"Failed to read CSV dataset '{name}': {str(e)}")

        # Dataset specific cleaning (e.g. dirty string values in CKD dataset)
        df = cls._clean_dataset_artifacts(name, df)
        
        target_col = cls.TARGET_COLUMNS[name]
        return df, target_col

    @classmethod
    def _clean_dataset_artifacts(cls, name: str, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        if name == "ckd":
            # Remove whitespace/tabs from string values in CKD dataset
            for col in df.columns:
                if df[col].dtype == object:
                    df[col] = df[col].astype(str).str.strip().str.replace('\t', '')
                    # Map missing value representations
                    df[col] = df[col].replace({'?': np.nan, 'nan': np.nan, 'NaN': np.nan, '': np.nan, 'None': np.nan})
            
            # Clean numeric columns that were parsed as object due to dirty strings
            numeric_cols = ['age', 'bp', 'sg', 'al', 'su', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Clean target column 'classification'
            if 'classification' in df.columns:
                df['classification'] = df['classification'].replace({'ckd': 1, 'notckd': 0, 'ckd\t': 1})
                # Drop rows where target is missing if any
                df = df.dropna(subset=['classification'])
                df['classification'] = df['classification'].astype(int)

        elif name == "diabetes":
            if 'Diabetes_binary' in df.columns:
                df['Diabetes_binary'] = df['Diabetes_binary'].astype(int)

        elif name == "cardio":
            if 'cardio' in df.columns:
                df['cardio'] = df['cardio'].astype(int)

        return df

    @classmethod
    def get_raw_metadata(cls, name: str) -> Dict[str, Any]:
        df, target_col = cls.load_dataset(name)
        return {
            "dataset_name": name,
            "file_name": cls.DATASET_FILES[name],
            "num_rows": int(df.shape[0]),
            "num_columns": int(df.shape[1]),
            "target_column": target_col,
            "columns": df.columns.tolist()
        }
