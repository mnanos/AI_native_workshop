# Run the AI Native Workshop Notebook on Windows

Below are detailed Windows instructions for running the workshop Jupyter notebook.

## 1. Install required software

Install these before the workshop:

### Required
- **Python 3.10 or newer**
- **Git**
- **Docker Desktop**
- **Visual Studio Code** or another editor
- **Jupyter Notebook / JupyterLab**

### Recommended
- Windows 10 or Windows 11
- WSL2 enabled
- At least 8 GB RAM; 16 GB recommended
- At least 10–20 GB free disk space for local models

---

## 2. Install Docker Desktop

Download and install Docker Desktop for Windows.

During installation, enable:

```text
Use WSL 2 instead of Hyper-V
```

After installation:

1. Open **Docker Desktop**
2. Wait until it says Docker is running
3. Open **PowerShell**
4. Test Docker:

```powershell
docker --version
docker ps
```

If `docker ps` works, Docker is ready.

---

## 3. Clone or create the workshop project folder

Open **PowerShell** and run:

```powershell
cd $HOME
git clone https://github.com/mnanos/AI_native_workshop.git
cd AI_native_workshop
```

If you are not using Git, create a folder manually and place the notebook inside it:

```powershell
cd $HOME
mkdir AI_native_workshop
cd AI_native_workshop
```

Then copy the notebook file into this folder:

```text
AI_Native_Workshop_Hands_On_Notebook.ipynb
```

---

## 4. Create a Python virtual environment

From the project folder:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

When activated, your terminal should show something like:

```text
(.venv) PS C:\Users\YourName\AI_native_workshop>
```

---

## 5. Install Python dependencies

Run:

```powershell
python -m pip install --upgrade pip
pip install notebook jupyterlab ipykernel requests pandas matplotlib
```

Optional but useful:

```powershell
pip install python-dotenv
```

---

## 6. Register the Jupyter kernel

Still inside the activated virtual environment, run:

```powershell
python -m ipykernel install --user --name ai-native-workshop --display-name "Python (AI Native Workshop)"
```

This creates a dedicated notebook kernel.

---

## 7. Start Ollama in Docker

The notebook expects Ollama to be available at:

```text
http://localhost:11434
```

Start the Ollama container:

```powershell
docker run -d `
  --name ollama `
  -p 11434:11434 `
  -v ollama:/root/.ollama `
  --restart unless-stopped `
  ollama/ollama
```

Check that it is running:

```powershell
docker ps
```

You should see a container named:

```text
ollama
```

---

## 8. Pull a local model

For the workshop, pull one model.

Recommended:

```powershell
docker exec -it ollama ollama pull llama3.1
```

Alternative smaller model:

```powershell
docker exec -it ollama ollama pull mistral
```

Check installed models:

```powershell
docker exec -it ollama ollama list
```

---

## 9. Test Ollama from PowerShell

Run:

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

If it returns a model response, Ollama is working.

---

## 10. Start Jupyter Notebook or JupyterLab

From the same project folder and activated venv:

```powershell
jupyter notebook
```

or:

```powershell
jupyter lab
```

A browser window should open.

Open:

```text
AI_Native_Workshop_Hands_On_Notebook.ipynb
```

---

## 11. Select the correct kernel

Inside Jupyter:

```text
Kernel → Change Kernel → Python (AI Native Workshop)
```

Or in JupyterLab:

```text
Kernel selector, top right → Python (AI Native Workshop)
```

This is important. The notebook should not run on a random global Python installation.

---

## 12. Configure the model name in the notebook

The notebook should use:

```python
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "llama3.1"
```

If you pulled `mistral`, change it to:

```python
MODEL_NAME = "mistral"
```

---

## 13. Run the notebook

Use:

```text
Run → Run All Cells
```

Or run cells one by one.

Recommended for workshop:

1. Run setup/check cells
2. Run Ollama connectivity check
3. Run sample data generation
4. Run AI as chatbot example
5. Run Planner / Builder / Reviewer workflow
6. Run deterministic tool example
7. Run participant exercise

---

## 14. Important note about shell commands in notebooks on Windows

Some notebook cells may use Linux/macOS shell syntax like:

```bash
!docker ps
```

That usually works.

But cells using:

```bash
%%bash
```

may not work in a native Windows Jupyter environment unless Git Bash or WSL is configured.

For Windows, prefer running Docker commands directly in **PowerShell**, not inside notebook cells.

Use the notebook mainly for:
- Python code
- calling Ollama API
- running the agent workflow
- displaying outputs
- generating sample data

Use PowerShell for:
- Docker start/stop
- model pull
- container logs
- troubleshooting

---

## 15. Useful Windows Docker commands

### Start existing Ollama container

```powershell
docker start ollama
```

### Stop Ollama container

```powershell
docker stop ollama
```

### Restart Ollama

```powershell
docker restart ollama
```

### View logs

```powershell
docker logs -f ollama
```

### List models

```powershell
docker exec -it ollama ollama list
```

### Pull another model

```powershell
docker exec -it ollama ollama pull mistral
```

### Remove a model

```powershell
docker exec -it ollama ollama rm mistral
```

### Delete the container but keep models

```powershell
docker rm -f ollama
```

The models remain because they are stored in the Docker volume:

```text
ollama
```

### Delete everything including downloaded models

```powershell
docker rm -f ollama
docker volume rm ollama
```

---

## 16. Optional: run Open WebUI too

If you want a browser chat UI in addition to the notebook:

```powershell
docker run -d `
  --name open-webui `
  -p 3000:8080 `
  -v open-webui:/app/backend/data `
  --add-host=host.docker.internal:host-gateway `
  --restart unless-stopped `
  ghcr.io/open-webui/open-webui:main
```

Open:

```text
http://localhost:3000
```

Configure Ollama endpoint as:

```text
http://host.docker.internal:11434
```

If Open WebUI and Ollama are on the same Docker network, use:

```text
http://ollama:11434
```

---

## 17. Troubleshooting

### Problem: `docker` command not found

Make sure Docker Desktop is installed and running.

Close and reopen PowerShell, then run:

```powershell
docker --version
```

---

### Problem: Cannot activate virtual environment

Run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

### Problem: Port 11434 already in use

Check what is using the port:

```powershell
netstat -ano | findstr :11434
```

If another Ollama instance is running locally, stop it or use the existing one.

---

### Problem: Ollama container already exists

Start it:

```powershell
docker start ollama
```

Or recreate it:

```powershell
docker rm -f ollama
docker run -d `
  --name ollama `
  -p 11434:11434 `
  -v ollama:/root/.ollama `
  --restart unless-stopped `
  ollama/ollama
```

---

### Problem: Model not found

Pull the model:

```powershell
docker exec -it ollama ollama pull llama3.1
```

Then verify:

```powershell
docker exec -it ollama ollama list
```

---

### Problem: Notebook cannot connect to Ollama

Check container:

```powershell
docker ps
```

Check API:

```powershell
Invoke-RestMethod http://localhost:11434/api/tags
```

In the notebook, verify:

```python
OLLAMA_BASE_URL = "http://localhost:11434"
```

---

### Problem: Model response is very slow

Use a smaller model:

```powershell
docker exec -it ollama ollama pull mistral
```

Then in the notebook:

```python
MODEL_NAME = "mistral"
```

Also close other heavy applications.

---

## 18. Recommended workshop checklist for Windows participants

Before the workshop, participants should confirm:

```text
[ ] Docker Desktop installed
[ ] Docker Desktop running
[ ] Python 3.10+ installed
[ ] Git installed
[ ] Project folder downloaded or cloned
[ ] Virtual environment created
[ ] Jupyter kernel registered
[ ] Ollama container running
[ ] Model pulled successfully
[ ] Notebook opens
[ ] Kernel set to Python (AI Native Workshop)
[ ] Ollama connectivity test passes
```

---

## 19. Minimal command sequence

For experienced Windows users, this is the short version:

```powershell
git clone https://github.com/mnanos/AI_native_workshop.git
cd AI_native_workshop

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install notebook jupyterlab ipykernel requests pandas matplotlib

python -m ipykernel install --user --name ai-native-workshop --display-name "Python (AI Native Workshop)"

docker run -d `
  --name ollama `
  -p 11434:11434 `
  -v ollama:/root/.ollama `
  --restart unless-stopped `
  ollama/ollama

docker exec -it ollama ollama pull llama3.1

jupyter lab
```

Then open the notebook and select:

```text
Python (AI Native Workshop)
```
