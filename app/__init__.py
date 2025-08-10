import os
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
DATA_DIR = os.path.join(SRC_DIR.parent, "data")
MODELS_DIR = os.path.join(SRC_DIR.parent, "models")
PROMPTS_DIR = os.path.join(SRC_DIR.parent, "prompts")
REPORT_DIR = os.path.join(SRC_DIR.parent, "prompts")
