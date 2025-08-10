import json
import os
import re
from typing import Optional

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from app.classifiers import Classifier
from app.utils import SafetyReport
from app.utils.paths import PROMPTS_DIR


class LLMPromptClassifier(Classifier):
    """
    Uses a local LLM to generate prompt safety reports.
    """

    _prompt_filepath = os.path.join(PROMPTS_DIR, "blocked_keywords.txt")
    _model_filepath = os.path.join("/opt", "models", "Qwen3-4B-Instruct-2507")

    def __init__(self):
        print(f"Loading model {os.path.basename(self._model_filepath)} and tokenizer...")
        self._model = AutoModelForCausalLM.from_pretrained(self._model_filepath, torch_dtype="auto", device_map="auto")
        self._tokenizer = AutoTokenizer.from_pretrained(self._model_filepath)

        # Read system prompt text from file
        with open(self._prompt_filepath, "r", encoding="utf-8") as f:
            self._system_prompt = f.read()

    def report(self, prompt: str) -> Optional[SafetyReport]:
        """
        Classify a prompt using the local LLM, returning a SafetyReport if possible.

        Args:
            prompt (str): The input prompt to classify.

        Returns:
            SafetyReport if parsing succeeds; otherwise None.
        """
        messages = [{"role": "system", "content": self._system_prompt}, {"role": "user", "content": prompt}]

        # Format chat for Qwen
        chat_text = self._tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self._tokenizer([chat_text], return_tensors="pt").to(self._model.device)

        with torch.no_grad():
            generated_ids = self._model.generate(**inputs, max_new_tokens=256)

        # Remove input prompt tokens from the generated output
        generated_ids = [
            output_ids[len(input_ids) :] for input_ids, output_ids in zip(inputs.input_ids, generated_ids)
        ]

        # Decode the generated response
        response_text = self._tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

        # Parse the model's response into SafetyReport
        return parse_safety_report(response_text)


def parse_safety_report(response_text: str) -> Optional[SafetyReport]:
    """
    Parse the JSON portion of an LLM response string into a SafetyReport object.

    Args:
        response_text (str): The raw text response from the LLM, expected to contain a JSON object with safety
          evaluation data.

    Returns:
        SafetyReport or None: The parsed safety report object, or None if parsing the JSON fails, required fields
         are missing, or values are out of allowed ranges.
    """
    # Regex to find the first {...} JSON object in the text
    json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if not json_match:
        print("No JSON object found in response.")
        return None

    json_str = json_match.group(0)
    try:
        response_dict = json.loads(json_str)

        required_keys = {"score", "confidence", "explanation", "recommendation"}
        if not required_keys.issubset(response_dict):
            print(f"Missing keys in response JSON: {required_keys - response_dict.keys()}")
            return None

        score = float(response_dict["score"])
        confidence = float(response_dict["confidence"])
        explanation = response_dict["explanation"]
        recommendation = response_dict["recommendation"]

        if not (0.0 <= score <= 1.0):
            print(f"Invalid score value: {score}")
            return None

        if not (0.0 <= confidence <= 1.0):
            print(f"Invalid confidence value: {confidence}")
            return None

        if not (isinstance(explanation, str) and explanation.strip()):
            print("Explanation is missing or not a non-empty string.")
            return None

        if not (isinstance(recommendation, str) and recommendation.strip()):
            print("Recommendation is missing or not a non-empty string.")
            return None

        if score > 0.5:
            label = 1
        else:
            label = 0

        return SafetyReport(
            label=label,
            score=score,
            confidence=confidence,
            explanation=explanation,
            recommendation=recommendation,
            classifier="LLMPromptClassifier",
        )
    except (json.JSONDecodeError, TypeError, KeyError) as e:
        print(f"Error parsing JSON: {e}")
        return None
