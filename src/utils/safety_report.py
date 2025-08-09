from dataclasses import dataclass, field


@dataclass
class SafetyReport:
    """
    Represents a safety evaluation report for a prompt.

    Attributes:
        score (float): Numeric safety score between 0.0 (safe) and 1.0 (unsafe).
        confidence (float): Confidence level of the safety assessment (0.0 to 1.0).
        explanation (str): Detailed explanation of why the prompt was flagged.
        recommendation (str): Suggested action based on the evaluation.
        fallback (bool): Whether the fallback mechanism was triggered. Defaults to False.
    """

    score: float
    confidence: float
    explanation: str
    recommendation: str
    fallback: bool = field(default=False)
