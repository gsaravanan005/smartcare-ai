"""
SmartCare AI - Multi-Task Shared Representation Neural Network
Implements a shared-feature encoder coupled with 3 independent disease heads (T2D, CVD, CKD),
analytical forward/backward propagation, Adam optimization, and scikit-learn compatible interfaces.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List, Optional
from .config import MTLConfig


class DenseLayer:
    """Fully connected layer with He/Xavier initialization and L2 regularization."""
    def __init__(self, in_features: int, out_features: int, rng: np.random.Generator, name: str = "dense"):
        self.name = name
        limit = np.sqrt(2.0 / in_features)
        self.W = rng.normal(0.0, limit, size=(in_features, out_features)).astype(np.float32)
        self.b = np.zeros((1, out_features), dtype=np.float32)

        # Adam state
        self.mW = np.zeros_like(self.W)
        self.vW = np.zeros_like(self.W)
        self.mb = np.zeros_like(self.b)
        self.vb = np.zeros_like(self.b)

        # Gradients
        self.dW = np.zeros_like(self.W)
        self.db = np.zeros_like(self.b)

    def forward(self, X: np.ndarray) -> np.ndarray:
        self.X_cache = X
        return np.dot(X, self.W) + self.b

    def backward(self, d_out: np.ndarray, l2_reg: float = 0.0) -> np.ndarray:
        N = self.X_cache.shape[0]
        self.dW = np.dot(self.X_cache.T, d_out) + l2_reg * self.W
        self.db = np.sum(d_out, axis=0, keepdims=True)
        return np.dot(d_out, self.W.T)

    def step_adam(self, lr: float, beta1: float, beta2: float, eps: float, t: int):
        # Update weights
        self.mW = beta1 * self.mW + (1.0 - beta1) * self.dW
        self.vW = beta2 * self.vW + (1.0 - beta2) * (self.dW ** 2)
        mW_hat = self.mW / (1.0 - beta1 ** t)
        vW_hat = self.vW / (1.0 - beta2 ** t)
        self.W -= lr * mW_hat / (np.sqrt(vW_hat) + eps)

        # Update biases
        self.mb = beta1 * self.mb + (1.0 - beta1) * self.db
        self.vb = beta2 * self.vb + (1.0 - beta2) * (self.db ** 2)
        mb_hat = self.mb / (1.0 - beta1 ** t)
        vb_hat = self.vb / (1.0 - beta2 ** t)
        self.b -= lr * mb_hat / (np.sqrt(vb_hat) + eps)


class LayerNorm:
    """Layer Normalization across features."""
    def __init__(self, features: int, eps: float = 1e-5):
        self.gamma = np.ones((1, features), dtype=np.float32)
        self.beta = np.zeros((1, features), dtype=np.float32)
        self.eps = eps

        self.m_gamma = np.zeros_like(self.gamma)
        self.v_gamma = np.zeros_like(self.gamma)
        self.m_beta = np.zeros_like(self.beta)
        self.v_beta = np.zeros_like(self.beta)

        self.d_gamma = np.zeros_like(self.gamma)
        self.d_beta = np.zeros_like(self.beta)

    def forward(self, X: np.ndarray) -> np.ndarray:
        self.mean = np.mean(X, axis=-1, keepdims=True)
        self.var = np.var(X, axis=-1, keepdims=True)
        self.x_hat = (X - self.mean) / np.sqrt(self.var + self.eps)
        return self.gamma * self.x_hat + self.beta

    def backward(self, d_out: np.ndarray) -> np.ndarray:
        N, D = d_out.shape
        self.d_gamma = np.sum(d_out * self.x_hat, axis=0, keepdims=True)
        self.d_beta = np.sum(d_out, axis=0, keepdims=True)

        std_inv = 1.0 / np.sqrt(self.var + self.eps)
        dxhat = d_out * self.gamma
        dvar = np.sum(dxhat * (self.x_hat * -0.5 * std_inv), axis=-1, keepdims=True)
        dmean = np.sum(dxhat * -std_inv, axis=-1, keepdims=True) + dvar * np.mean(-2.0 * (self.x_hat * std_inv), axis=-1, keepdims=True)
        dx = dxhat * std_inv + dvar * 2.0 * (self.x_hat * std_inv) / D + dmean / D
        return dx

    def step_adam(self, lr: float, beta1: float, beta2: float, eps: float, t: int):
        self.m_gamma = beta1 * self.m_gamma + (1.0 - beta1) * self.d_gamma
        self.v_gamma = beta2 * self.v_gamma + (1.0 - beta2) * (self.d_gamma ** 2)
        mg_hat = self.m_gamma / (1.0 - beta1 ** t)
        vg_hat = self.v_gamma / (1.0 - beta2 ** t)
        self.gamma -= lr * mg_hat / (np.sqrt(vg_hat) + eps)

        self.m_beta = beta1 * self.m_beta + (1.0 - beta1) * self.d_beta
        self.v_beta = beta2 * self.v_beta + (1.0 - beta2) * (self.d_beta ** 2)
        mb_hat = self.m_beta / (1.0 - beta1 ** t)
        vb_hat = self.v_beta / (1.0 - beta2 ** t)
        self.beta -= lr * mb_hat / (np.sqrt(vb_hat) + eps)


class TaskHead:
    """Disease-specific classification head taking shared representation to risk probability."""
    def __init__(self, in_features: int, hidden_dim: int, rng: np.random.Generator, name: str = "head"):
        self.name = name
        self.fc1 = DenseLayer(in_features, hidden_dim, rng, name=f"{name}_fc1")
        self.fc2 = DenseLayer(hidden_dim, 1, rng, name=f"{name}_fc2")

    def forward(self, Z: np.ndarray, training: bool = False) -> Tuple[np.ndarray, np.ndarray]:
        h1 = self.fc1.forward(Z)
        a1 = np.maximum(0, h1)  # ReLU
        self.relu_mask = (h1 > 0).astype(np.float32)
        logits = self.fc2.forward(a1)
        # Numerical stable Sigmoid
        probs = 1.0 / (1.0 + np.exp(-np.clip(logits, -20.0, 20.0)))
        return probs.ravel(), logits

    def backward(self, d_logits: np.ndarray, l2_reg: float = 0.0) -> np.ndarray:
        d_a1 = self.fc2.backward(d_logits, l2_reg=l2_reg)
        d_h1 = d_a1 * self.relu_mask
        d_Z = self.fc1.backward(d_h1, l2_reg=l2_reg)
        return d_Z

    def step_adam(self, lr: float, beta1: float, beta2: float, eps: float, t: int):
        self.fc1.step_adam(lr, beta1, beta2, eps, t)
        self.fc2.step_adam(lr, beta1, beta2, eps, t)


class MultiTaskNeuralNetwork:
    """
    Genuine Multi-Task Learning (MTL) Neural Network for SmartCare AI.
    
    Structure:
        Input Features (25)
               │
               ▼
        Shared Encoder:
          - Dense(25 -> 64) -> LayerNorm -> ReLU -> Dropout(0.15)
          - Dense(64 -> 32) -> LayerNorm -> ReLU
               │
               ▼ Shared Representation Z (32)
          ┌────┴────┬───────────┐
          ▼         ▼           ▼
       T2D Head  CVD Head    CKD Head
       (32->16->1)(32->16->1) (32->16->1)
          │         │           │
          ▼         ▼           ▼
       T2D Risk  CVD Risk    CKD Risk
    """

    def __init__(self, config: Optional[MTLConfig] = None, input_dim: Optional[int] = None):
        self.config = config or MTLConfig()
        self.input_dim = input_dim if input_dim is not None else self.config.input_dim
        self.shared_dims = self.config.shared_hidden_dims  # (64, 32)
        self.task_dim = self.config.task_hidden_dim        # 16
        self.dropout_rate = self.config.dropout_rate
        self.l2_reg = self.config.l2_reg
        self.seed = self.config.random_seed
        self.rng = np.random.default_rng(self.seed)

        # 1. Shared Feature Encoder Layers
        self.shared_fc1 = DenseLayer(self.input_dim, self.shared_dims[0], self.rng, name="shared_fc1")
        self.shared_ln1 = LayerNorm(self.shared_dims[0])
        self.shared_fc2 = DenseLayer(self.shared_dims[0], self.shared_dims[1], self.rng, name="shared_fc2")
        self.shared_ln2 = LayerNorm(self.shared_dims[1])

        # 2. Disease Task Heads
        self.head_t2d = TaskHead(self.shared_dims[1], self.task_dim, self.rng, name="head_t2d")
        self.head_cvd = TaskHead(self.shared_dims[1], self.task_dim, self.rng, name="head_cvd")
        self.head_ckd = TaskHead(self.shared_dims[1], self.task_dim, self.rng, name="head_ckd")

        # Optimizer step counter
        self.adam_step = 0
        self.is_fitted = False

    def forward(self, X: np.ndarray, training: bool = False) -> Tuple[Dict[str, np.ndarray], np.ndarray]:
        """
        Executes forward propagation through the shared encoder and all 3 task heads.
        
        Returns:
            probs_dict: {'t2d': (N,), 'cvd': (N,), 'ckd': (N,)}
            Z: Shared latent representation (N, 32)
        """
        if isinstance(X, pd.DataFrame):
            X_arr = X.values.astype(np.float32)
        else:
            X_arr = np.asarray(X, dtype=np.float32)

        # Shared Layer 1
        h1 = self.shared_fc1.forward(X_arr)
        ln1 = self.shared_ln1.forward(h1)
        a1 = np.maximum(0, ln1)
        self.relu_mask1 = (ln1 > 0).astype(np.float32)

        if training and self.dropout_rate > 0.0:
            self.drop_mask1 = (self.rng.random(a1.shape) >= self.dropout_rate).astype(np.float32) / (1.0 - self.dropout_rate)
            a1 = a1 * self.drop_mask1
        else:
            self.drop_mask1 = None

        # Shared Layer 2
        h2 = self.shared_fc2.forward(a1)
        ln2 = self.shared_ln2.forward(h2)
        Z = np.maximum(0, ln2)  # Shared representation Z (N, 32)
        self.relu_mask2 = (ln2 > 0).astype(np.float32)

        # Task Heads
        p_t2d, logits_t2d = self.head_t2d.forward(Z, training=training)
        p_cvd, logits_cvd = self.head_cvd.forward(Z, training=training)
        p_ckd, logits_ckd = self.head_ckd.forward(Z, training=training)

        probs = {
            "t2d": p_t2d,
            "cvd": p_cvd,
            "ckd": p_ckd
        }
        return probs, Z

    def backward(self, d_logits: Dict[str, np.ndarray]):
        """
        Executes analytical backpropagation.
        Couples task gradients at shared representation Z and propagates to all shared layers.
        """
        # Backprop through separate heads
        d_Z_t2d = self.head_t2d.backward(d_logits["t2d"], l2_reg=self.l2_reg)
        d_Z_cvd = self.head_cvd.backward(d_logits["cvd"], l2_reg=self.l2_reg)
        d_Z_ckd = self.head_ckd.backward(d_logits["ckd"], l2_reg=self.l2_reg)

        # Key Multi-Task Learning Joint Gradient Combination
        d_Z_total = d_Z_t2d + d_Z_cvd + d_Z_ckd

        # Backprop through Shared Layer 2
        d_ln2 = d_Z_total * self.relu_mask2
        d_h2 = self.shared_ln2.backward(d_ln2)
        d_a1 = self.shared_fc2.backward(d_h2, l2_reg=self.l2_reg)

        if self.drop_mask1 is not None:
            d_a1 = d_a1 * self.drop_mask1

        # Backprop through Shared Layer 1
        d_ln1 = d_a1 * self.relu_mask1
        d_h1 = self.shared_ln1.backward(d_ln1)
        self.shared_fc1.backward(d_h1, l2_reg=self.l2_reg)

    def optimizer_step(self, lr: float, beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8):
        """Applies Adam update to shared encoder and all 3 heads."""
        self.adam_step += 1
        t = self.adam_step

        # Shared encoder update
        self.shared_fc1.step_adam(lr, beta1, beta2, eps, t)
        self.shared_ln1.step_adam(lr, beta1, beta2, eps, t)
        self.shared_fc2.step_adam(lr, beta1, beta2, eps, t)
        self.shared_ln2.step_adam(lr, beta1, beta2, eps, t)

        # Heads update
        self.head_t2d.step_adam(lr, beta1, beta2, eps, t)
        self.head_cvd.step_adam(lr, beta1, beta2, eps, t)
        self.head_ckd.step_adam(lr, beta1, beta2, eps, t)

    def get_shared_representation(self, X: Any) -> np.ndarray:
        """Returns the learned 32-dimensional shared representation vector."""
        _, Z = self.forward(X, training=False)
        return Z

    def predict_proba(self, X: Any, task: str = "all") -> Any:
        """
        Scikit-learn compatible predict_proba.
        If task in ['t2d', 'cvd', 'ckd'], returns (N, 2) array [1-p, p].
        If task == 'all', returns dict of (N, 2) arrays.
        """
        probs_dict, _ = self.forward(X, training=False)

        if task in ["t2d", "cvd", "ckd"]:
            p1 = probs_dict[task]
            p0 = 1.0 - p1
            return np.column_stack([p0, p1])

        return {
            t: np.column_stack([1.0 - probs_dict[t], probs_dict[t]])
            for t in ["t2d", "cvd", "ckd"]
        }

    def predict(self, X: Any, task: str = "t2d", threshold: float = 0.5) -> np.ndarray:
        """Scikit-learn compatible binary predict method."""
        proba = self.predict_proba(X, task=task)[:, 1]
        return (proba >= threshold).astype(int)

    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        return {
            "input_dim": self.input_dim,
            "shared_hidden_dims": self.shared_dims,
            "task_hidden_dim": self.task_dim,
            "dropout_rate": self.dropout_rate,
            "l2_reg": self.l2_reg,
            "seed": self.seed
        }

    def set_params(self, **parameters):
        for param, value in parameters.items():
            setattr(self, param, value)
        return self
