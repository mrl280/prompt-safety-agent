from src.analyzers import KeywordChecker, QwenAnalyzer, TfidfClassifier
from src.utils import SafetyReport


def analyze(prompt: str) -> SafetyReport:
    """
    Analyze the given prompt using a multi-stage safety pipeline.

    Algorithm:
    1. Check the prompt against a static list of blocked keywords. If matched, return the keyword-based safety
        report immediately.
    2. Run the prompt through both the TF-IDF + Logistic Regression classifier and the LLM analyzer.
    3. If the LLM analyzer fails, fallback to the TF-IDF classifier's report.
    4. If the TF-IDF + Logistic Regression classifier and the LLM analyzer disagree on safety: For caution,
        return the report that flags the prompt as unsafe.
    5. If both the TF-IDF + Logistic Regression classifier and the LLM analyzer agree, generate a combined report.

    Args:
        prompt (str): The input prompt text to evaluate.

    Returns:
        SafetyReport: The safety assessment of the prompt.
    """

    # First, let's check against the list of blocked keywords
    kw_checker = KeywordChecker()
    keyword_report = kw_checker.analyze(prompt=prompt)
    if keyword_report is not None:
        return keyword_report

    # Next, let's run it through both the TF-IDF model and the LLM
    tfidf_classifier = TfidfClassifier()
    tfidf_report = tfidf_classifier.analyze(prompt=prompt)

    llm_classifier = QwenAnalyzer()
    llm_report = llm_classifier.analyze(prompt=prompt)

    if llm_report is None:
        # Something went wrong with the LLM report, fallback to TF-IDF report
        # TODO: It may be helpful to feed prompts that the TF-IDF model thinks are unsafe back through another
        #  LLM to get a decimal score as well as a more specific explanation and recommendation
        tfidf_report.analyzer.append(kw_checker.component_name)
        return tfidf_report

    if llm_report.label != tfidf_report.label:
        # If the LLM and TF-IDF model disagree then, to be cautious, report the prediction that flags the prompt
        #  as unsafe
        if llm_report.label:
            return llm_report
        else:
            # TODO: It may be helpful to feed prompts that the TF-IDF model thinks are unsafe back through another
            #  LLM to get a decimal score as well as a more specific explanation and recommendation
            return tfidf_report

    # Finally, if both the TF-IDF model and the LLM agree, generate a combined report. We average their confidence
    #  scores, but use the explanation and recommendation from the LLM since it’s usually richer and more specific.
    return SafetyReport(
        label=llm_report.label,
        score=llm_report.score,
        confidence=round((llm_report.confidence + tfidf_report.confidence) / 2, 2),
        explanation=llm_report.explanation,
        recommendation=llm_report.recommendation,
        analyzer=[llm_classifier.component_name, tfidf_classifier.component_name],
    )
