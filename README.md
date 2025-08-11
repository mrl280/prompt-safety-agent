# Prompt Safety Agent

Classifying text prompts as safe or unsafe using a local LLM

## 🚀 Getting started

The easiest way to use the Prompt Safety Agent is to pull the latest Docker image from Docker Hub:

```bash
docker pull mrl280/safety-agent:latest
```

## 🐳 Build the container locally

To build the container locally (for example, after making changes), run `docker build` from the project root:

```bash
docker build -t safety-agent:latest .
```

Use the following command to get an interactive shell inside the container. This can be helpful for inspecting the container’s contents and verifying that everything is set up as expected:

```bash
docker run -it --rm --entrypoint /bin/bash safety-agent:latest
```

This will create a local image tagged `safety-agent:latest`.

## 🛠️ Development environment

### Development container

This project includes a VS Code **Development Container** configuration. To build and start the dev container, simply open the project folder in VS Code and select **Reopen in Container** from the command palette. Note that developing inside a container requires the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

If you’re new to VS Code Dev Containers, refere to the following docs for more details: [Developing inside a Container](https://code.visualstudio.com/docs/remote/containers).

### Developing without the development container

You can also work on this project without the development container, but you will need to:

1; Manually set up a Python virtual environment and install the required packages from `requirements_dev.txt`.

```bash
python -m venv .venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements_dev.txt
```

2; Install the recommended extensions listed in `.vscode/extensions.json`

3; Install required model weights from Hugging Face Hub.
