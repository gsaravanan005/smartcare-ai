"""
SmartCare AI - Multi-Task Learning (MTL) Training, Calibration & Evaluation Pipeline
Orchestrates training of the shared representation network with task masking,
calibrates task probabilities, evaluates held-out test performance, conducts baseline comparisons,
performs ablation studies, and serializes all artifacts.
"""

import os
import sys
import json
import copy
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List, Optional
import matplotlib.pyplot as plt

# Ensure paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.insert(0, os.path.abspath("backend"))

from ml.multitask.config import MTLConfig
from ml.multitask.dataset import MTLDatasetManager, TaskBalancedBatchIterator
from ml.multitask.model import MultiTaskNeuralNetwork
from ml.multitask.loss import MaskedMultiTaskLoss
from ml.multitask.calibration import MultiTaskCalibrator
from ml.multitask.evaluate import MultiTaskEvaluator


def train_mtl_pipeline(
    config: Optional[MTLConfig] = None,
    run_ablation: bool = True,
    run_baselines: bool = True
) -> Dict[str, Any]:
    cfg = config or MTLConfig()
    os.makedirs(cfg.models_dir, exist_ok=True)
    os.makedirs(cfg.artifacts_dir, exist_ok=True)

    print("\n" + "=" * 65)
    print("   SMARTCARE AI - MULTI-TASK LEARNING (MTL) TRAINING PIPELINE   ")
    print("=" * 65 + "\n")

    # 1. Dataset Preparation
    print("[*] Harmonizing features and splitting cohorts (70% Train, 15% Val, 15% Test)...")
    data_mgr = MTLDatasetManager(config=cfg)
    prep_data = data_mgr.prepare_multitask_data(
        train_ratio=0.70, val_ratio=0.15, test_ratio=0.15, random_seed=cfg.random_seed
    )
    scaled_splits = prep_data["scaled_splits"]
    train_splits = {d: scaled_splits[d]["train"] for d in ["t2d", "cvd", "ckd"]}
    val_splits = {d: scaled_splits[d]["val"] for d in ["t2d", "cvd", "ckd"]}
    test_splits = {d: scaled_splits[d]["test"] for d in ["t2d", "cvd", "ckd"]}

    print(f"  [+] Cohort Split Sizes:")
    for d in ["t2d", "cvd", "ckd"]:
        print(f"      - {d.upper()}: Train N={len(train_splits[d][0])}, Val N={len(val_splits[d][0])}, Test N={len(test_splits[d][0])}")
    print(f"  [+] Harmonized Feature Count: {len(cfg.all_features)} features")

    # 2. Model & Loss Initialization
    print(f"\n[*] Initializing Shared Encoder Neural Network & Task-Masked Loss...")
    model = MultiTaskNeuralNetwork(config=cfg)
    loss_fn = MaskedMultiTaskLoss(task_weights=cfg.task_weights)

    # 3. Training Loop with Early Stopping
    print(f"[*] Training MTL Model for up to {cfg.epochs} epochs (Batch Size: {cfg.batch_size}, LR: {cfg.learning_rate})...")
    history = {
        "epoch": [], "train_loss": [], "t2d_loss": [], "cvd_loss": [], "ckd_loss": [],
        "val_loss": [], "val_mean_auc": []
    }

    best_val_auc = -1.0
    best_weights = None
    patience_counter = 0
    current_lr = cfg.learning_rate

    for epoch in range(1, cfg.epochs + 1):
        # LR Step Decay
        if epoch > 1 and epoch % cfg.lr_decay_step == 0:
            current_lr *= cfg.lr_decay_gamma

        # Iterate over mini-batches
        batch_iter = TaskBalancedBatchIterator(
            train_splits["t2d"], train_splits["cvd"], train_splits["ckd"],
            batch_size=cfg.batch_size, ckd_ratio=cfg.ckd_batch_sample_ratio, random_seed=cfg.random_seed + epoch
        )

        epoch_losses = []
        epoch_t2d = []
        epoch_cvd = []
        epoch_ckd = []

        for X_batch, y_dict, mask_dict in batch_iter:
            # Forward pass
            y_preds, _ = model.forward(X_batch, training=True)

            # Compute masked loss
            total_loss, task_losses = loss_fn.compute_loss(y_preds, y_dict, mask_dict)
            epoch_losses.append(total_loss)
            epoch_t2d.append(task_losses["t2d"])
            epoch_cvd.append(task_losses["cvd"])
            epoch_ckd.append(task_losses["ckd"])

            # Compute gradients & backprop
            d_logits = loss_fn.compute_gradients(y_preds, y_dict, mask_dict)
            model.backward(d_logits)

            # Optimizer update
            model.optimizer_step(lr=current_lr)

        avg_train_loss = float(np.mean(epoch_losses))
        avg_t2d = float(np.mean(epoch_t2d))
        avg_cvd = float(np.mean(epoch_cvd))
        avg_ckd = float(np.mean(epoch_ckd))

        # Evaluate on validation splits
        val_preds = {}
        val_targets = {}
        val_masks = {}
        val_aucs = []

        for d in ["t2d", "cvd", "ckd"]:
            X_va, y_va = val_splits[d]
            p_va = model.forward(X_va, training=False)[0][d]
            val_preds[d] = p_va
            val_targets[d] = y_va.values
            val_masks[d] = np.ones(len(y_va))
            from sklearn.metrics import roc_auc_score
            val_aucs.append(roc_auc_score(y_va.values, p_va))

        val_total_loss, _ = loss_fn.compute_loss(val_preds, val_targets, val_masks)
        mean_val_auc = float(np.mean(val_aucs))

        history["epoch"].append(epoch)
        history["train_loss"].append(round(avg_train_loss, 4))
        history["t2d_loss"].append(round(avg_t2d, 4))
        history["cvd_loss"].append(round(avg_cvd, 4))
        history["ckd_loss"].append(round(avg_ckd, 4))
        history["val_loss"].append(round(val_total_loss, 4))
        history["val_mean_auc"].append(round(mean_val_auc, 4))

        if epoch % 5 == 0 or epoch == 1:
            print(f"  [+] Epoch {epoch:02d}/{cfg.epochs:02d} | Train Loss: {avg_train_loss:.4f} (T2D: {avg_t2d:.4f}, CVD: {avg_cvd:.4f}, CKD: {avg_ckd:.4f}) | Val Loss: {val_total_loss:.4f} | Val Mean AUC: {mean_val_auc:.4f}")

        # Checkpointing & Early stopping
        if mean_val_auc > best_val_auc + 1e-4:
            best_val_auc = mean_val_auc
            best_weights = copy.deepcopy(model)
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= cfg.early_stopping_patience:
                print(f"  [!] Early stopping triggered at epoch {epoch} (Best Val Mean AUC: {best_val_auc:.4f})")
                break

    if best_weights is not None:
        model = best_weights
    model.is_fitted = True

    # 4. Post-Training Probability Calibration & Threshold Tuning
    print(f"\n[*] Calibrating task head probabilities on validation split...")
    calibrator = MultiTaskCalibrator(method="sigmoid")
    calib_reports = calibrator.fit_and_evaluate(model, val_splits)

    for d in ["t2d", "cvd", "ckd"]:
        cr = calib_reports[d]
        print(f"  [+] {d.upper()} Calibration: Brier: {cr['uncalibrated_brier']} -> {cr['calibrated_brier']} (ECE: {cr['calibrated_ece']:.4f}) | Optimal Threshold: {cr['optimal_threshold']}")

    # 5. Held-out Test Set Evaluation
    print(f"\n[*] Evaluating MTL Model on held-out test splits...")
    test_metrics = MultiTaskEvaluator.evaluate_model_on_test_splits(
        model, test_splits, calibrator=calibrator, thresholds=calibrator.optimal_thresholds
    )

    print("\n" + "=" * 65)
    print("      NEW MULTI-TASK LEARNING TEST EVALUATION RESULTS      ")
    print("=" * 65)
    for d in ["t2d", "cvd", "ckd"]:
        m = test_metrics[d]
        print(f"[*] {d.upper()}:")
        print(f"    - Accuracy: {m['accuracy']} | Precision: {m['precision']} | Recall: {m['recall']} | Specificity: {m['specificity']} | F1: {m['f1_score']}")
        print(f"    - ROC-AUC: {m['roc_auc']} | PR-AUC: {m['pr_auc']} | Brier: {m['brier_score']} | ECE: {m['ece']}")
        print(f"    - Confusion Matrix: TP={m['confusion_matrix']['tp']}, FP={m['confusion_matrix']['fp']}, TN={m['confusion_matrix']['tn']}, FN={m['confusion_matrix']['fn']}")
        print("-" * 65)

    # 6. Baseline Models Comparison
    baseline_metrics = {}
    if run_baselines:
        print(f"\n[*] Training and evaluating baseline models (Logistic Regression, Random Forest, XGBoost)...")
        baseline_metrics = MultiTaskEvaluator.train_and_evaluate_baselines(train_splits, test_splits, random_seed=cfg.random_seed)

    # 7. Subgroup Analysis & Decision Curve Analysis
    print(f"\n[*] Computing Age & Sex subgroup analysis and Decision Curve Analysis...")
    subgroups = MultiTaskEvaluator.perform_subgroup_analysis(
        model, test_splits, calibrator=calibrator, thresholds=calibrator.optimal_thresholds
    )

    dca_results = {}
    for d in ["t2d", "cvd", "ckd"]:
        p_te = calibrator.calibrators[d].predict_proba(model.forward(test_splits[d][0], training=False)[0][d])
        dca_results[d] = MultiTaskEvaluator.compute_decision_curve_analysis(p_te, test_splits[d][1].values)

    # 8. Ablation Study
    ablation_results = {}
    if run_ablation:
        print(f"\n[*] Running Ablation Study (Retraining MTL on feature sub-configurations)...")
        ablation_configs = {
            "Full Feature Set (Proposed)": cfg.all_features,
            "Demographics Only": cfg.DEMOGRAPHIC_FEATURES,
            "Vital Signs Only": cfg.VITAL_FEATURES,
            "Laboratory Biomarkers Only": cfg.LABORATORY_FEATURES,
            "Lifestyle & Behavioral Only": cfg.LIFESTYLE_FEATURES,
            "Without Engineered Cardiometabolic": [
                f for f in cfg.all_features
                if f not in ["pulse_pressure", "mean_arterial_pressure", "bun_creatinine_ratio", "egfr_proxy", "anemia_flag", "combined_vascular_risk"]
            ]
        }

        for config_name, feature_subset in ablation_configs.items():
            if config_name == "Full Feature Set (Proposed)":
                ablation_results[config_name] = {
                    d: {"roc_auc": test_metrics[d]["roc_auc"], "f1": test_metrics[d]["f1_score"], "recall": test_metrics[d]["recall"]}
                    for d in ["t2d", "cvd", "ckd"]
                }
                continue

            print(f"  [+] Retraining MTL for config: '{config_name}' ({len(feature_subset)} features)...")
            sub_cfg = copy.deepcopy(cfg)
            sub_cfg.epochs = 20  # Fast ablation training
            sub_model = MultiTaskNeuralNetwork(config=sub_cfg, input_dim=len(feature_subset))

            # Subset data
            sub_tr = {d: (train_splits[d][0][feature_subset], train_splits[d][1]) for d in ["t2d", "cvd", "ckd"]}
            sub_te = {d: (test_splits[d][0][feature_subset], test_splits[d][1]) for d in ["t2d", "cvd", "ckd"]}

            for ep in range(1, sub_cfg.epochs + 1):
                b_iter = TaskBalancedBatchIterator(
                    sub_tr["t2d"], sub_tr["cvd"], sub_tr["ckd"],
                    batch_size=sub_cfg.batch_size, ckd_ratio=sub_cfg.ckd_batch_sample_ratio, random_seed=sub_cfg.random_seed + ep
                )
                for X_b, y_d, m_d in b_iter:
                    y_p, _ = sub_model.forward(X_b, training=True)
                    d_l = loss_fn.compute_gradients(y_p, y_d, m_d)
                    sub_model.backward(d_l)
                    sub_model.optimizer_step(lr=sub_cfg.learning_rate)

            sub_eval = MultiTaskEvaluator.evaluate_model_on_test_splits(sub_model, sub_te)
            ablation_results[config_name] = {
                d: {"roc_auc": sub_eval[d]["roc_auc"], "f1": sub_eval[d]["f1_score"], "recall": sub_eval[d]["recall"]}
                for d in ["t2d", "cvd", "ckd"]
            }

    # 9. Plot and Save Training Curves
    print(f"\n[*] Generating training curves and calibration figures...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    ax1.plot(history["epoch"], history["train_loss"], label="Total Train Loss", color="#0284c7", lw=2)
    ax1.plot(history["epoch"], history["val_loss"], label="Total Val Loss", color="#dc2626", lw=2, linestyle="--")
    ax1.set_xlabel("Epoch", fontweight="bold")
    ax1.set_ylabel("Loss", fontweight="bold")
    ax1.set_title("MTL Joint Optimization Loss Curve", fontweight="bold")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(history["epoch"], history["t2d_loss"], label="T2D Loss", color="#0284c7", lw=1.5)
    ax2.plot(history["epoch"], history["cvd_loss"], label="CVD Loss", color="#ea580c", lw=1.5)
    ax2.plot(history["epoch"], history["ckd_loss"], label="CKD Loss", color="#9333ea", lw=1.5)
    ax2.plot(history["epoch"], history["val_mean_auc"], label="Val Mean AUC", color="#16a34a", lw=2, linestyle=":")
    ax2.set_xlabel("Epoch", fontweight="bold")
    ax2.set_ylabel("Metric Value", fontweight="bold")
    ax2.set_title("Task Losses & Validation Performance", fontweight="bold")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    curve_path = os.path.join(cfg.artifacts_dir, "mtl_training_curves.png")
    fig.savefig(curve_path, dpi=200)
    plt.close()

    # 10. Serialize Model Artifacts
    print(f"\n[*] Serializing MTL Model and Preprocessing Artifacts...")
    model_bundle = {
        "model": model,
        "model_version": "smartcare_mtl_v1",
        "architecture": "SharedFeatureEncoder_MultiTaskHead",
        "feature_names": cfg.all_features,
        "input_dim": cfg.input_dim,
        "shared_dims": cfg.shared_hidden_dims,
        "task_dim": cfg.task_hidden_dim,
        "thresholds": calibrator.optimal_thresholds,
        "metrics": test_metrics
    }
    model_save_path = os.path.join(cfg.models_dir, "smartcare_mtl_model.joblib")
    joblib.dump(model_bundle, model_save_path)

    # Preprocessing scaler & imputer
    prep_save_path = os.path.join(cfg.models_dir, "preprocessing.pkl")
    joblib.dump({
        "scaler": data_mgr.scaler,
        "imputer": data_mgr.imputer,
        "feature_names": cfg.all_features
    }, prep_save_path)

    # Separate calibration objects
    for d in ["t2d", "cvd", "ckd"]:
        calib_save_path = os.path.join(cfg.models_dir, f"calibration_{d}.pkl")
        joblib.dump(calibrator.calibrators[d], calib_save_path)

    # Thresholds JSON
    th_json_path = os.path.join(cfg.models_dir, "thresholds.json")
    with open(th_json_path, "w") as f:
        json.dump({
            "thresholds": calibrator.optimal_thresholds,
            "methodology": "Validation set F1 maximization under minimum clinical sensitivity constraints (T2D>=0.75, CVD>=0.75, CKD>=0.85)",
            "default_thresholds": cfg.default_thresholds
        }, f, indent=2)

    # Feature schema JSON
    schema_json_path = os.path.join(cfg.models_dir, "feature_schema.json")
    with open(schema_json_path, "w") as f:
        json.dump({
            "total_features": len(cfg.all_features),
            "all_features": cfg.all_features,
            "demographic": cfg.DEMOGRAPHIC_FEATURES,
            "vital_signs": cfg.VITAL_FEATURES,
            "laboratory": cfg.LABORATORY_FEATURES,
            "lifestyle": cfg.LIFESTYLE_FEATURES,
            "history_comorbidities": cfg.HISTORY_FEATURES
        }, f, indent=2)

    # Metadata JSON
    metadata = {
        "model_name": "SmartCare AI Multi-Task Neural Network",
        "model_version": "smartcare_mtl_v1",
        "architecture": {
            "type": "SharedFeatureEncoder",
            "shared_layers": [f"Dense({cfg.input_dim} -> 64) + LayerNorm + ReLU + Dropout(0.15)", "Dense(64 -> 32) + LayerNorm + ReLU"],
            "shared_latent_dimension": 32,
            "task_heads": {
                "t2d": "Dense(32 -> 16) + ReLU + Dense(16 -> 1) + Sigmoid",
                "cvd": "Dense(32 -> 16) + ReLU + Dense(16 -> 1) + Sigmoid",
                "ckd": "Dense(32 -> 16) + ReLU + Dense(16 -> 1) + Sigmoid"
            }
        },
        "training_configuration": {
            "epochs_completed": len(history["epoch"]),
            "batch_size": cfg.batch_size,
            "learning_rate": cfg.learning_rate,
            "task_weights": cfg.task_weights,
            "ckd_batch_sample_ratio": cfg.ckd_batch_sample_ratio,
            "random_seed": cfg.random_seed
        },
        "sample_counts": {
            "t2d": {"train": len(train_splits["t2d"][0]), "val": len(val_splits["t2d"][0]), "test": len(test_splits["t2d"][0])},
            "cvd": {"train": len(train_splits["cvd"][0]), "val": len(val_splits["cvd"][0]), "test": len(test_splits["cvd"][0])},
            "ckd": {"train": len(train_splits["ckd"][0]), "val": len(val_splits["ckd"][0]), "test": len(test_splits["ckd"][0])}
        },
        "test_metrics": test_metrics,
        "calibration_reports": calib_reports,
        "baseline_comparison": baseline_metrics,
        "ablation_study": ablation_results,
        "subgroup_analysis": subgroups,
        "dca_results": dca_results
    }

    meta_save_path = os.path.join(cfg.models_dir, "metadata.json")
    with open(meta_save_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print("\n[SUCCESS] Multi-Task Model Training, Calibration & Evaluation Pipeline Complete!\n")
    return metadata


if __name__ == "__main__":
    train_mtl_pipeline()
