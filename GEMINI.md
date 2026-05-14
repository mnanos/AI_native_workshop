# AI-Native Workshop Project Instructions

This document outlines the architecture, conventions, and workflows for the AI-Native Workshop Demo project.

## Architecture Overview

The project follows a role-based agent architecture orchestrated by a central deep agent.

- **Agents (`agents/`)**: Individual agents with specific roles (Planner, Builder, Reviewer). Each agent typically takes the previous agents' outputs as context.
- **Orchestration (`agents/deepagent.py`)**: `DeepAgent` manages the sequential execution. It provides both a standard `run` method and a `run_incremental` generator for streaming updates to the UI/CLI.
- **Workflow (`workflow/coordinator.py`)**: A compatibility layer providing a stable interface for different entry points.
- **Entry Points**:
  - `app.py`: Streamlit-based web interface.
  - `main.py`: CLI-based interface.
- **LLM Integration (`utils/llm.py`)**: Handles communication with local models via Ollama.

## Development Conventions

- **Incremental Processing**: Agents should support incremental output where possible. `DeepAgent.run_incremental` is the preferred way to execute the workflow in interactive environments.
- **Configuration**: Use `.env` for environment variables. Default values should be consistent with `.env.example`.
- **Error Handling**: Graceful handling of LLM connectivity issues (Ollama availability).
- **Testing**: There are currently no automated tests in the project. Adding unit tests for agents and utility functions is a priority for future development.

## Workflow

1. **Planner**: Extracts requirements and proposes structure.
2. **Builder**: Generates starter code.
3. **Reviewer**: Checks coverage and suggests improvements.

## Environment Setup

- Python 3.10+
- Ollama running locally (usually in Docker).
- Recommended model: `llama3.1` or `llama3.2:1b`.
