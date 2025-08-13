# Integrated pipeline

Once the baseline classifier and the initial LLM-based solution were complete, they were integrated, along with a static keyword checker, into a production pipeline.

## Static keyword checker

During development, it was observed that certain misclassifications could be mitigated by introducing a third component that checks prompts against a static dictionary of blocked keywords. For example, prompts containing the term "DAN" were sometimes long and linguistically complex, causing them to be misclassified by the TF-IDF-based classifier, and the LLM-based solution did not reliably recognize them as unsafe. Many of these cases could be addressed through alternative strategies, such as fine-tuning the LLM to better understand task-specific context. However, an added benefit of the static keyword checker is computational efficiency, enabling immediate detection and response.

## Analyzer base class

To standardize interaction across different pipeline components, including the static keyword checker, TF-IDF classifier, and LLM-based analysis component, a common interface called `Analyzer` was defined. This interface specifies an `analyze()` method, which returns a `SafetyReport`, if available. The implementations of the `Analyzer` base class and the `SafetyReport` data class are shown below.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


class Analyzer(ABC):
    """
    Abstract base class for prompt analyzers.
    """

    @abstractmethod
    def analyze(self, prompt: str) -> Optional[SafetyReport]:
        """
        Analyze the prompt and return a SafetyReport, if available.

        Args:
            prompt (str): The input text prompt to check.

        Returns:
            SafetyReport if available, otherwise None.
        """
        pass

    @property
    def component_name(self) -> str:
        """
        Name and identifier of the analyzer.
        """
        return self.__class__.__name__


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
        analyzer (list[str]): Names of the analysis components that contributed to the report.
    """

    label: int
    score: Optional[float]
    confidence: float
    explanation: str
    recommendation: str
    analyzer: list[str]
```

Each pipeline component was implemented by subclassing `Analyzer`, ensuring that all analysis components share a consistent, unified interface. This design simplified integration and provides a scalable foundation, making it straightforward to add new components to the pipeline in the future.

## Algorithm

When a input prompt is received, the following algorithm is used to generate a safety report:

1. Check the prompt against a static list of blocked keywords. If a match is found, return the keyword-based safety report immediately.

2. Run the prompt through both the TF-IDF classifier and the LLM analyzer.

3. If the LLM analyzer fails, fallback to the TF-IDF classifier’s report. This happens when the models output cannot be parsed into a `SafetyReport`.

4. If the TF-IDF classifier and LLM analyzer disagree on the safety classification, return the report that flags the prompt as unsafe. This approach prioritizes caution, as allowing an unsafe prompt to pass could have more serious consequences than mistakenly blocking a safe prompt.

5. If both the TF-IDF classifier and and LLM analyzer agree, generate a combined safety report. This is done by averaging the confidence score and using the recommendation and explanation from the LLM report as it is usually richer and more specific.

As a potential future improvement, prompts flagged as unsafe by the TF-IDF classifier could be passed through the same LLM with a different system prompt to obtain a continuous safety score, along with a more detailed explanation and recommended action.

This algorithm ensures that the LLM is invoked at most once per prompt, minimizing computational cost. Alternative approaches may improve classification accuracy by querying the LLM multiple times with varied inputs, albeit at a higher computational expense. A future enhancement could include a command-line option to allow users to balance execution time and report accuracy.

## System evaluation

The system was evaluated on the test set of the Safe-Guard Prompt Injection Dataset.

TODO: Add results!
