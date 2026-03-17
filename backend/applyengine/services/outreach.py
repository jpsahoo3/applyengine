from __future__ import annotations

import secrets

from applyengine.agents.cold_outreach import ColdOutreachAgent
from applyengine.agents.linkedin_networking import LinkedInNetworkingAgent
from applyengine.agents.recruiter_finder import RecruiterFinderAgent
from applyengine.core.telemetry import MetricsRegistry
from applyengine.db.models import OutreachMessage, Recruiter
from applyengine.repositories.memory import InMemoryOutreachRepository, InMemoryRecruiterRepository
from applyengine.schemas.job import JobRecord
from applyengine.schemas.profile import ProfileSnapshot


class OutreachService:
    def __init__(
        self,
        *,
        metrics: MetricsRegistry,
        recruiter_repository: InMemoryRecruiterRepository,
        outreach_repository: InMemoryOutreachRepository,
        recruiter_finder: RecruiterFinderAgent,
        cold_outreach: ColdOutreachAgent,
        linkedin_networking: LinkedInNetworkingAgent,
    ) -> None:
        self.metrics = metrics
        self.recruiter_repository = recruiter_repository
        self.outreach_repository = outreach_repository
        self.recruiter_finder = recruiter_finder
        self.cold_outreach = cold_outreach
        self.linkedin_networking = linkedin_networking

    def execute(
        self,
        *,
        user_id: str,
        profile: ProfileSnapshot,
        jobs: list[JobRecord],
    ) -> dict[str, object]:
        stored_recruiters: list[Recruiter] = []
        stored_messages: list[OutreachMessage] = []
        networking_actions: list[dict[str, str]] = []
        for job in jobs:
            recruiter_payload = self.recruiter_finder.find(job).payload["recruiters"]
            recruiters = [
                Recruiter(
                    id=secrets.token_hex(16),
                    company=item["company"],
                    full_name=item["name"],
                    email=item["email"],
                    linkedin_url=item["linkedin_url"],
                )
                for item in recruiter_payload
            ]
            stored_recruiters.extend(self.recruiter_repository.upsert_many(recruiters))
            messages = self.cold_outreach.compose(job, recruiter_payload, profile).payload["messages"]
            message_models = [
                OutreachMessage(
                    id=secrets.token_hex(16),
                    recruiter_id=recruiters[index].id,
                    user_id=user_id,
                    channel=message["channel"],
                    subject=message["subject"],
                    body=message["body"],
                    status="queued",
                )
                for index, message in enumerate(messages)
            ]
            stored_messages.extend(self.outreach_repository.create_many(message_models))
            actions = self.linkedin_networking.build_actions(job, recruiter_payload).payload["actions"]
            if isinstance(actions, list):
                networking_actions.extend(actions)
        self.metrics.increment("outreach.execute.success", len(stored_messages))
        return {
            "recruiters": stored_recruiters,
            "messages": stored_messages,
            "networking_actions": networking_actions,
        }

    def list_messages(self, user_id: str) -> list[OutreachMessage]:
        return self.outreach_repository.list_by_user_id(user_id)

