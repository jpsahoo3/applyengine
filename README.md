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

1. Create and activate the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install backend dependencies:

```powershell
.\.venv\Scripts\python -m pip install -e .[dev]
```

3. Run backend tests:

```powershell
.\.venv\Scripts\python -m pytest backend/tests
```

4. Start the API:

```powershell
.\.venv\Scripts\python -m applyengine.main
```

## Branch Workflow

- `dev`: active development
- `staging`: pre-production validation
- `main`: production

Development happens on `dev`, stable increments merge into `staging`, and validated releases merge into `main`.

