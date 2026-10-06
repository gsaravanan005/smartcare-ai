import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.dataset_loader_service import DatasetLoaderService
from app.services.dataset_profiler_service import DatasetProfilerService

def test_load_all_datasets():
    for name in ["diabetes", "cardio", "ckd"]:
        df, target_col = DatasetLoaderService.load_dataset(name)
        assert df is not None
        assert not df.empty
        assert target_col in df.columns
        assert df[target_col].isnull().sum() == 0, f"Target column {target_col} in {name} contains missing values."

def test_dataset_profiling():
    df, target_col = DatasetLoaderService.load_dataset("ckd")
    profile = DatasetProfilerService.generate_full_profile("ckd", df, target_col)
    
    assert profile["num_rows"] > 0
    assert profile["num_columns"] > 0
    assert profile["target_column"] == "classification"
    assert "summary_stats" in profile
    assert "target_distribution" in profile
