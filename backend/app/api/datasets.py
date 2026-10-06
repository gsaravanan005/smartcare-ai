from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..services.dataset_loader_service import DatasetLoaderService
from ..services.dataset_profiler_service import DatasetProfilerService
from ..services.missing_value_service import MissingValueService
from ..services.feature_mapping_service import FeatureMappingService

router = APIRouter(prefix="/datasets", tags=["Dataset Profiling & Research"])

@router.get("/list")
def list_datasets(current_user=Depends(require_role(["admin", "clinician"]))):
    return [
        DatasetLoaderService.get_raw_metadata("diabetes"),
        DatasetLoaderService.get_raw_metadata("cardio"),
        DatasetLoaderService.get_raw_metadata("ckd")
    ]

@router.get("/{name}/profile")
def get_dataset_profile(name: str, current_user=Depends(require_role(["admin", "clinician"]))):
    try:
        df, target_col = DatasetLoaderService.load_dataset(name)
        profile = DatasetProfilerService.generate_full_profile(name, df, target_col)
        return profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{name}/missingness")
def get_missingness_report(name: str, current_user=Depends(require_role(["admin", "clinician"]))):
    try:
        df, _ = DatasetLoaderService.load_dataset(name)
        report = MissingValueService.analyze_missingness_patterns(df)
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{name}/vif")
def get_vif_report(name: str, current_user=Depends(require_role(["admin", "clinician"]))):
    try:
        df, target_col = DatasetLoaderService.load_dataset(name)
        features = [c for c in df.columns if c != target_col and c.lower() != 'id']
        vif_data = DatasetProfilerService.calculate_vif(df, features)
        return {"dataset_name": name, "vif_summary": vif_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/feature-mapping")
def get_feature_mapping(current_user=Depends(get_current_user)):
    return FeatureMappingService.get_common_feature_schema()
