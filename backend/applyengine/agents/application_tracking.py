from __future__ import annotations

from applyengine.agents.base import AgentResult
from applyengine.schemas.application import ApplicationRecord
from applyengine.schemas.job import JobRecord


class ApplicationTrackingAgent:
    agent_name = "application_tracking"

    def summarize(
        self, applications: list[ApplicationRecord], dashboard_queue: list[JobRecord]
    ) -> AgentResult:
        summary = {
            "applied": len([item for item in applications if item.status == "applied"]),
            "login_required": len(dashboard_queue),
            "pending": len([item for item in applications if item.status == "pending"]),
        }
        return AgentResult(agent_name=self.agent_name, payload={"summary": summary})

