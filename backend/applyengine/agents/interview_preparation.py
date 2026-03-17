from __future__ import annotations

from applyengine.agents.base import AgentResult
from applyengine.schemas.job import JobRecord
from applyengine.schemas.profile import ProfileSnapshot


class InterviewPreparationAgent:
    agent_name = "interview_preparation"

    def prepare(self, job: JobRecord, profile: ProfileSnapshot) -> AgentResult:
        brief = {
            "company": job.company,
            "role": job.title,
            "behavioral": [f"Explain impact delivering {skill} systems." for skill in profile.skills[:3]],
            "technical": [f"Review architecture topics related to {skill}." for skill in job.skills[:3]],
        }
        return AgentResult(agent_name=self.agent_name, payload={"brief": brief})

