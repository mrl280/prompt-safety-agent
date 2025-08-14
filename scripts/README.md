# Scripts

This directory contains project scripts. This README file contains information on how to run the scripts located in this directory.

## LLM safety evaluation script

The LLM safety evaluation script, `llm_safety_eval.py` is used to evaluate the LLM solution on a test dataset.

This script loads the test dataset, runs the LLM safety analyzer on each sample, and saves the evaluation results to file. The saved results include lists of true and predicted indices, as well as a list of indices where model parsing failed.

With sufficient compute resources, this test could be handled gracefully within one of the exploratory notebooks. However, due to the long-running nature of the process, we have extracted the necessary utilities from `llm_agent.ipynb` to run this script independently inside a `tmux` session.

### Usage

1. Create a Python virtual environment and install the required packages from `requirements_dev.txt`:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements_dev.txt
```

2. Start a new tmux session:

```bash
tmux new -s llm_eval
```

3. Activate the previously created virtual environment inside the tmux session:

```bash
source .venv/bin/activate
```

4. Run the script in from the project root directory:

```bash
python -m scripts.llm_safety_eval \
    --model-dir ./models/Qwen3-4B-Instruct-2507 \
    --output-dir ./data \
    --system-prompt-path ./prompts/safety_check.txt
```

OR

```bash
python -m scripts.llm_safety_eval \
    --model-dir ./models/Mistral-7B-Instruct-v0.3 \
    --output-dir ./data \
    --system-prompt-path ./prompts/safety_check.txt
```

To detach from the session: `Ctrl + b`, then `d`. To attach to an existing session:

```bash
tmux attach -t <session_name>
```

**Note:** You can list all active tmux sessions by running: `tmux ls`.
