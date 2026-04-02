# AI-Native Development Workshop Guide

## Title
AI-Native Development in Practice: Building a Simple Agentic Application with Open Tools and Local Models

## Purpose
This document contains the full workshop instructions, including the required tools, system requirements, local setup steps, Python virtual environment instructions, project structure, required files, execution steps, and delivery guidance.

The workshop is designed so that participants can run everything locally without requiring a paid subscription.

---

## 1. Workshop Overview

### Format
- Online
- Hands-on
- Duration: 1 hour

### Audience
- Electrical and Computer Engineering students
- Students with basic Python knowledge

### Workshop Goal
Participants will build and run a simple AI-native application that:
- accepts a technical assignment
- breaks it into steps
- generates a first implementation draft
- reviews the output
- returns suggestions for improvement

---

## 2. Learning Objectives

By the end of the workshop, participants should be able to:
- understand what AI-native development means
- distinguish between prompts, workflows, and agents
- understand the role of orchestration
- run a simple local AI application using open tools
- understand how the example can be extended after the workshop

---

## 3. Workshop Use Case

### AI Lab Assistant
The example application acts as a small AI lab assistant.

Input:
- a short technical assignment or lab task

Output:
- requirements summary
- implementation plan
- starter code
- review comments
- next-step suggestions

### Example Assignment
Build a Python program that reads sensor measurements from a CSV file, computes the average and standard deviation, and generates a simple plot.

---

## 4. Core Concepts to Explain During the Workshop

### Prompt
A single instruction sent to a model.

### Workflow
A predefined sequence of execution steps.

### Agent
A software component with a specific role, defined input/output behavior, and possibly access to tools.

### Tool
An external capability such as file reading, code generation, formatting, or validation.

### Context / Knowledge
The information used by the system to reason correctly, such as the assignment text, constraints, and data files.

### Human in the Loop
The user can inspect intermediate outputs and refine the result.

---

## 5. Recommended Technical Stack

The workshop should use a lightweight open stack.

### Required Tools
- Python 3.10 or newer
- Git
- Ollama
- VS Code or another code editor
- Terminal access

### Python Libraries
- streamlit
- requests
- python-dotenv
- pydantic (optional)
- pandas (optional, for sample CSV handling)
- matplotlib (optional, for plotting)

### Local Model
Recommended local models via Ollama:
- llama3
- mistral
- qwen

Recommended default for the workshop:
- `llama3`

---

## 6. System Requirements

### Minimum
- 8 GB RAM
- Modern CPU
- Python 3.10+
- Internet access only for downloading tools and the model before the session

### Better Experience
- 16 GB RAM
- SSD
- stable internet connection before the workshop for installation

### Important Note
The project is designed to run locally, but model performance depends on the participant's laptop.

---

## 7. Installation Requirements Before the Workshop

Participants should install the following in advance:

### Python
Check version:

```bash
python --version
```

### Git
Check version:

```bash
git --version
```

### Ollama
Install Ollama from the official site, then verify:

```bash
ollama --version
```

### Pull the Model
Before the workshop, ask participants to run:

```bash
ollama pull llama3
```

To test the model:

```bash
ollama run llama3
```

---

## 8. Python Virtual Environment Setup

Participants should create and activate a virtual environment.

### Create project folder

```bash
mkdir ai-native-workshop
cd ai-native-workshop
```

### Create virtual environment

#### macOS / Linux
```bash
python -m venv .venv
```

#### Windows
```bash
python -m venv .venv
```

### Activate virtual environment

#### macOS / Linux
```bash
source .venv/bin/activate
```

#### Windows PowerShell
```powershell
.venv\Scripts\Activate.ps1
```

#### Windows CMD
```cmd
.venv\Scripts\activate.bat
```

### Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

## 9. Install Python Dependencies

Create a `requirements.txt` file with the following content:

```txt
streamlit
requests
python-dotenv
pydantic
pandas
matplotlib
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 10. Environment Configuration

Create a `.env` file in the project root.

### `.env.example`

```env
MODEL_PROVIDER=ollama
MODEL_NAME=llama3
OLLAMA_BASE_URL=http://localhost:11434
```

Participants can create `.env` from `.env.example`.

#### macOS / Linux
```bash
cp .env.example .env
```

#### Windows PowerShell
```powershell
Copy-Item .env.example .env
```

---

## 11. Suggested Project Structure

```text
ai-native-workshop/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .env.example
│
├── agents/
│   ├── planner.py
│   ├── builder.py
│   └── reviewer.py
│
├── workflow/
│   └── coordinator.py
│
├── prompts/
│   ├── planner_prompt.txt
│   ├── builder_prompt.txt
│   └── reviewer_prompt.txt
│
├── sample_data/
│   ├── assignment.txt
│   └── sensor_data.csv
│
└── utils/
    ├── llm.py
    └── parser.py
```

---

## 12. File Responsibilities

### `app.py`
Streamlit UI.

Responsibilities:
- text area for assignment input
- button to run workflow
- display planner output
- display builder output
- display reviewer output

### `main.py`
CLI entry point.

Responsibilities:
- accept assignment text
- run the workflow
- print results in terminal

### `agents/planner.py`
Responsibilities:
- extract requirements
- identify assumptions
- generate implementation plan

### `agents/builder.py`
Responsibilities:
- generate starter code
- generate file/function suggestions

### `agents/reviewer.py`
Responsibilities:
- review generated code
- identify missing parts
- suggest improvements

### `workflow/coordinator.py`
Responsibilities:
- orchestrate the full execution flow
- pass outputs between agents
- return final structured result

### `utils/llm.py`
Responsibilities:
- send prompts to Ollama
- handle local model requests
- abstract away API details

### `utils/parser.py`
Responsibilities:
- normalize or format outputs
- handle simple parsing logic if structured output is needed

### `prompts/*.txt`
Contain role-specific system instructions for each agent.

### `sample_data/assignment.txt`
Stores a sample task for the workshop.

### `sample_data/sensor_data.csv`
Optional sample CSV file for demonstration.

---

## 13. Suggested Prompt Files

### `prompts/planner_prompt.txt`
```txt
You are a planning assistant. Read the assignment, identify the requirements, assumptions, and implementation steps. Return a concise structured plan.
```

### `prompts/builder_prompt.txt`
```txt
You are a coding assistant. Based on the assignment and implementation plan, generate clean starter code with comments and a simple structure.
```

### `prompts/reviewer_prompt.txt`
```txt
You are a reviewer. Check whether the generated code addresses the assignment requirements. Identify missing parts, risks, edge cases, and improvement suggestions.
```

---

## 14. Example Workflow Logic

### High-level flow
1. user enters assignment
2. planner extracts requirements and plan
3. builder generates code
4. reviewer checks code against the assignment
5. app displays all outputs

### Example pseudo-code

```python
assignment = get_user_input()

requirements = planner.extract_requirements(assignment)
plan = planner.create_plan(assignment)

starter_code = builder.generate_code(assignment, plan)

review = reviewer.review_output(
    assignment=assignment,
    requirements=requirements,
    code=starter_code,
)

return {
    "requirements": requirements,
    "plan": plan,
    "code": starter_code,
    "review": review,
}
```

---

## 15. Suggested Ollama Utility Design

### Example logic for `utils/llm.py`
The module should:
- read the model name from `.env`
- call the local Ollama endpoint
- send the prompt
- return the response text

Expected endpoint:
- `POST http://localhost:11434/api/generate`

Expected input fields:
- model
- prompt
- stream false

---

## 16. Streamlit App Requirements

The UI should include:
- title of the workshop demo
- short description
- text area for task input
- run button
- separate sections for:
  - requirements
  - plan
  - starter code
  - review

### Suggested UI Sections
- Assignment Input
- Planner Output
- Builder Output
- Reviewer Output

---

## 17. CLI Version Requirements

The CLI version should:
- read input from file or prompt
- print structured results in the terminal
- be usable if the Streamlit setup is too slow during the workshop

Example run:

```bash
python main.py
```

Optional:

```bash
python main.py --input sample_data/assignment.txt
```

---

## 18. Recommended Sample Files

### `sample_data/assignment.txt`
```txt
Build a Python program that reads sensor measurements from a CSV file, computes the average and standard deviation, and generates a simple plot.
```

### `sample_data/sensor_data.csv`
Example:

```csv
sensor_id,value
1,10.2
2,12.4
3,11.7
4,9.8
5,10.9
```

---

## 19. Workshop Delivery Instructions

### Before the Session
Send participants:
- repo link
- install instructions
- list of prerequisites
- model name to pull with Ollama
- sample assignment

### During the Session
Recommended flow:

#### Part 1: Concepts
Explain:
- prompt
- workflow
- agent
- tool
- context

#### Part 2: Architecture
Show:
- planner
- builder
- reviewer
- coordinator

#### Part 3: Code Walkthrough
Explain the structure of:
- app.py
- workflow/coordinator.py
- utils/llm.py
- one agent example

#### Part 4: Live Run
Demonstrate:
- entering the assignment
- planner output
- builder output
- reviewer output

#### Part 5: Participant Run
Ask participants to:
- activate venv
- start Ollama
- run the app
- test the sample assignment

---

## 20. Commands to Run the Project

### Start Ollama model service
If Ollama is installed, ensure it is available locally.

### Run Streamlit UI
```bash
streamlit run app.py
```

### Run CLI
```bash
python main.py
```

---

## 21. Suggested README Sections

The project README should include:
- project title
- workshop purpose
- prerequisites
- setup steps
- venv instructions
- Ollama setup
- how to run Streamlit
- how to run CLI
- example input
- possible extensions

---

## 22. Common Troubleshooting Notes

### Problem: `ollama` command not found
Cause:
- Ollama not installed or not in PATH

Fix:
- install Ollama
- restart terminal
- verify with `ollama --version`

### Problem: model not found
Cause:
- model not pulled yet

Fix:
```bash
ollama pull llama3
```

### Problem: Python package missing
Cause:
- requirements not installed in active venv

Fix:
```bash
pip install -r requirements.txt
```

### Problem: Streamlit not found
Cause:
- virtual environment not activated

Fix:
- activate `.venv`
- reinstall requirements

### Problem: slow model response
Cause:
- local hardware limitations

Fix:
- keep prompts concise
- use a lighter model if needed
- use CLI fallback if UI feels slow

---

## 23. Acceptance Criteria for the Project

The project is considered ready for the workshop if:
- the repo can be cloned successfully
- the venv can be created without issues
- dependencies install successfully
- Ollama can be reached locally
- the selected model responds correctly
- Streamlit app launches
- the planner output is generated
- the builder output is generated
- the reviewer output is generated
- the CLI version also runs as fallback

---

## 24. Optional Extensions After the Workshop

Possible next steps:
- add file upload support
- support PDF assignment input
- add retrieval over notes or documentation
- add testing tools
- add evaluation scoring
- add multiple workflow branches
- replace simple orchestration with LangGraph
- expose the workflow via FastAPI

---

## 25. Summary for Organizers or Internal Team

This workshop uses:
- open tools
- local open models
- no paid subscription
- simple reproducible setup
- student-friendly use case

Participants will:
- understand core AI-native concepts
- see a small agentic workflow
- run it locally
- leave with a project they can extend

---

## 26. Short Internal Checklist

### Instructor Checklist
- verify the repo works on a clean machine
- verify the chosen model with Ollama
- prepare sample assignment
- prepare sample CSV
- prepare demo screenshots or backup output
- prepare a CLI fallback

### Participant Checklist
- install Python
- install Git
- install Ollama
- pull the selected model
- clone repo
- create venv
- install requirements
- run app

---

## 27. Recommended Default Configuration

For the workshop, keep the defaults simple:

- model: `llama3`
- provider: `ollama`
- UI: `streamlit`
- fallback: `main.py`
- sample input: `sample_data/assignment.txt`

This minimizes confusion and support overhead.

---

## 28. Final Positioning Statement

A practical introduction to AI-native development through a small but complete role-based application built with open tools and local models.
