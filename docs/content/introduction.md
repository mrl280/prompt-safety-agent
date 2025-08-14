# Introduction

Large language models (LLMs) are advanced AI systems designed for natural language processing. These models are trained on large amounts of natural language data, enabling them to effectively process and generate natural language text. Users interact with LLMs by providing prompts that specify the desired content, structure, or style of the model’s subsequent output. For example, prompts may instruct the model to answer a question, generate a story, summarize a document, translate text, write code, or perform other language-based tasks.

Like any emerging technology, LLMs are susceptible to misuse and malicious exploitation. One avenue for misuse is through unsafe or malicious prompts, which can cause LLMs to generate harmful, biased, inappropriate, or misleading outputs. As a result, prompt safety has become a focus of several recent studies.

Using a combination of statistical text analysis (TF-IDF) and large language models (LLMs), a safety agent was developed to analyze LLM prompts for potential safety risks. The body of this report is organized to reflect the project development activities:

- Dataset Exploration: The project dataset was analyzed to identify signals for class separation.
- TF-IDF Classifier: A simple baseline classifier was trained and evaluated on the problem of unsafe prompt detection.
- LLM-Based Classifier: A local LLM-based solution was prototyped.
- Pipeline Integration: The TF-IDF classifier and LLM agent were integrated together into a unified solution.

Finally, the key learnings and next steps from the project are summarized in the conclusion.

Users can navigate this report by selecting tabs in the banner at the top of the page. Additional information on system usage is available in the project README.
