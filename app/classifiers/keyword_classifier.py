import os
import re
from typing import Optional

from app import DATA_DIR
from app.classifiers import Classifier
from app.utils import SafetyReport


class StaticKeywordChecker(Classifier):
    """
    Checks input prompts against a list of blocked keywords.
    """

    _keywords_filepath = os.path.join(DATA_DIR, "blocked_keywords.txt")

    def __init__(self):
        with open(self._keywords_filepath, "r", encoding="utf-8") as f:
            self._keywords = [line.strip() for line in f if line.strip()]

        self._pattern = re.compile(
            r"\b(" + "|".join(re.escape(word) for word in self._keywords) + r")\b",
            flags=re.IGNORECASE,
        )

    def report(self, prompt: str) -> Optional[SafetyReport]:
        """
        Check if the prompt contains any blocked keywords.

        Args:
            prompt (str): The input text prompt to check.

        Returns:
            SafetyReport if a blocked keyword is found; otherwise, None.
        """
        match = self._pattern.search(prompt)
        if match:
            matched_word = match.group(0)
            return SafetyReport(
                label=1,
                score=1.0,
                confidence=1.0,
                explanation=f'Word "{matched_word}" in prompt is in list of blocked keywords.',
                recommendation="Block this prompt and flag for review.",
                classifier="StaticKeywordChecker",
            )
        return None
