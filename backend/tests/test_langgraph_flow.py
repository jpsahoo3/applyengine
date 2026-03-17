from __future__ import annotations

import unittest

from applyengine.graphs.orchestration import JobHuntingGraph
from applyengine.graphs.state import WorkflowState
from applyengine.schemas.job import JobRecord
from applyengine.schemas.profile import ProfileSnapshot


class LangGraphFlowTests(unittest.TestCase):
    def test_workflow_routes_applyable_and_login_required_jobs(self) -> None:
        graph = JobHuntingGraph()
        state = WorkflowState(
            user_id="user-1",
            profile=ProfileSnapshot(
                headline="Backend engineer focused on python, fastapi, redis",
                target_roles=["backend", "ai"],
                skills=["python", "fastapi", "redis", "langgraph"],
                years_experience=5,
                resume_summary="5 years building Python and AI workflows.",
            ),
        )
        seed_jobs = [
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
                description="LangGraph Python",
                apply_url="https://jobs.example.com/login",
                skills=["python", "langgraph"],
                login_required=True,
            ),
        ]
        result = graph.run(state, seed_jobs=seed_jobs)
        self.assertEqual(len(result.applications), 1)
        self.assertEqual(len(result.dashboard_queue), 1)
        self.assertEqual(result.tracking_summary["applied"], 1)
        self.assertEqual(result.tracking_summary["login_required"], 1)


if __name__ == "__main__":
    unittest.main()
