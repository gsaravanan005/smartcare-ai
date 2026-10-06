from sqlalchemy.orm import Session
from datetime import datetime
import time
from ..models.models import PreprocessingExperiment, PipelineVersion, DatasetMetadata
from ..schemas.schemas import PipelineRunRequest

class ExperimentTrackingService:

    @classmethod
    def log_experiment(cls, db: Session, req: PipelineRunRequest, run_result: dict) -> PreprocessingExperiment:
        exp_id = run_result["experiment_id"]
        
        # Check if experiment_id already exists to prevent SQLite UNIQUE constraint failure
        existing_exp = db.query(PreprocessingExperiment).filter(PreprocessingExperiment.experiment_id == exp_id).first()
        if existing_exp:
            exp_id = f"{exp_id}_{int(time.time())}"
            run_result["experiment_id"] = exp_id

        exp = PreprocessingExperiment(
            experiment_id=exp_id,
            dataset_name=req.dataset_name,
            missingness_scenario=req.missingness_injection_scenario,
            missingness_percentage=req.missingness_injection_rate,
            imputation_method=req.imputation_method,
            outlier_strategy=req.outlier_strategy,
            encoding_strategy=req.encoding_strategy,
            scaling_strategy=req.scaling_strategy,
            feature_selection_method=req.feature_selection_method,
            class_imbalance_method=req.class_imbalance_method,
            train_val_test_ratio=f"{int(req.train_ratio*100)}/{int(req.val_ratio*100)}/{int(req.test_ratio*100)}",
            random_seed=req.random_seed,
            pipeline_version=run_result["pipeline_version"],
            metrics_summary={
                "train_shape": run_result["train_shape"],
                "val_shape": run_result["val_shape"],
                "test_shape": run_result["test_shape"],
                "selected_features": run_result["selected_features"],
                "vif_summary": run_result["vif_summary"]
            }
        )
        db.add(exp)

        # Log pipeline version artifact record
        pv = db.query(PipelineVersion).filter(PipelineVersion.pipeline_version == run_result["pipeline_version"]).first()
        if not pv:
            pv = PipelineVersion(
                pipeline_version=run_result["pipeline_version"],
                dataset_name=req.dataset_name,
                artifact_path=run_result["artifacts_exported"][3] if len(run_result["artifacts_exported"]) > 3 else "",
                configuration=req.dict(),
                status="ACTIVE"
            )
            db.add(pv)

        # Update dataset metadata status
        meta = db.query(DatasetMetadata).filter(DatasetMetadata.dataset_name == req.dataset_name).first()
        if meta:
            meta.processing_status = "PROCESSED"
            meta.last_updated = datetime.utcnow()
        else:
            meta = DatasetMetadata(
                dataset_name=req.dataset_name,
                file_name=f"{req.dataset_name}.csv",
                num_rows=run_result["train_shape"][0] + run_result["val_shape"][0] + run_result["test_shape"][0],
                num_columns=run_result["train_shape"][1],
                target_column="target",
                processing_status="PROCESSED"
            )
            db.add(meta)

        db.commit()
        db.refresh(exp)
        return exp

    @classmethod
    def get_experiments(cls, db: Session, dataset_name: str = None) -> list:
        query = db.query(PreprocessingExperiment)
        if dataset_name:
            query = query.filter(PreprocessingExperiment.dataset_name == dataset_name)
        return query.order_by(PreprocessingExperiment.created_at.desc()).all()
