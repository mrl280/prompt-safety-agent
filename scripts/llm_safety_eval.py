"""
Script to evaluate the LLM solution on a test dataset.

For more information, including usage instructions, see the README file in this directory.
"""

import argparse
import json
import os
import time
from dataclasses import asdict, dataclass
from typing import Optional, cast

import torch
from datasets import DatasetDict, load_dataset
from datasets.arrow_dataset import Column
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedTokenizerBase


@dataclass
class EvaluationResult:
    """
    Represents the results of a model evaluation.
    """

    y_true: list[int]
    y_pred: list[int]
    failed_indices: list[int]


@dataclass
class SafetyReport:
    """
    Represents a prompt safety report, to be built from model output.
    """

    score: float
    confidence: float
    explanation: str
    recommendation: str


def prepare_inputs_for_model(
    model_path: str, device: torch.device, tokenizer: PreTrainedTokenizerBase, prompt: str, system_prompt: str
) -> tuple[dict[str, torch.Tensor], int]:
    """
    Prepare tokenized inputs based on model family.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    if "mistral" in model_path.lower():
        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}
        input_length = inputs["input_ids"].shape[-1]

    elif "qwen" in model_path.lower():
        chat_text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = tokenizer([chat_text], return_tensors="pt").to(device)
        input_length = inputs.input_ids.shape[-1]

    else:
        raise ValueError(f"Model family not supported: {model_path}")

    return inputs, input_length


def parse_safety_report(json_str: str) -> Optional[SafetyReport]:
    """
    Parse a JSON string into a SafetyReport object, returning None if JSON is invalid.
    """
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return None

    # Validate required keys and types
    required_fields = {
        "score": (float, int),
        "confidence": (float, int),
        "explanation": str,
        "recommendation": str,
    }

    for field, expected_types in required_fields.items():
        if field not in data:
            return None
        if not isinstance(data[field], expected_types):
            return None

    score = float(data["score"])
    confidence = float(data["confidence"])

    if not (0.0 <= score <= 1.0) or not (0.0 <= confidence <= 1.0):
        return None

    return SafetyReport(
        score=score,
        confidence=confidence,
        explanation=data["explanation"],
        recommendation=data["recommendation"],
    )


def evaluate_model(
    X: Column,
    y: Column,
    model_path: str,
    system_prompt: str,
) -> EvaluationResult:
    """
    Evaluate the specified model on the provided data.
    """
    y_true, y_pred = [], []
    failed_indices = []

    model = AutoModelForCausalLM.from_pretrained(
        model_path, local_files_only=True, torch_dtype="auto", device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)

    assert len(X) == len(y)
    n_examples = len(X)
    print(f"Total number of elements in the test dataset: {n_examples}")

    start_time = time.time()

    for i, (text, true_label) in enumerate(zip(X, y)):
        if i % 10 == 0:
            elapsed = time.time() - start_time
            print(f"\rProcessing example {i + 1} out of {n_examples} — elapsed {elapsed: .1f}s", end="", flush=True)

        inputs, input_length = prepare_inputs_for_model(
            model_path=model_path, device=model.device, tokenizer=tokenizer, prompt=text, system_prompt=system_prompt
        )

        # Generate response
        with torch.no_grad():
            generated_ids = model.generate(**inputs, max_new_tokens=256)

        # Trim the prompt part from the output and remove input tokens
        generated_ids_trimmed = generated_ids[:, input_length:]

        model_output = tokenizer.decode(generated_ids_trimmed[0], skip_special_tokens=True).strip()
        report = parse_safety_report(json_str=model_output)

        if report is None:
            failed_indices.append(i)
            continue

        if report.score > 0.5:
            predicted_label = 1
        else:
            predicted_label = 0

        y_true.append(true_label)
        y_pred.append(predicted_label)

    return EvaluationResult(y_true, y_pred, failed_indices)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate LLM-based prompt analyzer on test dataset")
    parser.add_argument(
        "--model-dir",
        type=str,
        required=True,
        help="Local directory path of the model to load and evaluate",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Directory to save evaluation results",
    )
    parser.add_argument(
        "--system-prompt-path",
        type=str,
        required=True,
        help="Path to system prompt text file",
    )
    args = parser.parse_args()

    model_path = os.path.abspath(args.model_dir)
    print(f"Evaluating model at: {model_path}")

    # Load system prompt text
    if not os.path.isfile(args.system_prompt_path):
        raise FileNotFoundError(f"System prompt file not found: {args.system_prompt_path}")
    with open(args.system_prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # Make sure output directory exists
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    # Check to ensure CUDA is available.
    cuda = torch.cuda.is_available()
    if cuda:
        print("CUDA device count:", torch.cuda.device_count())
        print("Current CUDA device:", torch.cuda.current_device())
        print("CUDA device name:", torch.cuda.get_device_name(torch.cuda.current_device()))
    else:
        raise RuntimeError("CUDA is not available")

    # Load synthetic prompt injection dataset.
    dataset_id = "xTRam1/safe-guard-prompt-injection"
    dataset = cast(DatasetDict, load_dataset(dataset_id))
    X_test, y_test = cast(Column, dataset["test"]["text"]), cast(Column, dataset["test"]["label"])

    result = evaluate_model(X=X_test, y=y_test, model_path=model_path, system_prompt=system_prompt)

    model_name = model_path.split("/")[-1]
    output_filepath = os.path.join(output_dir, f"llm_safety_eval_{model_name}.json")

    print(f"\nSaving evaluation results to: {output_filepath}")
    with open(output_filepath, "w") as f:
        json.dump(asdict(result), f, indent=4)
