import os

import joblib
from sklearn.pipeline import Pipeline

from src.classifiers import Classifier
from src.utils import SafetyReport
from src.utils.paths import MODELS_DIR


class TfidfClassifier(Classifier):
    """
    Uses a TF-IDF + Logistic Regression classification model to generate safety reports.
    """

    _model_filepath = os.path.join(MODELS_DIR, "tdidf_classifier.joblib")

    def __init__(self):
        self._model: Pipeline = joblib.load(self._model_filepath)

    def analyze(self, prompt: str) -> SafetyReport:
        """
        Classify prompt using TF-IDF + Logistic Regression classification model.

        Predict the label and confidence score for a single input prompt.

        Args:
            prompt (str): The input text prompt to classify.

        Returns:
           SafetyReport
        """
        probas = self._model.predict_proba([prompt])[0]
        label = int(self._model.predict([prompt])[0])
        confidence = float(probas[label])

        if label == 1:
            explanation = "Words in the prompt indicate risk based on statistical analysis."
            recommendation = "Block this prompt and flag for review."
        else:
            explanation = "No strong risk signals detected by statistical analysis."
            recommendation = "Allow this prompt."

        return SafetyReport(
            label=label,
            score=None,
            confidence=confidence,
            explanation=explanation,
            recommendation=recommendation,
            classifier=self.get_class_name(),
        )
