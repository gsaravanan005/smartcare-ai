"""
SmartCare AI - Multi-Task Learning (MTL) Module
Provides shared representation neural architecture, task-masked loss,
dataset alignment, calibration, and explainability for T2D, CVD, and CKD.
"""

from .config import MTLConfig
from .model import MultiTaskNeuralNetwork
from .loss import MaskedMultiTaskLoss
from .dataset import MTLDatasetManager
from .calibration import MultiTaskCalibrator
from .explain import MultiTaskExplainer
from .evaluate import MultiTaskEvaluator

__all__ = [
    "MTLConfig",
    "MultiTaskNeuralNetwork",
    "MaskedMultiTaskLoss",
    "MTLDatasetManager",
    "MultiTaskCalibrator",
    "MultiTaskExplainer",
    "MultiTaskEvaluator",
]
