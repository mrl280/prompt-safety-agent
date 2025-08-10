FROM python:3.12-slim AS dev_containers_target_stage

# Create user
ARG USERNAME=agent
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && chown -R $USERNAME /home/$USERNAME

# Install additional system dependencies
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends  \
    git \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries
COPY ../requirements_dev.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements_dev.txt && \
    rm requirements_dev.txt

# Clone the Qwen3-4B-Instruct-2507 model from Hugging Face into /opt/models folder
RUN mkdir -p /opt/models && \
    git clone https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507 /opt/models/Qwen3-4B-Instruct-2507

# Create working directory and models subdirectory
ARG WORKSPACE_DIR=/workspace
RUN mkdir -p $WORKSPACE_DIR && chown agent:agent $WORKSPACE_DIR
WORKDIR $WORKSPACE_DIR

# Switch to non-root user
USER $USERNAME
