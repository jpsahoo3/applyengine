from __future__ import annotations

from applyengine.agents.base import AgentResult
from applyengine.schemas.job import JobRecord


class LoginDetectionAgent:
    agent_name = "login_detection"

    def evaluate(self, job: JobRecord) -> AgentResult:
        requires_login = job.login_required or "login" in job.apply_url.lower()
        return AgentResult(
            agent_name=self.agent_name,
            payload={"requires_login": requires_login, "job": job},
        )

