# Conclusion

In this project, machine learning was applied to the problem of unsafe prompt detection. The final system consists of three analysis components: A static keyword checker, a TD-IDF-based classifier, and an LLM-based analysis component. The dataset used in this project was the Safe-Guard Prompt Injection Dataset, accessed from Hugging Face Hub: [`xTRam1/safe-guard-prompt-injection`](https://huggingface.co/datasets/xTRam1/safe-guard-prompt-injection). All performance metrics reported in this conclusion were evaluated on the test subset of the dataset.

The static keyword checker examines each input against a predefined list of keywords known to be unsafe. For example, keyword such as "DAN", "Developer Mode", and "ChatGPT jailbreak" are included in this list. This is a simple and effective check, but it has meaningful limitations. For example, prompts innocently asking what "DAN" stands for will be incorrectly flagged as unsafe and sent for review.

Based on dataset exploration, \( n \)-grams, particularly unigrams, provide a strong signal for classifying unsafe prompts. Leveraging this insight, a logistic regression model was trained on TF-IDF vectorized representations of the training prompts. The tuned classifier achieves an overall accuracy of 99.3%, with 98.8% precision and 99.1% recall for unsafe prompts. The predicted class probabilities are used as confidence measures, and the distribution of prediction confidences indicates that misclassifications tend to occur at lower confidence levels. The classifier sometimes struggles with prompts in which unsafe indicators make up only a small fraction of the text. For example, very long and linguistically rich prompts, wherein unsafe signals are diluted.

The final classification component developed was an LLM-based prompt analyzer, built on a pre-trained, instruction-tuned LLM. Two candidate models were evaluated with a custom system prompt: [mistralai/Mistral-7B-Instruct-v0.3](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) and [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507). Neither system performed particularly well, indicating that further work is required to improve this components performance. Mistral-7B-Instruct-v0.3 achieved 90% classification accuracy, while Qwen3-4B-Instruct-2507 achieved 92%. Although Mistral-7B-Instruct-v0.3 had higher recall (85% versus 77% for Qwen3-4B-Instruct-2507), it failed to produce the the proper output schema on 109 instances (5.3%) compared to 7 for Qwen3-4B-Instruct-2507 (0.3%). These results suggest that the LLM would benefit from additional domain-specific context or fine-tuning to improve performance.

Integrated together, the Qwen-based system achieved 98.5% accuracy, with 95.7% precision and 99.7% recall for unsafe prompts, demonstrating that the combined pipeline outperforms the individual components. The high recall is critical for safety applications because it minimizes misclassified positives (unsafe prompts misclassified as safe). Future work should aim to increase the precision for unsafe prompts while maintaining the high recall necessary for safety-critical applications.

The final system was packaged as a Docker container and made available on Docker Hub.

## Key learnings

This project was a rewarding opportunity to explore an exciting application of LLMs. Additionally, it provided the chance to work with several new tools and technologies:

- This project was my first time configuring a VS Code development container; previously, I had only worked in preconfigured development containers.

- The project documentation is my first Flask application, and my first time configuring djLint.

- This was my first time experimenting with the newly released Qwen3-4B-Instruct-2507 model.

## Future work

- Further work is needed to improve the performance of the LLM-based component. Recommended next steps, in order of priority, include incorporating retrieval-augmented generation (RAG) to provide relevant context at inference, and fine-tuning the model on task-specific data.

- Prompts flagged as unsafe by the TF-IDF classifier should be passed through the same LLM with a different system prompt to obtain a continuous safety score, along with a more detailed explanation and recommended action.

- Several data insights have not yet been exploited. For example, checks based on Shannon entropy could be incorporated to improve detection confidence. Additionally, confidence scores are currently generated only for inclusion in system output, but they could be leveraged within the algorithm to enable more nuanced decision-making.

- Introduce an option to query the LLM multiple times per prompt, allowing users a trade off between improved classification accuracy and increased computational cost.

- Explore and implement novel approaches to prompt safety analysis, such as gradient-based detection methods (e.g., [GradSafe](https://arxiv.org/abs/2402.13494)) or feature- and response-based classification approaches (e.g., [Adversarial Prompt Detection](https://www.sciencedirect.com/org/science/article/pii/S1546221825004898)).

- Add automated testing.
