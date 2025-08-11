#!/usr/bin/env bash
set -e

echo "Running initialize-command.sh..."

# Load environment variables from .env file
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
else
    echo ".env file not found. Please create one containing HUGGINGFACE_HUB_TOKEN=... This is required to download gated models."
    exit 1
fi

# Define project models
declare -A MODELS=(
    ["Qwen3-4B-Instruct-2507"]="https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507"
    ["Mistral-7B-Instruct-v0.3"]="https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3"
)

# Define target directory
project_dir="$(pwd)"
models_dir="$project_dir/models"

# Clone project models, only if they doesn't already exist
for model_name in "${!MODELS[@]}"; do
    repo_url="${MODELS[$model_name]}"
    model_dir="$models_dir/$model_name"

    if [ ! -d "$model_dir" ]; then
        echo "Cloning $model_name model into $model_dir..."

        if [[ "$repo_url" == *"huggingface.co"* && -n "$HUGGINGFACE_HUB_TOKEN" ]]; then
            # Use token auth if token is set and repo is on huggingface.co
            git clone "https://user:$HUGGINGFACE_HUB_TOKEN@${repo_url#https://}" "$model_dir"
        else
            git clone "$repo_url" "$model_dir"
        fi

        if [ $? -ne 0 ]; then
            echo "Warning: Failed to clone $model_name from $repo_url, skipping download."
            continue
        fi
    else
        echo "Model $model_name already exists at $model_dir, skipping clone."
    fi
done
