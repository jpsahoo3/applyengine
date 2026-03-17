from __future__ import annotations

from applyengine.agents.base import AgentResult
from applyengine.schemas.job import JobRecord


class RecruiterFinderAgent:
    agent_name = "recruiter_finder"

    def find(self, job: JobRecord) -> AgentResult:
        domain = job.company.lower().replace(" ", "") + ".example.com"
        recruiters = [
            {
                "company": job.company,
                "name": f"{job.company} Talent Team",
                "email": f"recruiting@{domain}",
                "linkedin_url": f"https://linkedin.com/company/{job.company.lower().replace(' ', '-')}",
            }
        ]
        return AgentResult(agent_name=self.agent_name, payload={"recruiters": recruiters})

