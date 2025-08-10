from typing import Optional

from ops import KeywordChecker, LLMPromptClassifier, TfidfClassifier
from src.utils.reports import SafetyReport


class SafetyPipeline:
    def __init__(self):
        self.keyword_checker = KeywordChecker()
        self.prompt_classifier = TfidfClassifier()
        self.llm_classifier = LLMPromptClassifier()

    def run(self, prompt: str) -> Optional[SafetyReport]:
        """
        Runs the prompt through the safety pipeline operators in order:

        TODO: Optimize and articulate algorithm
        """

        # First, let's check against the list of blocked keywords
        keyword_report = self.keyword_checker.check(prompt)
        if keyword_report is not None:
            return keyword_report

        # Next, let's run it through both the TF-IDF + Logistic Regression as well as the LLM
        tfidf_prediction = self.prompt_classifier.predict_prompt_with_confidence(prompt)
        llm_report = self.llm_classifier.classify_prompt(prompt)

        if llm_report is None:
            # Something went wrong with the LLM, fallback to TF-IDF prediction if confidence is high enough
            if tfidf_prediction.confidence > 0.85:
                if tfidf_prediction.label == 1:
                    tfidf_explanation = "Words in the prompt indicate risk based on statistical analysis."
                    tfidf_recommendation = "Block this prompt and flag for review."
                else:
                    tfidf_explanation = "No strong risk signals detected by statistical analysis."
                    tfidf_recommendation = "Allow this prompt."

                return SafetyReport(
                    label=tfidf_prediction.label,
                    score=tfidf_prediction.label,
                    confidence=tfidf_prediction.confidence,
                    explanation=tfidf_explanation,
                    recommendation=tfidf_recommendation,
                )
            else:
                # TODO: Implement fallback
                return None

        if (
            llm_report.label == tfidf_prediction.label
            and llm_report.confidence > 0.7
            and tfidf_prediction.confidence > 0.7
        ):
            # LLM and TF-IDF agree and both are confident
            return llm_report

        # TODO: Implement fallback
        return None
