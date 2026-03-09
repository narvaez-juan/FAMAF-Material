# Backend setup and running

## Clone the repository
```bash
git clone https://github.com/IngSoft1-pseudoIngenieros/backend.git
# Change directory to the cloned repo folder
cd backend
```
This will create a local copy of the backend project and move into the backend folder.

## Steps to run the backend on Linux Ubuntu (Bash)

These instructions assume you are on Linux Ubuntu and using Bash.

1) Create and activate a virtual environment (recommended)

```bash
# From the `backend` folder (or wherever you want the venv)
python3 -m venv .venv
# Activate the virtual environment in PowerShell
source .venv/bin/activate
```

2) Update pip

```bash
python -m pip install --upgrade pip
```

3) Install dependencies

If there is a `requirements.txt` in the `backend` folder, install dependencies with:

```bash
pip install -r requirements.txt
```

If you want to install FastAPI with recommended extras:

```bash
pip install "fastapi[standard]"
```

4) Run the application

Change into the `src` folder and run:

```bash
cd src
python main.py
```

Using Uvicorn for development:

```bash
cd src
pip install uvicorn
uvicorn --host 0.0.0.0 --port 8000 --reload main:app
```

5) Run tests

First make sure you are on the backend folder, where you can visualize src and test folders

Run all tests

```bash
python -m pytest
```

Run tests from a single file
```bash
# Run single file test example
python -m pytest test/some_test_file.py
```

If you want to run seeing the coverage
```bash
pip install pytest pytest-cov
python -m pytest --cov=src --cov-report=html
# Visualization
firefox htmlcov/index.html
```

## Steps to run the backend on Windows (PowerShell)

These instructions assume you are on Windows and using PowerShell.

1) Create and activate a virtual environment (recommended)

```powershell
# From the `backend` folder (or wherever you want the venv)
python -m venv .venv
# Activate the virtual environment in PowerShell
.\.venv\Scripts\Activate.ps1
```

2) Update pip

```powershell
python -m pip install --upgrade pip
```

3) Install dependencies

If there is a `requirements.txt` in the `backend` folder, install dependencies with:

```powershell
pip install -r requirements.txt
```

If you want to install FastAPI with recommended extras:

```powershell
pip install "fastapi[standard]"
```

4) Run the application

Change into the `src` folder and run:

```powershell
cd src
python main.py
```

Using Uvicorn for development:

```powershell
cd src
pip install uvicorn
uvicorn --host 0.0.0.0 --port 8000 --reload main:app
```

5) Run tests

Run all tests

```powershell
pytest
```

Run tests from a single file
```powershell
# Run single file test example
pytest test/some_test_file.py
```

If you want to run seeing the coverage
```bash
pip install pytest pytest-cov
pytest --cov=src --cov-report=html
# Visualization
firefox htmlcov/index.html
```
