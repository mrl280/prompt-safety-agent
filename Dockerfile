FROM python:3.12-slim AS production

ARG USERNAME=agent
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create non-root user (no sudo)
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Install additional system dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends git git-lfs \
    && git lfs install \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python packages
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt


# Copy local prompt, model, and data files to /app directory
RUN mkdir -p /app/models /app/prompts /app/data /app/docs
COPY models /app/models
COPY prompts /app/prompts
COPY data /app/data
COPY docs /app/docs

# Clone the Qwen3-4B-Instruct-2507 model from Hugging Face into /app/models, if it doesn't already exist
RUN [ ! -d /app/models/Qwen3-4B-Instruct-2507 ] && \
    git clone https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507 /app/models/Qwen3-4B-Instruct-2507 || \
    echo "Model Qwen3-4B-Instruct-2507 already exists, skipping clone"

# Pull the large files from LFS
RUN cd /app/models/Qwen3-4B-Instruct-2507 && git lfs pull

# Copy your source code into /app
COPY src/ /app/src/

# Change ownership so non-root user can access files
RUN chown -R $USERNAME:$USERNAME /app

# Switch to non-root user
USER $USERNAME

# Set default command to your CLI script entry point, passing command line argument(s)
ENTRYPOINT ["python", "-m", "src.cli"]
CMD []
