from __future__ import annotations

import secrets

from applyengine.agents.base import AgentResult
from applyengine.schemas.job import JobRecord
from applyengine.schemas.profile import ProfileSnapshot


class JobDiscoveryAgent:
    agent_name = "job_discovery"

    def discover(self, profile: ProfileSnapshot, seed_jobs: list[JobRecord] | None = None) -> AgentResult:
        if seed_jobs is not None:
            return AgentResult(agent_name=self.agent_name, payload={"jobs": seed_jobs})
        jobs = [
            JobRecord(
                id=secrets.token_hex(8),
                source="linkedin",
                title=f"{profile.target_roles[0].title()} Engineer",
                company="Acme Cloud",
                location="Remote",
                description=f"Looking for {', '.join(profile.skills[:5])} experience.",
                apply_url="https://jobs.example.com/acme/apply",
                skills=profile.skills[:5],
                login_required=False,
            ),
            JobRecord(
                id=secrets.token_hex(8),
                source="workday",
                title=f"Senior {profile.target_roles[0].title()} Engineer",
                company="Orbit Systems",
                location="Bengaluru",
                description=f"Scale systems with {', '.join(profile.skills[:4])}.",
                apply_url="https://jobs.example.com/orbit/login",
                skills=profile.skills[:4],
                login_required=True,
            ),
        ]
        return AgentResult(agent_name=self.agent_name, payload={"jobs": jobs})

