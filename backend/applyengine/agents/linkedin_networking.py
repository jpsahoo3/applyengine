from __future__ import annotations

from applyengine.agents.base import AgentResult
from applyengine.schemas.job import JobRecord


class LinkedInNetworkingAgent:
    agent_name = "linkedin_networking"

    def build_actions(self, job: JobRecord, recruiters: list[dict[str, str]]) -> AgentResult:
        actions = [
            {
                "type": "connect",
                "target": recruiter["linkedin_url"],
                "message": f"Applied for {job.title}; would value connecting.",
            }
            for recruiter in recruiters
        ]
        return AgentResult(agent_name=self.agent_name, payload={"actions": actions})

