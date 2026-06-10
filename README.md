# Agent Project

This repository is a work-in-progress Boot.dev assignment project. The goal is to build a small educational AI agent that can inspect and modify files in a simple calculator application in order to fix a minor bug.

> **Note:** This project is for personal learning and coursework only. It is not intended or recommended for public, production, or general-purpose use.

## What is included

- `main.py` - the current AI agent entry point that sends a user prompt to Gemini.
- `functions/` - helper functions the agent can use for file operations, such as listing files, reading file contents, and writing files within a permitted working directory.
- `calculator/` - the sample calculator app the agent will eventually work on.
- `test_*.py` and `calculator/tests.py` - small tests used while developing the project.

## Current status

This repo is still under active development. The agent currently has basic plumbing for interacting with an LLM and helper file-operation functions, but it is not yet a complete or robust bug-fixing agent.

## Setup

This project uses Python 3.13 and `uv`.

```bash
uv sync
```

Create a `.env` file with a Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the agent with a prompt:

```bash
uv run python main.py "your prompt here"
```

Use verbose mode to print token usage:

```bash
uv run python main.py "your prompt here" --verbose
```

## Disclaimer

This is an experimental learning project and may contain incomplete code, bugs, or insecure behavior. Do not use it as a production AI agent or as a general-purpose automation tool.
