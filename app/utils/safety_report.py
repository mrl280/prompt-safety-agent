from dataclasses import dataclass
from typing import Optional


@dataclass
class SafetyReport:
    """
    Represents a safety evaluation report for a prompt.

    Attributes:
        label (int): Predicted class label; 0 for safe or 1 for unsafe.
        confidence (float): Confidence score of the prediction, between 0.0 and 1.0.
        score (Optional[float]): Numeric safety score between 0.0 (safe) and 1.0 (unsafe).
        explanation (str): Detailed explanation of why the prompt was flagged.
        recommendation (str): Suggested action based on the evaluation.
        classifier (str): Name of the classification mechanism that generated the report.
    """

    label: int
    score: Optional[float]
    confidence: float
    explanation: str
    recommendation: str
    classifier: str
