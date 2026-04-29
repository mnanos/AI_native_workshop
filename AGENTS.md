# Repository Guidelines

## Project Structure & Module Organization
This repository is a small Python workshop demo that compares prompts, workflows, and role-based agents over a local Ollama model.

- `app.py`: Streamlit UI entry point.
- `main.py`: CLI entry point for running the workflow from a file or stdin.
- `agents/`: planner, builder, reviewer, and `DeepAgent` orchestrator implementations.
- `workflow/`: orchestration compatibility layer, centered on `WorkflowCoordinator`.
- `utils/`: shared helpers for config, formatting, and model access.
- `prompts/`: plain-text system prompts loaded by the role agents.
- `sample_data/`: example assignment and CSV input for demos.
- Root docs such as `README.md`, `design.md`, and `spec.md` describe usage and intent.

## Build, Test, and Development Commands
Set up a local environment before making changes:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Run the UI:

```bash
streamlit run app.py
```

Run the CLI:

```bash
python main.py --input sample_data/assignment.txt
```

Start the local model backend separately:

```bash
ollama serve
ollama run llama3
```

## Coding Style & Naming Conventions
Follow existing Python style: 4-space indentation, type hints on public functions, and concise docstrings for modules and classes. Use `snake_case` for functions, variables, and files; use `PascalCase` for classes such as `DeepAgent` and `WorkflowCoordinator`. Keep prompt filenames descriptive and aligned with agent names, for example `planner_prompt.txt`.

## Testing Guidelines
There is no formal test suite yet. Before opening a PR, run the CLI and Streamlit paths against `sample_data/assignment.txt` and confirm the planner, builder, and reviewer stages complete without exceptions. If you add tests, prefer `pytest`, place them under `tests/`, and name files `test_<module>.py`.

## Commit & Pull Request Guidelines
Recent history uses short, imperative subjects such as `Update app run instructions` and `Document Ollama service startup`. Keep commit messages brief and action-oriented. PRs should include a clear summary, note any config or model changes, link related issues when applicable, and attach screenshots for UI changes in `app.py`.

## Configuration Tips
Local runtime settings live in `.env`. Keep secrets out of version control, and use `.env.example` as the source of documented defaults for `MODEL_NAME`, `OLLAMA_BASE_URL`, and related settings.
