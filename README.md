# ApplyEngine

ApplyEngine is a monorepo for a distributed AI job-hunting SaaS platform built around FastAPI, LangGraph-style orchestration, Celery workers, Playwright automation, PostgreSQL, Redis, and a Next.js dashboard.

## Repository Layout

- `backend/`: API, orchestration graph, agents, worker tasks, tests
- `frontend/`: Next.js dashboard
- `infra/`: Docker, Kubernetes, and cloud deployment assets
- `docs/`: system diagrams, state machines, and architecture decisions
- `loadtests/`: load generation and throughput validation assets
- `scripts/`: helper scripts for local workflows

## Local Development

Python dependencies are isolated in `backend/.venv`. The backend source package lives in `backend/applyengine`, while the project definition stays at the repo root in `pyproject.toml`.

1. Create the backend virtual environment:

```bash
python -m venv backend/.venv
```

2. Activate it:

```bash
source backend/.venv/bin/activate
```

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

3. Install backend dependencies:

```bash
backend/.venv/bin/python -m pip install -e .[dev]
```

```powershell
.\backend\.venv\Scripts\python.exe -m pip install -e .[dev]
```

4. Run backend tests:

```bash
backend/.venv/bin/python -m unittest discover -s backend/tests -v
```

```powershell
.\backend\.venv\Scripts\python.exe -m unittest discover -s backend\tests -v
```

5. Start the backend bootstrap:

```bash
backend/.venv/bin/python -m applyengine.main
```

```powershell
.\backend\.venv\Scripts\python.exe -m applyengine.main
```

`applyengine.egg-info` is generated packaging metadata created by editable installs. It is not source code and is ignored by git.

## Branch Workflow

- `dev`: active development
- `staging`: pre-production validation
- `main`: production

Development happens on `dev`, stable increments merge into `staging`, and validated releases merge into `main`.
