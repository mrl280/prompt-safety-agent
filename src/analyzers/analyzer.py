from abc import ABC, abstractmethod
from typing import Optional

from src.utils import SafetyReport


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
