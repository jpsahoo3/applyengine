from __future__ import annotations

from applyengine.agents.base import AgentResult
from applyengine.schemas.job import JobRecord
from applyengine.schemas.profile import ProfileSnapshot


class JobMatchingAgent:
    agent_name = "job_matching"

    def match(self, profile: ProfileSnapshot, jobs: list[JobRecord]) -> AgentResult:
        scored_jobs: list[JobRecord] = []
        profile_skills = {skill.lower() for skill in profile.skills}
        for job in jobs:
            overlap = profile_skills.intersection({skill.lower() for skill in job.skills})
            score = len(overlap) / max(1, len(profile_skills))
            job.semantic_score = round(score, 3)
            if score >= 0.15:
                scored_jobs.append(job)
        scored_jobs.sort(key=lambda item: item.semantic_score, reverse=True)
        return AgentResult(agent_name=self.agent_name, payload={"jobs": scored_jobs})

