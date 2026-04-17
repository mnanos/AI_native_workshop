# AI-Native Workshop Demo

A small workshop project that demonstrates the difference between a prompt, a workflow, and role-based agents using local models through Ollama.

## Prerequisites
- Python 3.10+
- Ollama installed locally
- A local model pulled, for example:

```bash
ollama pull llama3
```

## Setup
Run these commands once from the project directory:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

The default `.env` values use Ollama and `llama3`:

```bash
MODEL_PROVIDER=ollama
MODEL_NAME=llama3
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=90
```

## Run the app

Use two terminals.

### Terminal 1: start Ollama

Start or verify the local model:

```bash
ollama run llama3
```

If Ollama is already running as a background service, this command opens an interactive
model session and confirms the model is available. You can leave it open while using
the app.

### Terminal 2: start Streamlit

In a second terminal, activate the virtual environment and run the UI:

```bash
cd /home/mnanos/AI_native_w
source .venv/bin/activate
streamlit run app.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser, paste an assignment, and click **Run Workflow**.

## Run the CLI fallback

If you do not want to use the Streamlit UI, keep Ollama running and run:

```bash
source .venv/bin/activate
python main.py --input sample_data/assignment.txt
```

You can also paste input directly:

```bash
python main.py
```

Then paste an assignment and press `Ctrl-D` when finished.

## Troubleshooting

- `ollama: command not found`: install Ollama and make sure it is on your `PATH`.
- `Could not connect to Ollama`: start Ollama and verify `OLLAMA_BASE_URL` in `.env`.
- `model 'llama3' was not found`: run `ollama pull llama3`.
- Slow responses: try a smaller local model and update `MODEL_NAME` in `.env`.

## What It Shows
- `Planner`: extracts requirements and creates a plan
- `Builder`: generates starter code
- `Reviewer`: checks coverage and suggests improvements
- `Coordinator`: orchestrates a deterministic workflow
