from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ClassifierPredictionResult:
    """
    Represents the basic prediction output from the classifier.

    Attributes:
        label (int): Predicted class label; 0 for safe or 1 for unsafe.
        confidence (float): Confidence score of the prediction, between 0.0 and 1.0.
    """

    label: int
    confidence: float


@dataclass
class SafetyReport(ClassifierPredictionResult):
    """
    Represents a detailed safety evaluation report for a prompt.

    Extends:
        ClassifierPredictionResult

    Attributes:
        score (Optional[float]): Numeric safety score between 0.0 (safe) and 1.0 (unsafe).
        explanation (str): Detailed explanation of why the prompt was flagged.
        recommendation (str): Suggested action based on the evaluation.
        fallback (bool): Whether the fallback mechanism was triggered. Defaults to False.
    """

    score: Optional[float]
    explanation: str
    recommendation: str
    fallback: bool = field(default=False)
