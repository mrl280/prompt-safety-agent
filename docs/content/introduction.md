# Introduction

Large language models (LLMs) are advanced AI systems designed for natural language processing. These models are trained on large amounts of natural language data, enabling them to effectively process and generate natural language text. Users interact with LLMs by providing prompts that guide the model on what to generate next. For example, a question of instruction.

Like any emerging technology, LLMs are susceptible to misuse and malicious exploitation. In the case of LLMs, one of the most prominent risk vectors is unsafe prompts. Unsafe prompts can come from malicious actors deliberately producing inappropriate, offensive, or dangerous content, as well as from regular users who inadvertently submit inputs that lead to unintended harmful or biased outputs. As a result, prompt safety has become a focus of several recent studies [TODO: Add refs; https://arxiv.org/html/2402.13494v1].

In this project, a safety agent was developed to analyze LLM prompts for potential safety risks.

The following sections of this report are organized in alignment with project development activities:

- Dataset Exploration: The project dataset was analyzed to identify signals for class separation.
- TF-IDF Classifier: A simple baseline classifier was trained and evaluated on the problem of unsafe prompt detection.
- LLM-Based Solution: A local LLM-based solution was prototyped, complete with natural language explanations and recommendations.
- Pipeline Integration: The TF-IDF classifier, LLM agent, were integrated together into a unified product, which was then packaged as a Docker container.

Users can navigate the report by selecting tabs in the banner at the top of the page.
