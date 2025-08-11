FROM python:3.12-slim AS dev_containers_target_stage

ARG USERNAME=agent
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && chown -R $USERNAME /home/$USERNAME

# Install additional system dependencies, including Google Chrome, which is required to export Plotly figures
RUN apt-get update && DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends wget gnupg2 git git-lfs \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY ../requirements_dev.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements_dev.txt && \
    rm requirements_dev.txt

# Create working directory
ARG WORKSPACE_DIR=/app
RUN mkdir -p $WORKSPACE_DIR && chown agent:agent $WORKSPACE_DIR
WORKDIR $WORKSPACE_DIR

# Switch to non-root user
USER $USERNAME
