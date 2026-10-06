#!/usr/bin/env python
"""
SmartCare AI - Module 1 Preprocessing Pipeline Execution CLI Script
Reproducibly processes Diabetes, CVD, and CKD datasets and exports artifacts to Module 2.
"""
import sys
import os
import argparse
import json

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.services.preprocessing_pipeline_service import PreprocessingPipelineService

def main():
    parser = argparse.ArgumentParser(description="SmartCare AI - Module 1 Pipeline Runner")
    parser.add_argument("--dataset", type=str, default="all", choices=["diabetes", "cardio", "ckd", "all"], help="Dataset to process")
    parser.add_argument("--imputation", type=str, default="median", choices=["mean", "median", "mode", "knn", "iterative"], help="Imputation strategy")
    parser.add_argument("--outlier", type=str, default="iqr_capping", choices=["iqr_capping", "zscore_capping", "removal", "keep"], help="Outlier treatment")
    parser.add_argument("--encoding", type=str, default="onehot", choices=["onehot", "ordinal"], help="Categorical encoding")
    parser.add_argument("--scaling", type=str, default="standard", choices=["standard", "minmax"], help="Numerical scaling")
    parser.add_argument("--feature-selection", type=str, default="select_k_best", choices=["select_k_best", "mutual_info", "rfe", "all"], help="Feature selection method")
    parser.add_argument("--k-features", type=int, default=15, help="Number of top features to select")
    parser.add_argument("--imbalance", type=str, default="smote", choices=["smote", "oversampling", "undersampling", "class_weights", "none"], help="Class imbalance technique")
    parser.add_argument("--scenario", type=str, default=None, choices=["scenario_a", "scenario_b", "scenario_c", "scenario_d"], help="Missingness injection scenario for experiments")
    parser.add_argument("--injection-rate", type=float, default=0.0, help="Controlled missingness injection rate (0.05, 0.10, 0.15, 0.20)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")

    args = parser.parse_args()

    datasets = ["diabetes", "cardio", "ckd"] if args.dataset == "all" else [args.dataset]
    print("\n=======================================================")
    print("      SMARTCARE AI - MODULE 1 PIPELINE RUNNER        ")
    print("=======================================================\n")

    for d in datasets:
        print(f"[*] Processing dataset: {d.upper()}...")
        res = PreprocessingPipelineService.run_pipeline(
            dataset_name=d,
            imputation_method=args.imputation,
            outlier_strategy=args.outlier,
            encoding_strategy=args.encoding,
            scaling_strategy=args.scaling,
            feature_selection_method=args.feature_selection,
            k_features=args.k_features,
            class_imbalance_method=args.imbalance,
            missingness_injection_scenario=args.scenario,
            missingness_injection_rate=args.injection_rate,
            random_seed=args.seed
        )
        print(f"  [+] Status: {res['status']}")
        print(f"  [+] Train shape: {res['train_shape']} | Val shape: {res['val_shape']} | Test shape: {res['test_shape']}")
        print(f"  [+] Selected features ({len(res['selected_features'])}): {res['selected_features'][:5]}...")
        print(f"  [+] Pipeline artifact saved: {res['artifacts_exported'][3]}")
        print("-" * 55)

    print("\n[SUCCESS] Module 1 pipeline execution completed! All Module 2 input artifacts are ready in 'artifacts/module2_inputs/'.\n")

if __name__ == "__main__":
    main()
