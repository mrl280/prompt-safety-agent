from abc import ABC, abstractmethod
from typing import Optional

from src.utils import SafetyReport


class Classifier(ABC):
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

    def get_class_name(self) -> str:
        """
        Return the analyzer name as a string.
        """
        return self.__class__.__name__
