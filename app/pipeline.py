from classifiers import LLMPromptClassifier, StaticKeywordChecker, TfidfClassifier

from app.utils import SafetyReport


class SafetyPipeline:
    def __init__(self):
        self._keyword_checker = StaticKeywordChecker()
        self._tfidf_classifier = TfidfClassifier()
        self._llm_classifier = LLMPromptClassifier()

    def run(self, prompt: str) -> SafetyReport:
        """
        Runs the given prompt through a multi-stage safety pipeline.

        Algorithm:
        1. Check the prompt against a static list of blocked keywords. If matched, return the keyword-based safety
         report immediately.
        2. Run the prompt through both the TF-IDF + Logistic Regression classifier and the LLM classifier.
        3. If the LLM classifier fails, fallback to the TF-IDF classifier's report.
        4. If the classifiers disagree on safety:
        - For caution, return the report that flags the prompt as unsafe.
        5. If both classifiers agree, return the LLM report for its richer explanation and scoring.

        Args:
            prompt (str): The input prompt text to evaluate.

        Returns:
            SafetyReport: The safety assessment of the prompt.
        """

        # First, let's check against the list of blocked keywords
        keyword_report = self._keyword_checker.report(prompt=prompt)
        if keyword_report is not None:
            return keyword_report

        # Next, let's run it through both the TF-IDF model and the LLM
        tfidf_report = self._tfidf_classifier.report(prompt=prompt)
        llm_report = self._llm_classifier.report(prompt=prompt)

        if llm_report is None:
            # Something went wrong with the LLM report, fallback to TF-IDF report
            # TODO: It may be helpful to feed prompts that the TF-IDF model thinks are unsafe back through another
            #  LLM to get a decimal score as well as a more specific explanation and recommendation
            return tfidf_report

        if llm_report.label != tfidf_report.label:
            # If the LLM and TF-IDF model disagree, to be cautious, report the prediction that flags the prompt as
            #  unsafe
            if llm_report.label:
                return llm_report
            else:
                # TODO: It may be helpful to feed prompts that the TF-IDF model thinks are unsafe back through another
                #  LLM to get a decimal score as well as a more specific explanation and recommendation
                return tfidf_report

        # Finally, if both the TF-IDF model and the LLM are in agreement, return the LLM report, it is is generally
        #  more usful due to the score, richer explanation, and recommendation
        return llm_report
