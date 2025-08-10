import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = os.path.join(APP_DIR.parent, "data")
MODELS_DIR = os.path.join(APP_DIR.parent, "models")
PROMPTS_DIR = os.path.join(APP_DIR.parent, "prompts")
REPORT_DIR = os.path.join(APP_DIR.parent, "reports")
