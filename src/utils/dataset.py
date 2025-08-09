from typing import cast

from datasets import DatasetDict, load_dataset


def get_project_dataset() -> DatasetDict:
    """
    Load the synthetic prompt injection detection dataset from Hugging Face.

    Returns:
        DatasetDict: A Hugging Face dataset dictionary
    """
    return cast(DatasetDict, load_dataset("xTRam1/safe-guard-prompt-injection"))
