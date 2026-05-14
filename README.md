# AI-Native Workshop Demo

A small workshop project that demonstrates the difference between a prompt, a workflow, and role-based agents using local models through Ollama.

## Prerequisites
- Python 3.10+
- Git
- Docker Desktop for Windows, or Docker Engine in Linux / WSL
- Jupyter Notebook / JupyterLab if running the hands-on notebook
- Ollama running in Docker
- A local model pulled into the Ollama container

Recommended model:

```text
llama3.1
```

## Setup
Clone the repo and create a virtual environment.

PowerShell:

```powershell
git clone https://github.com/mnanos/AI_native_workshop.git
cd AI_native_workshop

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install notebook jupyterlab ipykernel pandas matplotlib

Copy-Item .env.example .env
```

Bash / WSL:

```bash
git clone https://github.com/mnanos/AI_native_workshop.git
cd AI_native_workshop

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install notebook jupyterlab ipykernel pandas matplotlib

cp .env.example .env
```

Update `.env` for the workshop model:

```bash
MODEL_PROVIDER=ollama
MODEL_NAME=llama3.1
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=90
```

Register the notebook kernel if you plan to run the Jupyter notebook:

```bash
python -m ipykernel install --user --name ai-native-workshop --display-name "Python (AI Native Workshop)"
```

## Start Ollama in Docker

The app and notebook expect Ollama at:

```text
http://localhost:11434
```

PowerShell:

```powershell
docker run -d `
  --name ollama `
  -p 11434:11434 `
  -v ollama:/root/.ollama `
  --restart unless-stopped `
  ollama/ollama
```

Bash / WSL:

```bash
docker run -d \
  --name ollama \
  -p 11434:11434 \
  -v ollama:/root/.ollama \
  --restart unless-stopped \
  ollama/ollama
```

If the container already exists, start it:

```bash
docker start ollama
docker ps
```

Pull the recommended model:

```bash
docker exec -it ollama ollama pull llama3.1
```

For lower-memory machines:

```bash
docker exec -it ollama ollama pull llama3.2:1b
```

If you use `llama3.2:1b`, also update `.env`:

```bash
MODEL_NAME=llama3.2:1b
```

Verify Ollama:

PowerShell:

```powershell
Invoke-RestMethod http://localhost:11434/api/tags
```

Bash / WSL:

```bash
curl http://localhost:11434/api/tags
```

## Run the Streamlit App

Activate the virtual environment, then run:

```bash
streamlit run app.py
```

Streamlit prints a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser, paste an assignment, and click **Run Workflow**.

The UI now renders the workflow incrementally as each stage completes.

## Run the CLI Fallback

If you do not want to use the Streamlit UI, keep the Ollama container running and run:

```bash
python main.py --input sample_data/assignment.txt
```

You can also paste input directly:

```bash
python main.py
```

Then paste an assignment and press `Ctrl-D` when finished.

The CLI also prints sections incrementally as each stage finishes.

## Run the Jupyter Notebook

From the activated virtual environment:

```bash
jupyter lab
```

Open:

```text
AI_Native_Workshop_Hands_On_Notebook.ipynb
```

Select this kernel:

```text
Python (AI Native Workshop)
```

The notebook reads `OLLAMA_MODEL` if you configure the model through shell environment variables:

PowerShell:

```powershell
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "llama3.1"
```

Bash / WSL:

```bash
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="llama3.1"
```

## Troubleshooting

- `docker: command not found`: install Docker Desktop, enable WSL integration if needed, or install Docker Engine in your Linux distro.
- `Could not connect to Ollama`: run `docker start ollama`, check `docker ps`, and verify `OLLAMA_BASE_URL` in `.env`.
- `model 'llama3.1' was not found`: run `docker exec -it ollama ollama pull llama3.1`.
- Slow responses: try `llama3.2:1b` and update `MODEL_NAME` in `.env`.
- Notebook uses the wrong model: set `OLLAMA_MODEL`, not `MODEL_NAME`, when configuring the notebook through environment variables.

## What It Shows
- `Planner`: extracts requirements, proposes an ASCII-tree project structure, and creates a plan
- `Builder`: generates file-labeled starter code that follows the proposed project structure
- `Reviewer`: checks coverage and suggests improvements
- `DeepAgent`: orchestrates the deterministic multi-step flow
- `WorkflowCoordinator`: thin wrapper that keeps the CLI and Streamlit entrypoints stable

## Agent Architecture
- `agents/planner.py`: Planner role
- `agents/builder.py`: Builder role
- `agents/reviewer.py`: Reviewer role
- `agents/deepagent.py`: orchestrator that runs Planner, Builder, and Reviewer
- `workflow/coordinator.py`: compatibility layer that delegates to `DeepAgent`

`DeepAgent.run_incremental()` emits these steps in order:
1. `assignment`
2. `planner`
3. `builder`
4. `reviewer`
5. `next_steps`
