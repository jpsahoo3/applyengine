from __future__ import annotations

import json
import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from applyengine.graphs.orchestration import JobHuntingGraph
from applyengine.graphs.state import WorkflowState
from applyengine.schemas.job import JobRecord
from applyengine.schemas.profile import ProfileSnapshot


def main() -> None:
    graph = JobHuntingGraph()
    state = WorkflowState(
        user_id="validation-user",
        profile=ProfileSnapshot(
            headline="Backend engineer",
            target_roles=["backend", "ai"],
            skills=["python", "fastapi", "redis", "langgraph"],
            years_experience=5,
            resume_summary="Validation profile",
        ),
    )
    jobs = [
        JobRecord(
            id="job-1",
            source="linkedin",
            title="Backend Engineer",
            company="Acme",
            location="Remote",
            description="Python FastAPI Redis",
            apply_url="https://jobs.example.com/apply",
            skills=["python", "fastapi", "redis"],
            login_required=False,
        ),
        JobRecord(
            id="job-2",
            source="workday",
            title="AI Engineer",
            company="Orbit",
            location="Remote",
            description="Python LangGraph",
            apply_url="https://jobs.example.com/login",
            skills=["python", "langgraph"],
            login_required=True,
        ),
    ]
    result = graph.run(state, seed_jobs=jobs)
    print(json.dumps(graph.snapshot(result), indent=2, default=str))


if __name__ == "__main__":
    main()

