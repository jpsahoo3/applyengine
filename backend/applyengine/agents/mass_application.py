from __future__ import annotations

from applyengine.agents.base import AgentResult
from applyengine.schemas.application import ApplicationRecord
from applyengine.schemas.job import JobRecord


class MassApplicationAgent:
    agent_name = "mass_application"

    def apply(self, job: JobRecord, optimized_resumes: dict[str, dict[str, object]]) -> AgentResult:
        preferred_variant = "backend"
        lowered_title = job.title.lower()
        for variant in optimized_resumes:
            if variant in lowered_title:
                preferred_variant = variant
                break
        application = ApplicationRecord(
            job_id=job.id,
            company=job.company,
            title=job.title,
            source=job.source,
            status="applied",
            resume_variant=preferred_variant,
        )
        return AgentResult(agent_name=self.agent_name, payload={"application": application})

