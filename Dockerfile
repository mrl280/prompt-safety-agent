FROM python:3.12-slim AS production

ARG USERNAME=agent
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create non-root user (no sudo)
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Install additional system dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends git \
    && apt-get autoremove -y && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python packages
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

# Clone the Qwen3-4B-Instruct-2507 model from Hugging Face into /opt/models folder
RUN mkdir -p /opt/models && \
    git clone https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507 /opt/models/Qwen3-4B-Instruct-2507

# Copy your source code into /app
COPY app/ ./

# Change ownership so non-root user can access files
RUN chown -R $USERNAME:$USERNAME /app /opt/models

# Switch to non-root user
USER $USERNAME

# Set default command to your CLI script entry point, passing command line argument(s)
ENTRYPOINT ["python", "cli.py"]
CMD []
