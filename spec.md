# AI-Native Workshop Demo — Implementation Spec for Codex CLI

## Goal
Build a small, fully local, reproducible AI-native demo application for a 1-hour workshop. The app should demonstrate the difference between a simple prompt, a workflow, and role-based agents by implementing an **AI Lab Assistant** that:

1. accepts a short technical assignment from a user,
2. extracts requirements,
3. creates an implementation plan,
4. generates starter code,
5. reviews the generated output,
6. shows the final result in a simple UI.

The system must run **without paid subscriptions** and use **local open models via Ollama**.

---

## Product framing
This is a workshop/demo project, not a production system.

Priorities:
- clarity over complexity,
- small codebase,
- easy local setup,
- good structure for teaching AI-native design,
- deterministic orchestration with role-based agent modules,
- minimal dependencies.

Non-goals:
- authentication,
- database persistence,
- multi-user support,
- advanced observability,
- deployment to cloud,
- complex agent autonomy.

---

## Core concept to demonstrate
The app should make visible that:
- a **prompt** is a single model request,
- a **workflow** is a sequence of explicit steps,
- an **agent** is a role-based software component with a specific responsibility.

Use three role modules:
- **Planner**
- **Builder**
- **Reviewer**

The workflow should be explicit and deterministic:

`User input → Planner → Builder → Reviewer → Final assembled result`

---

## Technical requirements

### Stack
- Python 3.10+
- Streamlit for UI
- Ollama for local model inference
- Pure Python orchestration
- No LangChain / LangGraph unless absolutely necessary (prefer not to use them)

### Model access
Use Ollama HTTP API at:
- default base URL: `http://localhost:11434`

Default model:
- `llama3`

Allow model name to be configured via environment variable.

### Dependencies
Keep dependencies minimal. Preferred:
- `streamlit`
- `requests`
- `python-dotenv`

Optional:
- `pydantic` only if it meaningfully improves code clarity

Do **not** add heavy frameworks.

---

## User experience

### Main flow
The user opens the app and sees:
- workshop title,
- short description,
- text area to paste an assignment,
- button to run the workflow.

After running, the UI should clearly show these sections:
1. Assignment
2. Requirements
3. Plan
4. Starter Code
5. Review
6. Final Next Steps

### Usability expectations
- The app should work with a pasted assignment only.
- No login.
- No file upload required for v1.
- Handle empty input gracefully.
- Show clear error messages if Ollama is not running or the model is unavailable.

### Style
- Clean, simple Streamlit layout.
- Suitable for workshop/demo use.
- Focus on readability.

---

## Sample use case
The demo should work well with input such as:

> Build a Python program that reads sensor measurements from a CSV file, computes the average and standard deviation, and generates a simple plot.

The app should produce:
- requirement summary,
- implementation steps,
- starter Python code,
- review feedback,
- suggested improvements.

---

## Functional requirements

### 1. Planner module
Create a module for the Planner role.

Responsibilities:
- read the assignment,
- extract explicit requirements,
- identify assumptions,
- generate a concise step-by-step implementation plan.

Output format should be structured text with headings or bullets.

Suggested outputs:
- Requirements
- Assumptions
- Implementation Steps
- Edge Cases

### 2. Builder module
Create a module for the Builder role.

Responsibilities:
- use the original assignment and planner output,
- generate starter Python code,
- keep code simple and readable,
- include comments,
- avoid excessive abstraction.

The Builder output should be code only or code-first, with minimal explanatory text.

### 3. Reviewer module
Create a module for the Reviewer role.

Responsibilities:
- compare generated code against the assignment and plan,
- identify gaps,
- identify risks and edge cases,
- suggest practical improvements.

Suggested output sections:
- Coverage Check
- Missing Parts
- Risks / Edge Cases
- Improvement Suggestions

### 4. Coordinator / workflow module
Create a coordinator that:
- validates input,
- calls Planner,
- passes Planner output to Builder,
- passes assignment + requirements + code to Reviewer,
- assembles a final result object.

The workflow must be deterministic and easy to read.

### 5. LLM client module
Create a small utility for calling Ollama.

Requirements:
- configurable base URL,
- configurable model name,
- timeout handling,
- clear error messages,
- one reusable function for chat/generation.

Prefer a simple interface like:

```python
ask_model(system_prompt: str, user_prompt: str) -> str
```

or equivalent.

### 6. Final result assembly
Create a final result object/dictionary containing:
- assignment
- requirements
- plan
- starter_code
- review
- next_steps

`next_steps` may be derived from the review stage or generated separately by simple formatting logic.

---

## Non-functional requirements
- Code should be easy for students to read.
- Modules should be small and well named.
- Use docstrings and comments where useful.
- Include basic type hints.
- Avoid overengineering.
- Keep functions short.
- Make the app robust enough for a live workshop.

---

## Project structure
Create the repository with this structure:

```text
ai-native-workshop/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── agents/
│   ├── __init__.py
│   ├── planner.py
│   ├── builder.py
│   └── reviewer.py
├── prompts/
│   ├── planner_prompt.txt
│   ├── builder_prompt.txt
│   └── reviewer_prompt.txt
├── workflow/
│   ├── __init__.py
│   └── coordinator.py
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── llm.py
│   └── formatting.py
└── sample_data/
    ├── assignment.txt
    └── sensor_data.csv
```

---

## File-by-file requirements

### `app.py`
Implement a Streamlit app.

Requirements:
- page title and short intro,
- assignment text area,
- button to run workflow,
- display sections for each workflow artifact,
- syntax-highlight starter code,
- show helpful error states.

Suggested section order:
1. Assignment
2. Requirements
3. Plan
4. Starter Code
5. Review
6. Next Steps

### `main.py`
Implement a CLI entry point.

Requirements:
- accept assignment via prompt or sample file,
- run the same coordinator,
- print each output section clearly.

This exists as a fallback in case Streamlit is not used during the workshop.

### `agents/planner.py`
Implement a function/class for the planner role.

Preferred interface:

```python
def run_planner(assignment: str) -> dict:
    ...
```

It may return structured fields such as:
- `requirements`
- `assumptions`
- `plan`
- `edge_cases`

### `agents/builder.py`
Implement a function/class for the builder role.

Preferred interface:

```python
def run_builder(assignment: str, plan_context: str) -> str:
    ...
```

Return starter code as a string.

### `agents/reviewer.py`
Implement a function/class for the reviewer role.

Preferred interface:

```python
def run_reviewer(assignment: str, requirements: str, code: str) -> dict:
    ...
```

Suggested fields:
- `coverage_check`
- `missing_parts`
- `risks`
- `improvements`

### `workflow/coordinator.py`
Implement the main deterministic workflow.

Preferred interface:

```python
def run_workflow(assignment: str) -> dict:
    ...
```

Responsibilities:
- validate input,
- orchestrate all roles,
- return final combined result.

### `utils/config.py`
Load environment variables.

Required variables:
- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`

Provide sensible defaults:
- `http://localhost:11434`
- `llama3`

### `utils/llm.py`
Implement the Ollama API wrapper.

Requirements:
- use `requests`,
- expose one simple reusable function,
- raise meaningful exceptions for:
  - connection failure,
  - timeout,
  - invalid response.

### `utils/formatting.py`
Helper functions for:
- combining planner sections,
- formatting final next steps,
- safe rendering in Streamlit and CLI.

### `prompts/*.txt`
Store role prompts in separate files rather than hardcoding large prompt strings inline.

---

## Prompt design requirements
Prompts must be concise, role-based, and workshop-friendly.

### Planner prompt
The Planner should:
- analyze the assignment,
- extract requirements,
- identify assumptions,
- propose implementation steps,
- mention edge cases.

### Builder prompt
The Builder should:
- generate simple, readable starter Python code,
- align with the plan,
- include comments,
- prefer functions over monolithic code,
- not overcomplicate the implementation.

### Reviewer prompt
The Reviewer should:
- check coverage against the assignment,
- identify missing parts,
- identify risks,
- suggest realistic improvements.

Prompt outputs should be easy to display in UI.

---

## Error handling requirements
The app must handle these cases gracefully:

### Empty assignment
Show a user-friendly validation message.

### Ollama not running
Show a clear message such as:
> Could not connect to Ollama. Please start Ollama locally and try again.

### Model missing
Show a clear message such as:
> The configured Ollama model is not available locally. Please run `ollama pull <model>`.

### Model returns malformed output
Do not crash. Fall back to raw text display where possible.

---

## README requirements
Write a clear README for workshop participants.

Include:
- what the project does,
- why it demonstrates AI-native development,
- prerequisites,
- installation steps,
- how to install Ollama,
- how to pull the model,
- how to run the Streamlit app,
- how to run the CLI version,
- example assignment text,
- troubleshooting tips.

### README setup section should include commands like

```bash
git clone <repo>
cd ai-native-workshop
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

And for Ollama:

```bash
ollama pull llama3
```

Run app:

```bash
streamlit run app.py
```

Fallback CLI:

```bash
python main.py
```

---

## `.env.example` requirements
Create `.env.example` with:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

---

## `.gitignore` requirements
Include at minimum:
- `.venv/`
- `__pycache__/`
- `.env`
- `.DS_Store`
- `.streamlit/`

---

## Sample data requirements

### `sample_data/assignment.txt`
Add a sample assignment that matches the workshop example.

### `sample_data/sensor_data.csv`
Add a small CSV file with fake sensor values for demo/testing purposes.

---

## Output contract
The final workflow output should be a dictionary with this approximate shape:

```python
{
    "assignment": str,
    "requirements": str,
    "plan": str,
    "starter_code": str,
    "review": {
        "coverage_check": str,
        "missing_parts": str,
        "risks": str,
        "improvements": str,
    },
    "next_steps": str,
}
```

Keep field names stable and simple.

---

## Implementation style guidance
- Prefer straightforward functions over complex class hierarchies.
- Keep modules independent and readable.
- Use dataclasses only if they improve clarity.
- Avoid “agent framework” abstractions.
- Make the workflow logic obvious to students reading the code.
- Favor explicit code over clever code.

---

## Acceptance criteria
The project is complete when all of the following are true:

1. `streamlit run app.py` launches a working UI.
2. A user can paste an assignment and run the workflow.
3. The app calls a local Ollama model.
4. The Planner, Builder, and Reviewer are separate modules.
5. The workflow output is displayed in clear sections.
6. Errors are handled gracefully when Ollama is unavailable.
7. `python main.py` works as a CLI fallback.
8. `README.md` contains complete local setup instructions.
9. Sample files are present.
10. The codebase is easy to explain in a workshop.

---

## Nice-to-have features (only if time permits)
Implement only after core requirements are done.

- button to load sample assignment,
- collapsible sections in Streamlit,
- “copy code” friendly formatting,
- simple health check for Ollama connection,
- model name shown in the UI,
- markdown rendering for planner/reviewer outputs.

Do not add features that compromise simplicity.

---

## Explicit constraints for Codex CLI
- Generate complete working code, not stubs.
- Do not introduce unnecessary frameworks.
- Do not use cloud APIs.
- Do not assume any paid service.
- Keep setup friction low.
- Prioritize workshop readability.
- Ensure the app is runnable locally with minimal steps.

---

## Suggested build order
1. Create project skeleton.
2. Add config and Ollama client.
3. Implement prompt files.
4. Implement Planner.
5. Implement Builder.
6. Implement Reviewer.
7. Implement coordinator workflow.
8. Implement CLI.
9. Implement Streamlit UI.
10. Add README, sample data, and polish error handling.

---

## Final deliverable summary
Codex CLI should generate a small repository for a workshop demo that teaches AI-native development through a local, open, role-based workflow app using Python, Streamlit, and Ollama.
