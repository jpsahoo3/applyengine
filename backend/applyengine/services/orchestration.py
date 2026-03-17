from __future__ import annotations

from applyengine.graphs.orchestration import JobHuntingGraph
from applyengine.graphs.state import WorkflowState
from applyengine.schemas.job import JobRecord
from applyengine.schemas.profile import ProfileSnapshot


class OrchestrationService:
    def __init__(self, graph: JobHuntingGraph | None = None) -> None:
        self.graph = graph or JobHuntingGraph()

    def run(self, user_id: str, profile: ProfileSnapshot, seed_jobs: list[JobRecord] | None = None) -> dict[str, object]:
        state = WorkflowState(user_id=user_id, profile=profile)
        result = self.graph.run(state, seed_jobs=seed_jobs)
        return self.graph.snapshot(result)

