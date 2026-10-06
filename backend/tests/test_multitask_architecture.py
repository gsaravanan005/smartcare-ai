"""
SmartCare AI - Automated Multi-Task Architecture Validation Test
Strictly verifies that:
1. There is one shared feature encoder.
2. T2D, CVD, and CKD heads receive the shared representation.
3. Shared parameters are jointly trainable and receive combined gradients from multiple tasks.
4. Task-specific heads are structurally independent.
5. Task-masked loss and gradients behave correctly.
6. The model is NOT three separate independent networks.
"""

import pytest
import os
import sys
import numpy as np
import pandas as pd

# Add backend and root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ml.multitask.config import MTLConfig
from ml.multitask.model import MultiTaskNeuralNetwork, TaskHead, DenseLayer
from ml.multitask.loss import MaskedMultiTaskLoss
from ml.multitask.dataset import MTLDatasetManager, TaskBalancedBatchIterator


def test_shared_encoder_and_task_heads_structure():
    """Verifies that 1 shared encoder exists and feeds into 3 separate heads."""
    config = MTLConfig()
    model = MultiTaskNeuralNetwork(config=config)

    # 1. Verify shared encoder layers exist
    assert hasattr(model, "shared_fc1")
    assert hasattr(model, "shared_ln1")
    assert hasattr(model, "shared_fc2")
    assert hasattr(model, "shared_ln2")

    # 2. Verify 3 separate task heads exist
    assert hasattr(model, "head_t2d")
    assert hasattr(model, "head_cvd")
    assert hasattr(model, "head_ckd")

    # 3. Verify heads are distinct objects
    assert model.head_t2d is not model.head_cvd
    assert model.head_cvd is not model.head_ckd
    assert model.head_t2d is not model.head_ckd

    # 4. Forward pass produces shared latent representation and 3 probabilities
    N = 10
    X_dummy = np.random.randn(N, config.input_dim).astype(np.float32)
    probs, Z = model.forward(X_dummy, training=False)

    assert Z.shape == (N, 32), f"Shared representation Z must have shape (N, 32), got {Z.shape}"
    assert "t2d" in probs and "cvd" in probs and "ckd" in probs
    assert probs["t2d"].shape == (N,)
    assert probs["cvd"].shape == (N,)
    assert probs["ckd"].shape == (N,)

    # Verify probability bounds [0.0, 1.0]
    for task in ["t2d", "cvd", "ckd"]:
        assert np.all(probs[task] >= 0.0) and np.all(probs[task] <= 1.0)


def test_joint_gradient_flow_into_shared_encoder():
    """
    Verifies that shared parameters receive joint gradients from multiple tasks
    and that changing task losses directly impacts shared representation gradients.
    """
    config = MTLConfig()
    model = MultiTaskNeuralNetwork(config=config)
    loss_fn = MaskedMultiTaskLoss(task_weights={"t2d": 1.0, "cvd": 1.0, "ckd": 2.5})

    N = 6
    X_dummy = np.random.randn(N, config.input_dim).astype(np.float32)

    # Scenario A: All 3 tasks active
    y_preds, _ = model.forward(X_dummy, training=True)
    y_trues = {
        "t2d": np.array([1, 0, 1, 0, 1, 0], dtype=np.float32),
        "cvd": np.array([0, 1, 0, 1, 0, 1], dtype=np.float32),
        "ckd": np.array([1, 1, 0, 0, 1, 0], dtype=np.float32)
    }
    masks_all = {
        "t2d": np.array([1, 1, 0, 0, 0, 0], dtype=np.float32),
        "cvd": np.array([0, 0, 1, 1, 0, 0], dtype=np.float32),
        "ckd": np.array([0, 0, 0, 0, 1, 1], dtype=np.float32)
    }

    d_logits_all = loss_fn.compute_gradients(y_preds, y_trues, masks_all)
    model.backward(d_logits_all)

    shared_grad_W1_all = model.shared_fc1.dW.copy()
    shared_grad_W2_all = model.shared_fc2.dW.copy()

    assert not np.allclose(shared_grad_W1_all, 0.0), "Shared Layer 1 must receive non-zero gradients."
    assert not np.allclose(shared_grad_W2_all, 0.0), "Shared Layer 2 must receive non-zero gradients."

    # Scenario B: Zero out CKD task mask and verify shared gradient changes
    masks_no_ckd = {
        "t2d": np.array([1, 1, 0, 0, 0, 0], dtype=np.float32),
        "cvd": np.array([0, 0, 1, 1, 0, 0], dtype=np.float32),
        "ckd": np.array([0, 0, 0, 0, 0, 0], dtype=np.float32)
    }
    d_logits_no_ckd = loss_fn.compute_gradients(y_preds, y_trues, masks_no_ckd)
    assert np.allclose(d_logits_no_ckd["ckd"], 0.0), "Masked task must have zero gradient."

    model.backward(d_logits_no_ckd)
    shared_grad_W2_no_ckd = model.shared_fc2.dW.copy()

    # The shared weights MUST receive different gradients when CKD is active vs inactive
    assert not np.allclose(shared_grad_W2_all, shared_grad_W2_no_ckd), (
        "TRUE MULTI-TASK FAILURE: Shared layer gradients did not change when task composition changed! "
        "Shared parameters must be jointly driven by all active tasks."
    )


def test_task_masking_loss_and_gradient_isolation():
    """Verifies that samples masked for a task do not incur loss or gradient for that task."""
    loss_fn = MaskedMultiTaskLoss(task_weights={"t2d": 1.0, "cvd": 1.0, "ckd": 1.0})

    y_preds = {
        "t2d": np.array([0.9, 0.1]),
        "cvd": np.array([0.8, 0.2]),
        "ckd": np.array([0.7, 0.3])
    }
    y_trues = {
        "t2d": np.array([1.0, 0.0]),
        "cvd": np.array([0.0, 1.0]),
        "ckd": np.array([1.0, 0.0])
    }
    # Only T2D sample 0 is valid, CVD sample 1 is valid, CKD none
    masks = {
        "t2d": np.array([1.0, 0.0]),
        "cvd": np.array([0.0, 1.0]),
        "ckd": np.array([0.0, 0.0])
    }

    total_loss, task_losses = loss_fn.compute_loss(y_preds, y_trues, masks)
    d_logits = loss_fn.compute_gradients(y_preds, y_trues, masks)

    assert task_losses["ckd"] == 0.0, "Masked CKD task must produce 0.0 loss."
    assert np.allclose(d_logits["ckd"], 0.0), "Masked CKD task must produce 0.0 gradient."
    assert d_logits["t2d"][1] == 0.0, "Masked sample in T2D must produce 0.0 gradient."
    assert d_logits["cvd"][0] == 0.0, "Masked sample in CVD must produce 0.0 gradient."


def test_shared_representation_dimensionality_and_predict_proba():
    """Verifies that model meets scikit-learn / joblib / SHAP requirements."""
    config = MTLConfig()
    model = MultiTaskNeuralNetwork(config=config)

    X_test = pd.DataFrame(
        np.random.randn(20, len(config.all_features)),
        columns=config.all_features
    )

    # Test individual task predict_proba
    for task in ["t2d", "cvd", "ckd"]:
        proba = model.predict_proba(X_test, task=task)
        assert proba.shape == (20, 2)
        assert np.allclose(proba.sum(axis=1), 1.0)

    # Test all tasks predict_proba dict
    all_proba = model.predict_proba(X_test, task="all")
    assert isinstance(all_proba, dict)
    assert set(all_proba.keys()) == {"t2d", "cvd", "ckd"}
