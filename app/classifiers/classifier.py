from abc import ABC, abstractmethod
from typing import Optional

from app.utils import SafetyReport


class Classifier(ABC):
    """
    Abstract base class for prompt classifiers.
    """

    @abstractmethod
    def report(self, prompt: str) -> Optional[SafetyReport]:
        """
        Evaluate the prompt and return a SafetyReport, if available.

        Args:
            prompt (str): The input text prompt to check.

        Returns:
            SafetyReport if available, otherwise None.
        """
        pass
