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
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run
Start the Streamlit app:

```bash
streamlit run app.py
```

Run the CLI fallback:

```bash
python main.py --input sample_data/assignment.txt
```

## What It Shows
- `Planner`: extracts requirements and creates a plan
- `Builder`: generates starter code
- `Reviewer`: checks coverage and suggests improvements
- `Coordinator`: orchestrates a deterministic workflow
