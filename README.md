# Prompt Safety Agent

Classifying text prompts as safe or unsafe using a local LLM.

## 🚀 Getting started

The easiest way to use the Prompt Safety Agent is to pull the latest Docker image from Docker Hub:

```bash
docker pull mrl280/safety-agent:latest
```

Use the `check` command to generate a safety report:

```bash
TODO: Add usage example
```

Use `--help` to see the full list of available commands:

```bash
docker run --rm safety-agent --help
```

## 📚 Documentation web server

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

### Development container (recommended)

This project includes a VS Code **Development Container** configuration. Follow the instructions below to build and start the development container:

1; One of the models used in this project is Mistral-7B-Instruct-v0.3. To access this gated model, you need to visit Hugging Face and request access by sharing your contact information: [`Mistral-7B-Instruct-v0.3`](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3). If you prefer not to provide your contact information, just be aware this model won’t be included automatically in the development container.

2; Create a new user access token for this project. This is only necessary if you’ve provided your contact information to gain access to the `Mistral-7B-Instruct-v0.3` model. A token is not required to clone public models. For help creating a token, please refere to the Hugging Face Hub docs: [User access tokens](https://huggingface.co/docs/hub/en/security-tokens). Place your token in a `.env` file in the project root:

```bash
# .env
HUGGINGFACE_HUB_TOKEN=<your_token_here>
```

3; Open the project folder in VS Code and install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

4; Press `Ctrl+Shift+P` to open the command palette. Select **Dev Containers: Rebuild and Reopen in Container** from the command palette. Note that the first time you build and start the development container may take several minutes.

If you’re new to VS Code Dev Containers, refere to the following docs for help getting started: [Developing inside a Container](https://code.visualstudio.com/docs/remote/containers).

### Developing without the development container

You can also work on this project without using the development container. However, you’ll need to configure a few things manually. Follow the instructions below to get set up:

1; Create a Python virtual environment and install the required packages from `requirements_dev.txt`.

```bash
python -m venv .venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements_dev.txt
```

2; Install the recommended extensions listed in `.vscode/extensions.json`.

3; Clone project models from Hugging Face Hub:

```bash
RUN git clone https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507 ./models/Qwen3-4B-Instruct-2507
RUN git clone https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3 ./models/Mistral-7B-Instruct-v0.3
```
