import os
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
DATA_DIR = os.path.join(SRC_DIR.parent, "data")
MODEL_DIR = os.path.join(SRC_DIR.parent, "model")

if __name__ == "__main__":
    print(SRC_DIR)
    print(DATA_DIR)
    print(MODEL_DIR)
