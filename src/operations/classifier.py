import os

import joblib
from sklearn.pipeline import Pipeline

from src import MODELS_DIR
from src.utils.reports import ClassifierPredictionResult


class PromptClassifier:
    """
    Loads a trained TF-IDF + Logistic Regression classification model and predicts safety labels and confidence for prompts.
    """

    _model_filepath = os.path.join(MODELS_DIR, "classifier.joblib")

    def __init__(self, model_path: str):
        self._model: Pipeline = joblib.load(model_path)

    def predict_prompt_with_confidence(self, prompt: str) -> ClassifierPredictionResult:
        """
        Predict the label and confidence score for a single input prompt.

        Args:
            prompt (str): The input text prompt to classify.

        Returns:
            A ClassifierPredictionResult with the predicted label and the confidence score.
        """
        probas = self._model.predict_proba([prompt])[0]
        label = int(self._model.predict([prompt])[0])
        confidence = float(probas[label])

        return ClassifierPredictionResult(label=label, confidence=confidence)
