# Prompt Safety Agent

Classifying text prompts as safe or unsafe using a local LLM

## 🚀 Getting started

The easiest way to use the Prompt Safety Agent is to pull the latest Docker image from Docker Hub:

```bash
docker pull mrl280/safety-agent:latest
```

Run the following command to see available commands and options:

```bash
docker run --rm safety-agent --help
```

### Generate prompt safety report

Use the following command to generate a safety report for a prompt.

TODO: Add usage example

### Documentation web server

Use the following command to start the documentation server:

```bash
docker run --rm -p 8000:8000 safety-agent docs
```

Once the web server starts, you can view the project documentation in your browser at: `http://<host>:<port>` where `<host>` and `<port>` are set via the CLI options `--host` and `--port` respectively (defaulting to `0.0.0.0` and `8000` if not specified).

**Note:** The `-p` option maps the container’s internal port to a port on the host machine. If you want to serve the docs on a different host port, you can change this mapping. For example, using `-p 8001:8000` will expose the container’s port `8000` on host port `8001`.

## 🐳 Build the container locally

To build the container locally (for example, after making changes), run `docker build` from the project root:

```bash
docker build -t safety-agent:latest .
```

This will create a local image tagged `safety-agent:latest`.

Use the following command to get an interactive shell inside the container. This can be helpful for inspecting the container’s contents and verifying that everything is set up as expected:

```bash
docker run -it --rm --entrypoint /bin/bash safety-agent:latest
```

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
