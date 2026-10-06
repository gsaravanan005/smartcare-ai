"""
SmartCare AI - Masked Multi-Task Binary Cross-Entropy Loss
Computes loss and analytical gradients exclusively for samples with valid task labels,
combining task losses using configurable task weights.
"""

import numpy as np
from typing import Dict, Tuple, Optional


class MaskedMultiTaskLoss:
    """
    Implements task-masked binary cross-entropy loss with task weighting.
    Only samples with mask == 1.0 contribute to task loss and gradients.
    """

    def __init__(self, task_weights: Optional[Dict[str, float]] = None, eps: float = 1e-7):
        self.task_weights = task_weights or {"t2d": 1.0, "cvd": 1.0, "ckd": 2.5}
        self.eps = eps

    def compute_loss(
        self,
        y_preds: Dict[str, np.ndarray],
        y_trues: Dict[str, np.ndarray],
        masks: Dict[str, np.ndarray]
    ) -> Tuple[float, Dict[str, float]]:
        """
        Computes weighted total loss and individual task losses.
        
        Args:
            y_preds: Dict of predicted probabilities in [0, 1] for each task.
            y_trues: Dict of binary ground truth labels in {0, 1}.
            masks: Dict of binary masks in {0, 1} indicating valid task label presence.
            
        Returns:
            total_loss: Scalar weighted sum of task losses.
            task_losses: Dict of unweighted task losses.
        """
        task_losses = {}
        total_loss = 0.0

        for task in ["t2d", "cvd", "ckd"]:
            p = np.clip(y_preds[task], self.eps, 1.0 - self.eps)
            y = y_trues[task]
            m = masks[task]

            valid_count = np.sum(m)
            if valid_count > 0:
                bce = -(y * np.log(p) + (1.0 - y) * np.log(1.0 - p))
                task_loss = float(np.sum(bce * m) / (valid_count + self.eps))
            else:
                task_loss = 0.0

            task_losses[task] = task_loss
            w = self.task_weights.get(task, 1.0)
            total_loss += w * task_loss

        return total_loss, task_losses

    def compute_gradients(
        self,
        y_preds: Dict[str, np.ndarray],
        y_trues: Dict[str, np.ndarray],
        masks: Dict[str, np.ndarray]
    ) -> Dict[str, np.ndarray]:
        """
        Computes analytical gradient of total loss w.r.t logits (z) for each task head:
        dL/dz_i = w_task * (p_i - y_i) * m_i / (sum(m) + eps)
        
        Returns:
            d_logits: Dict mapping task name to gradient array of shape (N, 1).
        """
        d_logits = {}

        for task in ["t2d", "cvd", "ckd"]:
            p = y_preds[task].reshape(-1, 1)
            y = y_trues[task].reshape(-1, 1)
            m = masks[task].reshape(-1, 1)

            valid_count = np.sum(m)
            w = self.task_weights.get(task, 1.0)

            if valid_count > 0:
                grad = w * (p - y) * m / (valid_count + self.eps)
            else:
                grad = np.zeros_like(p)

            d_logits[task] = grad

        return d_logits
