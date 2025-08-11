import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = os.path.join(APP_DIR, "data")
DATA_DIR = os.path.join(APP_DIR, "data")
MODELS_DIR = os.path.join(APP_DIR, "models")
PROMPTS_DIR = os.path.join(APP_DIR, "prompts")
REPORT_DIR = os.path.join(APP_DIR, "reports")
DOCS_DIR = os.path.join(APP_DIR, "docs")
