#!/usr/bin/env python
"""
SmartCare AI - Module 2 ML Model Training, Tuning, Calibration & Evaluation CLI Script
"""
import sys
import os
import argparse
import numpy as np
import pandas as pd
import json

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.core.database import SessionLocal, engine, Base
from app.models.models import ModelRegistry, ModelExperiment, ModelEvaluation
from app.services.data_validation_service import DataValidationService
from app.services.model_training_service import ModelTrainingService
from app.services.tuning_cv_service import TuningCVService
from app.services.calibration_service import CalibrationService
from app.services.experiment_comparison_service import ExperimentComparisonService
from app.services.model_registry_service import ModelRegistryService

# Initialize tables
Base.metadata.create_all(bind=engine)

def main():
    parser = argparse.ArgumentParser(description="SmartCare AI - Module 2 Model Trainer")
    parser.add_argument("--mode", type=str, default="all", choices=["all", "independent", "multitask"], help="Training mode")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    print("\n=======================================================")
    print("   SMARTCARE AI - MODULE 2 ML MODEL TRAINING ENGINE    ")
    print("=======================================================\n")

    db = SessionLocal()
    diseases = ["diabetes", "cardio", "ckd"]
    independent_test_results = {}

    # -------------------------------------------------------------
    # 1. INDEPENDENT DISEASE MODEL TRAINING & CALIBRATION
    # -------------------------------------------------------------
    if args.mode in ["all", "independent"]:
        for disease in diseases:
            print(f"[*] Validating and training independent models for {disease.upper()}...")
            
            # Step A: Validate artifacts from Module 1
            X_train, y_train, X_val, y_val, X_test, y_test, meta = DataValidationService.validate_dataset_artifacts(disease)
            print(f"  [+] Module 1 artifacts validated. Features ({len(meta['feature_names'])}): {meta['feature_names'][:4]}...")
            print(f"  [+] Split shapes -> Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")

            # Step B: Train Baseline 1 - Logistic Regression
            print(f"  [+] Tuning Baseline 1 (Logistic Regression)...")
            lr_grid = {'C': [0.1, 1.0, 10.0], 'class_weight': ['balanced']}
            lr_cv = TuningCVService.evaluate_model_cv('logistic_regression', X_train, y_train, lr_grid, random_seed=args.seed)
            lr_model = ModelTrainingService.train_logistic_regression(X_train, y_train, **lr_cv['best_parameters'], random_seed=args.seed)
            print(f"      - Best LR CV ROC-AUC: {lr_cv['best_cv_roc_auc']:.4f} (Recall: {lr_cv['best_cv_recall']:.4f})")

            # Step C: Train Baseline 2 - Random Forest
            print(f"  [+] Tuning Baseline 2 (Random Forest)...")
            rf_grid = {'n_estimators': [50, 100], 'max_depth': [6, 10], 'class_weight': ['balanced']}
            rf_cv = TuningCVService.evaluate_model_cv('random_forest', X_train, y_train, rf_grid, random_seed=args.seed)
            rf_model = ModelTrainingService.train_random_forest(X_train, y_train, **rf_cv['best_parameters'], random_seed=args.seed)
            print(f"      - Best RF CV ROC-AUC: {rf_cv['best_cv_roc_auc']:.4f} (Recall: {rf_cv['best_cv_recall']:.4f})")

            # Step D: Train Advanced Model - XGBoost
            print(f"  [+] Tuning Advanced Model (XGBoost)...")
            xgb_grid = {'n_estimators': [50, 100], 'learning_rate': [0.05, 0.1], 'max_depth': [4, 6]}
            xgb_cv = TuningCVService.evaluate_model_cv('xgboost', X_train, y_train, xgb_grid, random_seed=args.seed)
            xgb_model = ModelTrainingService.train_xgboost(X_train, y_train, **xgb_cv['best_parameters'], random_seed=args.seed)
            print(f"      - Best XGB CV ROC-AUC: {xgb_cv['best_cv_roc_auc']:.4f} (Recall: {xgb_cv['best_cv_recall']:.4f})")

            # Select Best Candidate Model based on Validation CV score
            candidates = [
                ("LogisticRegression", lr_model, lr_cv),
                ("RandomForest", rf_model, rf_cv),
                ("XGBoost", xgb_model, xgb_cv)
            ]
            best_name, best_uncalib_model, best_cv = max(candidates, key=lambda x: x[2]['best_cv_roc_auc'])
            print(f"  [+] Selected Best Model for {disease.upper()}: {best_name} (CV ROC-AUC: {best_cv['best_cv_roc_auc']:.4f})")

            # Step E: Probability Calibration on Validation Set
            calibrated_model, calib_metrics = CalibrationService.calibrate_model(best_uncalib_model, X_val, y_val, method="sigmoid")
            print(f"  [+] Calibrated model probabilities. Brier score improved by: {calib_metrics['brier_improvement']:.4f}")

            # Step F: Optimal Threshold Tuning on Validation Set
            th_info = CalibrationService.find_optimal_threshold(calibrated_model, X_val, y_val, min_recall_target=0.70)
            optimal_th = th_info.get("threshold", 0.5)
            print(f"  [+] Optimal decision threshold selected on Val set: {optimal_th} (Val Recall: {th_info.get('recall')})")

            # Step G: Final Unbiased Evaluation ONCE on Isolated Held-out Test Set
            test_metrics = ExperimentComparisonService.evaluate_binary_classifier(calibrated_model, X_test, y_test, threshold=optimal_th)
            test_metrics["model_type"] = best_name
            test_metrics["calibration_curve"] = calib_metrics["calibration_curve"]
            independent_test_results[disease] = test_metrics

            print(f"  [+] TEST EVALUATION RESULTS FOR {disease.upper()}:")
            print(f"      - Accuracy: {test_metrics['accuracy']} | Precision: {test_metrics['precision']} | Recall: {test_metrics['recall']} | F1: {test_metrics['f1_score']}")
            print(f"      - Test ROC-AUC: {test_metrics['roc_auc']} | PR-AUC: {test_metrics['pr_auc']} | Brier Score: {test_metrics['brier_score']}")
            print(f"      - Confusion Matrix: TP={test_metrics['confusion_matrix']['tp']}, FP={test_metrics['confusion_matrix']['fp']}, TN={test_metrics['confusion_matrix']['tn']}, FN={test_metrics['confusion_matrix']['fn']}")

            # Step H: Serialize Model Artifact & Register in DB
            ver_str = f"{disease}_{best_name.lower()}_v1"
            artifact_path = ModelRegistryService.save_model_artifact(
                disease=disease,
                model_name=best_name,
                version=ver_str,
                model=calibrated_model,
                feature_names=meta["feature_names"],
                threshold=optimal_th,
                calibration_method="platt_sigmoid",
                metrics=test_metrics
            )
            ModelRegistryService.register_model_in_db(db, disease, best_name, ver_str, "scikit-learn", artifact_path, test_metrics)
            ModelRegistryService.log_evaluation_in_db(db, ver_str, disease, test_metrics)

            # Log experiment record safely
            exp_id_str = f"EXP_{disease.upper()}_{best_name}_{args.seed}"
            exp_rec = db.query(ModelExperiment).filter(ModelExperiment.experiment_id == exp_id_str).first()
            if exp_rec:
                exp_rec.hyperparameters = best_cv["best_parameters"]
                exp_rec.cv_score_mean = best_cv["best_cv_roc_auc"]
                exp_rec.cv_score_std = best_cv["best_cv_std"]
                exp_rec.test_roc_auc = test_metrics["roc_auc"]
                exp_rec.test_recall = test_metrics["recall"]
                exp_rec.test_f1 = test_metrics["f1_score"]
                exp_rec.brier_score = test_metrics["brier_score"]
                exp_rec.metrics_full = test_metrics
            else:
                exp_rec = ModelExperiment(
                    experiment_id=exp_id_str,
                    disease=disease,
                    model_type=best_name,
                    architecture_type="independent",
                    hyperparameters=best_cv["best_parameters"],
                    cv_score_mean=best_cv["best_cv_roc_auc"],
                    cv_score_std=best_cv["best_cv_std"],
                    test_roc_auc=test_metrics["roc_auc"],
                    test_recall=test_metrics["recall"],
                    test_f1=test_metrics["f1_score"],
                    brier_score=test_metrics["brier_score"],
                    metrics_full=test_metrics,
                    random_seed=args.seed
                )
                db.add(exp_rec)
            db.commit()


            print("-" * 65)

    # -------------------------------------------------------------
    # 2. MULTI-TASK ARCHITECTURE TRAINING & COMPARISON
    # -------------------------------------------------------------
    if args.mode in ["all", "multitask"]:
        print(f"[*] Training Multi-Task Shared Representation Network...")
        from ml.multitask.train import train_mtl_pipeline
        from ml.multitask.config import MTLConfig
        
        mtl_cfg = MTLConfig(random_seed=args.seed)
        mtl_meta = train_mtl_pipeline(config=mtl_cfg, run_ablation=True, run_baselines=True)
        mtl_test_metrics = mtl_meta["test_metrics"]

        ver_mt = "smartcare_mtl_v1"
        mt_path = os.path.join(mtl_cfg.models_dir, "smartcare_mtl_model.joblib")
        
        # Register MTL model in DB
        ModelRegistryService.register_model_in_db(
            db, "multitask", "MultiTaskSharedEncoder", ver_mt, "custom-neural-mtl", mt_path, mtl_test_metrics
        )
        for dis in ["t2d", "cvd", "ckd"]:
            ModelRegistryService.log_evaluation_in_db(db, ver_mt, dis, mtl_test_metrics[dis])

        # -------------------------------------------------------------
        # 3. INDEPENDENT VS MULTI-TASK COMPARATIVE ANALYSIS
        # -------------------------------------------------------------
        print("\n=======================================================")
        print("    INDEPENDENT VS MULTI-TASK EXPERIMENT COMPARISON   ")
        print("=======================================================\n")
        
        mapping = {"diabetes": "t2d", "cardio": "cvd", "ckd": "ckd"}
        for dis, mtl_key in mapping.items():
            ind = independent_test_results.get(dis, {})
            mt = mtl_test_metrics.get(mtl_key, {})
            ind_roc = ind.get("roc_auc", 0.0)
            mt_roc = mt.get("roc_auc", 0.0)
            winner = "Multi-Task" if mt_roc >= ind_roc else "Independent"
            
            print(f"[*] Disease: {dis.upper()}")
            print(f"    - Independent Model ({ind.get('model_type', 'Baseline')}): ROC-AUC={ind_roc}, Recall={ind.get('recall', 0.0)}")
            print(f"    - Multi-Task Model (SharedEncoderMTL):       ROC-AUC={mt_roc}, Recall={mt.get('recall', 0.0)}")
            print(f"    - Winning Architecture:                      {winner.upper()}")
            print("-" * 55)

    print("\n[SUCCESS] Module 2 model training, tuning, calibration, and test evaluation complete!\n")

if __name__ == "__main__":
    main()
