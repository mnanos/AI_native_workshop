# AI-Native Development Workshop Guide

## Title
AI-Native Development in Practice: Building a Simple Agentic Application with Open Tools and Local Models

## Purpose
This guide is organized by execution path. Start with the mandatory setup that takes time before the workshop, then choose one of the three run modes:

1. Web GUI with Streamlit
2. CLI fallback
3. Jupyter notebook

The workshop is designed so participants can run everything locally without requiring a paid subscription.

---

## 1. Mandatory Pre-Workshop Steps

These steps take the most time and should be completed before the live session.

### 1.1 Confirm System Requirements

Minimum:
- 8 GB RAM
- Modern CPU
- Python 3.10 or newer
- Internet access before the workshop for downloading tools and models

Better experience:
- 16 GB RAM
- SSD
- Stable internet connection during setup

### 1.2 Install Required Tools

Install:
- Python 3.10+
- Git
- Docker Desktop for Windows, or Docker Engine for Linux / WSL
- VS Code or another code editor
- Terminal access
- Jupyter Notebook / JupyterLab if using the notebook path

Verify Python:

```bash
python --version
```

On some Linux / WSL systems:

```bash
python3 --version
```

Verify Git:

```bash
git --version
```

Verify Docker:

PowerShell:

```powershell
docker --version
docker ps
```

Bash / WSL:

```bash
docker --version
docker ps
```

If `docker ps` fails, start Docker Desktop or fix Docker Engine permissions before the workshop.

### 1.3 Clone the Repository

```bash
git clone https://github.com/mnanos/AI_native_workshop.git
cd AI_native_workshop
```

### 1.4 Create and Activate the Python Virtual Environment

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

Bash / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

### 1.5 Install Python Dependencies

Install the project requirements:

```bash
python -m pip install -r requirements.txt
```

If using the notebook path, also install notebook dependencies:

```bash
python -m pip install notebook jupyterlab ipykernel pandas matplotlib
```

### 1.6 Configure Environment Variables

Create `.env` from `.env.example`.

PowerShell:

```powershell
Copy-Item .env.example .env
```

Bash / WSL:

```bash
cp .env.example .env
```

Recommended workshop configuration:

```env
MODEL_PROVIDER=ollama
MODEL_NAME=llama3.1
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=90
```

For lower-memory machines, use:

```env
MODEL_PROVIDER=ollama
MODEL_NAME=llama3.2:1b
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=180
```

Important for the notebook path: if configuring through shell environment variables instead of `.env`, use `OLLAMA_MODEL`, not `MODEL_NAME`.

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

### 1.7 Start Ollama in Docker

The project expects Ollama at:

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

If the container already exists:

```bash
docker start ollama
docker ps
```

### 1.8 Pull the Local Model

Recommended model:

```bash
docker exec -it ollama ollama pull llama3.1
```

Lower-memory fallback:

```bash
docker exec -it ollama ollama pull llama3.2:1b
```

Verify installed models:

```bash
docker exec -it ollama ollama list
```

### 1.9 Verify Ollama Responds

PowerShell:

```powershell
Invoke-RestMethod -Uri http://localhost:11434/api/chat `
  -Method Post `
  -ContentType "application/json" `
  -Body '{
    "model": "llama3.1",
    "messages": [
      {
        "role": "user",
        "content": "Say hello from local Ollama."
      }
    ],
    "stream": false
  }'
```

Bash / WSL:

```bash
curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "messages": [
      {
        "role": "user",
        "content": "Say hello from local Ollama."
      }
    ],
    "stream": false
  }'
```

If this does not return a model response, fix Ollama before continuing.

### 1.10 Pre-Workshop Readiness Checklist

- Python version is 3.10 or newer
- Git is installed
- Docker is installed and running
- Repository is cloned
- `.venv` is created and activated
- Dependencies are installed
- `.env` exists
- Ollama container is running
- Selected model is pulled
- `http://localhost:11434` responds
- Sample assignment is available at `sample_data/assignment.txt`
- Sample CSV is available at `sample_data/sensor_data.csv`

---

## 2. Web GUI Steps

Use this path for the main workshop demonstration.

### 2.1 Start Required Services

Activate the virtual environment:

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Bash / WSL:

```bash
source .venv/bin/activate
```

Start or verify Ollama:

```bash
docker start ollama
docker ps
```

Check the Ollama API:

```bash
curl http://localhost:11434/api/tags
```

### 2.2 Run the Streamlit App

```bash
streamlit run app.py
```

Streamlit usually prints:

```text
http://localhost:8501
```

Open the local URL in a browser.

### 2.3 Use the Web GUI

Paste this sample assignment into the text area:

```text
Build a Python program that reads sensor measurements from a CSV file, computes the average and standard deviation, and generates a simple plot.
```

Click **Run Workflow**.

Expected UI output sections:
- Assignment
- Requirements
- Plan
- Starter Code
- Review
- Final Next Steps

### 2.4 Web GUI Acceptance Check

The Web GUI path is ready when:
- Streamlit launches without import errors
- The browser opens the app
- Assignment input is accepted
- Planner output appears
- Builder output appears
- Reviewer output appears
- The workflow completes without a model error

---

## 3. CLI Steps

Use this path as the fallback if the Streamlit setup is slow or the browser environment is unreliable.

### 3.1 Start Required Services

Activate the virtual environment:

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Bash / WSL:

```bash
source .venv/bin/activate
```

Start or verify Ollama:

```bash
docker start ollama
docker ps
```

### 3.2 Run the CLI with the Sample Assignment

```bash
python main.py --input sample_data/assignment.txt
```

On systems where `python` is not available:

```bash
python3 main.py --input sample_data/assignment.txt
```

### 3.3 Run the CLI with Pasted Input

```bash
python main.py
```

Then paste an assignment and press `Ctrl-D` when finished.

On systems where `python` is not available:

```bash
python3 main.py
```

### 3.4 Expected CLI Output

The CLI should print these sections:
- Assignment
- Requirements
- Plan
- Starter Code
- Review
- Final Next Steps

### 3.5 CLI Acceptance Check

The CLI path is ready when:
- The assignment file is read
- The assignment section prints
- Planner output prints
- Builder output prints
- Reviewer output prints
- The command exits successfully

---

## 4. Jupyter Notebook Steps

Use this path for hands-on exploration and guided experimentation.

### 4.1 Install Notebook Dependencies

From the activated virtual environment:

```bash
python -m pip install notebook jupyterlab ipykernel requests pandas matplotlib python-dotenv
```

### 4.2 Register the Workshop Kernel

```bash
python -m ipykernel install --user --name ai-native-workshop --display-name "Python (AI Native Workshop)"
```

### 4.3 Start Required Services

Start or verify Ollama:

```bash
docker start ollama
docker ps
```

Confirm the model is installed:

```bash
docker exec -it ollama ollama list
```

### 4.4 Launch JupyterLab

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

### 4.5 Notebook Environment Variables

If the notebook does not use `.env`, set:

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

Inside the notebook, verify:

```python
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "llama3.1"
```

### 4.6 Notebook Acceptance Check

The notebook path is ready when:
- JupyterLab launches
- The notebook opens
- The `Python (AI Native Workshop)` kernel is selectable
- The notebook can reach Ollama
- The model responds from a notebook cell
- The sample assignment can be processed

---

## 5. Workshop Concept Reference

### Workshop Goal

Participants will build and run a simple AI-native application that:
- accepts a technical assignment
- breaks it into steps
- generates a first implementation draft
- reviews the output
- returns suggestions for improvement

### Learning Objectives

By the end of the workshop, participants should be able to:
- understand what AI-native development means
- distinguish between prompts, workflows, and agents
- understand the role of orchestration
- run a simple local AI application using open tools
- understand how the example can be extended after the workshop

### Core Concepts

Prompt:
A single instruction sent to a model.

Workflow:
A predefined sequence of execution steps.

Agent:
A software component with a specific role, defined input/output behavior, and possibly access to tools.

Tool:
An external capability such as file reading, code generation, formatting, or validation.

Context / Knowledge:
The information used by the system to reason correctly, such as the assignment text, constraints, and data files.

Human in the Loop:
The user can inspect intermediate outputs and refine the result.

### Use Case: AI Lab Assistant

Input:
- a short technical assignment or lab task

Output:
- requirements summary
- implementation plan
- starter code
- review comments
- next-step suggestions

---

## 6. Project Reference

### Project Structure

```text
ai-native-workshop/
|
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .env.example
|
├── agents/
│   ├── planner.py
│   ├── builder.py
│   ├── reviewer.py
│   └── deepagent.py
|
├── workflow/
│   └── coordinator.py
|
├── prompts/
│   ├── planner_prompt.txt
│   ├── builder_prompt.txt
│   └── reviewer_prompt.txt
|
├── sample_data/
│   ├── assignment.txt
│   └── sensor_data.csv
|
└── utils/
    ├── config.py
    ├── formatting.py
    └── llm.py
```

### File Responsibilities

`app.py`:
- Streamlit UI
- assignment input
- workflow run button
- progressive display of planner, builder, reviewer, and next-step output

`main.py`:
- CLI entry point
- reads assignment from file or stdin
- prints structured terminal output

`agents/planner.py`:
- extracts requirements
- identifies assumptions
- generates implementation plan

`agents/builder.py`:
- generates starter code
- uses assignment and planner output as context

`agents/reviewer.py`:
- reviews generated code
- identifies missing parts
- suggests improvements

`agents/deepagent.py`:
- orchestrates planner, builder, reviewer, and final next-step derivation

`workflow/coordinator.py`:
- compatibility layer used by the CLI and Streamlit app

`utils/llm.py`:
- sends prompts to Ollama
- handles model request errors
- abstracts API details

`prompts/*.txt`:
- role-specific system instructions

`sample_data/assignment.txt`:
- sample task for the workshop

`sample_data/sensor_data.csv`:
- optional sample CSV file for generated code demonstrations

### Workflow Logic

High-level flow:

1. User enters assignment
2. Planner extracts requirements and plan
3. Builder generates code
4. Reviewer checks code against the assignment
5. App or CLI displays all outputs

### Ollama Utility Design

The local model utility should:
- read the model name from `.env`
- call the local Ollama endpoint
- send the prompt
- return response text

Expected endpoint:

```text
POST http://localhost:11434/api/generate
```

Expected request fields:
- `model`
- `prompt`
- `stream: false`

---

## 7. Troubleshooting

### `docker` command not found

Cause:
- Docker Desktop WSL integration is not enabled
- Docker Engine is not installed in the Linux distro
- terminal was opened before Docker was installed

Fix:
- install and start Docker Desktop, or install Docker Engine for the distro
- enable Docker Desktop WSL integration when using WSL
- restart terminal
- verify with `docker --version`

### Permission denied connecting to Docker

Cause:
- current user cannot access the Docker socket
- Docker Desktop or Docker Engine is not running

Fix:
- start Docker Desktop
- verify WSL integration if using WSL
- on Linux, add the user to the Docker group if appropriate
- restart the terminal after permission changes

### Ollama container already exists

Fix:

```bash
docker start ollama
docker ps
```

Or recreate it:

```bash
docker rm -f ollama
docker run -d \
  --name ollama \
  -p 11434:11434 \
  -v ollama:/root/.ollama \
  --restart unless-stopped \
  ollama/ollama
```

### Model not found

Cause:
- selected model was not pulled yet

Fix:

```bash
docker exec -it ollama ollama pull llama3.1
docker exec -it ollama ollama list
```

### Python package missing

Cause:
- requirements are not installed in the active virtual environment

Fix:

```bash
pip install -r requirements.txt
```

### Streamlit not found

Cause:
- virtual environment is not activated
- requirements are not installed

Fix:
- activate `.venv`
- reinstall requirements

### Notebook cannot connect to Ollama

Cause:
- Ollama container is not running
- notebook has the wrong base URL or model name

Fix:

```bash
docker ps
curl http://localhost:11434/api/tags
```

In the notebook, verify:

```python
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "llama3.1"
```

### Slow model response

Cause:
- local hardware limitations

Fix:
- keep prompts concise
- use `llama3.2:1b` or another lighter model
- use CLI fallback if the UI feels slow

---

## 8. Final Acceptance Criteria

The project is ready for the workshop when:
- the repo can be cloned successfully
- the venv can be created without issues
- dependencies install successfully
- Ollama can be reached locally
- the selected model responds correctly
- Streamlit app launches
- planner output is generated
- builder output is generated
- reviewer output is generated
- CLI version also runs as fallback
- notebook path works if it is part of the workshop

---

## 9. Optional Extensions

Possible next steps after the workshop:
- add file upload support
- support PDF assignment input
- add retrieval over notes or documentation
- add testing tools
- add evaluation scoring
- add multiple workflow branches
- replace simple orchestration with LangGraph
- expose the workflow via FastAPI

