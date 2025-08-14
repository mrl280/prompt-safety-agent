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

This algorithm ensures that the LLM is invoked at most once per prompt, minimizing computational cost. Alternative approaches may improve classification accuracy by querying the LLM multiple times with varied inputs, albeit at a higher computational expense. A future enhancement could include a command-line option to allow users to balance execution time and report accuracy.

## System evaluation

Two systems were evaluated based on the test subset of the Safe-Guard Prompt Injection Dataset. The evaluation combined the predictions from all three analyzers: if any of the three systems classified an example as unsafe, it was considered unsafe; only when all three systems classified an example as safe was it marked as safe. The system was tested using the LLM analyzer with both Mistral-7B-Instruct-v0.3 and Qwen3-4B-Instruct-2507.

Table 8 presents the performance metrics for the system using Mistral-7B-Instruct-v0.3, with Figure 12 showing the corresponding confusion matrix. Table 9 presents the performance metrics for Qwen3-4B-Instruct-2507, accompanied by its confusion matrix in Figure 13.

<p align="center"><strong>Table 8:</strong> Test Set Performance Metrics for System with Mistral-7B-Instruct-v0.3</p>

<table>
  <thead>
    <tr>
      <th>Class</th>
      <th>Precision</th>
      <th>Recall</th>
      <th>F1-Score</th>
      <th>Support</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Safe (0)</td>
      <td>1.00</td>
      <td>0.91</td>
      <td>0.95</td>
      <td>1410</td>
    </tr>
    <tr>
      <td>Unsafe (1)</td>
      <td>0.84</td>
      <td>1.00</td>
      <td>0.91</td>
      <td>650</td>
    </tr>
    <tr>
      <td>accuracy</td>
      <td></td>
      <td></td>
      <td>0.94</td>
      <td>2060</td>
    </tr>
    <tr>
      <td>macro avg</td>
      <td>0.92</td>
      <td>0.96</td>
      <td>0.93</td>
      <td>2060</td>
    </tr>
    <tr>
      <td>weighted avg</td>
      <td>0.95</td>
      <td>0.94</td>
      <td>0.94</td>
      <td>2060</td>
    </tr>
  </tbody>
</table>

{{ plot:conf_matrix_system_test_Mistral-7B-Instruct-v0.3.html }}

<p align="center"><strong>Figure 12:</strong> Test Set Confusion Matrix for System with Mistral-7B-Instruct-v0.3</p>

<br>

<p align="center"><strong>Table 9:</strong> Test Set Performance Metrics for System with Qwen3-4B-Instruct-2507</p>

<table>
  <thead>
    <tr>
      <th>Class</th>
      <th>Precision</th>
      <th>Recall</th>
      <th>F1-Score</th>
      <th>Support</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Safe (0)</td>
      <td>1.00</td>
      <td>0.98</td>
      <td>0.99</td>
      <td>1410</td>
    </tr>
    <tr>
      <td>Unsafe (1)</td>
      <td>0.96</td>
      <td>1.00</td>
      <td>0.98</td>
      <td>650</td>
    </tr>
    <tr>
      <td>accuracy</td>
      <td></td>
      <td></td>
      <td>0.98</td>
      <td>2060</td>
    </tr>
    <tr>
      <td>macro avg</td>
      <td>0.98</td>
      <td>0.99</td>
      <td>0.98</td>
      <td>2060</td>
    </tr>
    <tr>
      <td>weighted avg</td>
      <td>0.99</td>
      <td>0.98</td>
      <td>0.98</td>
      <td>2060</td>
    </tr>
  </tbody>
</table>

{{ plot:conf_matrix_system_test_Qwen3-4B-Instruct-2507.html }}

<p align="center"><strong>Figure 13:</strong> Test Set Confusion Matrix for System with Qwen3-4B-Instruct-2507</p>

As shown in Tables 8 and 9, the Mistral-based system achieved an overall accuracy of 94%, compared to 98% for the Qwen-based system. Both models attained near-perfect recall for unsafe prompts, with the confusion matrices showing that the Mistral system misclassifying 3 unsafe examples and the Qwen system misclassifying 2. Rather, the difference in performance lies in precision for the unsafe prompts: the Qwen-based system achieved 96%, while the Mistral-based system achieved 84%. The confusion matrices show that this difference corresponds to 120 false positives for the Mistral system versus only 30 for the Qwen system.

Based on these results, Qwen3-4B-Instruct-2507 was selected for deployment in the production system. Additionally, the Qwen-based system offers faster inference due to smaller model size, and this LLM is publicly available for use, eliminating the need to share contact information.
