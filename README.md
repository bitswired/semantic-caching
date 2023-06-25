# Semantic Caching Evaluation 🚀
Explore semantic caching to reduce your OpenAI/LLM API bill


This repository contains a Python application that demonstrates the use of semantic caching in searching for similar questions in a cache. It compares the performance of two different embedding methods: OpenAI and ONNX.

## Features 🌟

- Streamlit web application to test and evaluate semantic caching.
- CLI for testing exact, semantic, and no cache.
- ONNX and OpenAI embeddings.
- FAISS search for fast similarity search.

## Installation 🛠️

To install this project, you need to have Python 3.10 installed. Then, follow these steps:

1. Clone the repository

2. Enter the project directory

3. Install the project: `poetry install`

4. Set up your OpenAI API key in the `.env` file.

## Usage 🎮

### CLI

To run the CLI, use the following command:

```bash
poetry run cli run <cache_type>
```

Replace `<cache_type>` with `no_cache`, `semantic_cache`.

### Streamlit Web App

To run the Streamlit web app, use the following command:

```bash
poetry run webapp
```

The app will be available at `localhost:8501`.

## Project Structure 📁

- `pyproject.toml`: TOML file that contains the project metadata and dependencies.
- `scripts/`: Folder containing the Streamlit app and CLI scripts.
- `semantic_caching/`: Folder containing the core caching logic.
- `cache/`: Folder to store cache files (FAISS indices and SQLite databases).

## Dependencies 📚

- langchain
- openai
- streamlit
- python-dotenv
- gptcache
- tiktoken
- rich
- torch
- typer

## Contributing 🤝

We welcome contributions to this project! Please feel free to submit issues or pull requests.

## License ⚖️

This project is licensed under the MIT License.