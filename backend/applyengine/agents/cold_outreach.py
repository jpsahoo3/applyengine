from __future__ import annotations

from applyengine.agents.base import AgentResult
from applyengine.schemas.job import JobRecord
from applyengine.schemas.profile import ProfileSnapshot


class ColdOutreachAgent:
    agent_name = "cold_outreach"

    def compose(self, job: JobRecord, recruiters: list[dict[str, str]], profile: ProfileSnapshot) -> AgentResult:
        messages = []
        for recruiter in recruiters:
            messages.append(
                {
                    "channel": "email",
                    "recipient": recruiter["email"],
                    "subject": f"{profile.headline} | Interest in {job.title}",
                    "body": (
                        f"Hi {recruiter['name']}, I applied for {job.title} at {job.company}. "
                        f"My background spans {', '.join(profile.skills[:5])}."
                    ),
                }
            )
        return AgentResult(agent_name=self.agent_name, payload={"messages": messages})

