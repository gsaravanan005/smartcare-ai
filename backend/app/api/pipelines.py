from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..core.database import get_db
from ..core.security import require_role
from ..schemas.schemas import PipelineRunRequest, PipelineRunResponse
from ..services.preprocessing_pipeline_service import PreprocessingPipelineService
from ..services.experiment_tracking_service import ExperimentTrackingService

router = APIRouter(prefix="/pipelines", tags=["Preprocessing Pipelines & Experiments"])

@router.post("/run", response_model=List[PipelineRunResponse])
def run_pipeline(
    req: PipelineRunRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin", "clinician"]))
):
    datasets_to_run = ["diabetes", "cardio", "ckd"] if req.dataset_name == "all" else [req.dataset_name]
    results = []

    for name in datasets_to_run:
        try:
            res = PreprocessingPipelineService.run_pipeline(
                dataset_name=name,
                imputation_method=req.imputation_method,
                outlier_strategy=req.outlier_strategy,
                encoding_strategy=req.encoding_strategy,
                scaling_strategy=req.scaling_strategy,
                feature_selection_method=req.feature_selection_method,
                k_features=req.k_features,
                class_imbalance_method=req.class_imbalance_method,
                missingness_injection_scenario=req.missingness_injection_scenario,
                missingness_injection_rate=req.missingness_injection_rate,
                random_seed=req.random_seed,
                train_ratio=req.train_ratio,
                val_ratio=req.val_ratio,
                test_ratio=req.test_ratio
            )
            
            # Log run to database
            exp_req = req.copy()
            exp_req.dataset_name = name
            ExperimentTrackingService.log_experiment(db, exp_req, res)

            results.append(PipelineRunResponse(
                status=res["status"],
                experiment_id=res["experiment_id"],
                dataset_name=res["dataset_name"],
                pipeline_version=res["pipeline_version"],
                train_shape=res["train_shape"],
                val_shape=res["val_shape"],
                test_shape=res["test_shape"],
                selected_features=res["selected_features"],
                vif_summary=res["vif_summary"],
                artifacts_exported=res["artifacts_exported"],
                message=res["message"]
            ))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Pipeline execution failed for '{name}': {str(e)}")

    return results

@router.get("/experiments")
def get_experiments(
    dataset_name: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin", "clinician"]))
):
    exps = ExperimentTrackingService.get_experiments(db, dataset_name)
    return exps
