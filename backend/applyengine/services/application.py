from __future__ import annotations

import secrets
from datetime import UTC, datetime

from applyengine.agents.application_tracking import ApplicationTrackingAgent
from applyengine.agents.login_detection import LoginDetectionAgent
from applyengine.agents.mass_application import MassApplicationAgent
from applyengine.core.telemetry import MetricsRegistry
from applyengine.db.models import Application
from applyengine.repositories.memory import InMemoryApplicationRepository
from applyengine.schemas.application import ApplicationRecord
from applyengine.schemas.job import JobRecord


class ApplicationService:
    def __init__(
        self,
        *,
        metrics: MetricsRegistry,
        repository: InMemoryApplicationRepository,
        login_detection: LoginDetectionAgent,
        application_agent: MassApplicationAgent,
        tracking_agent: ApplicationTrackingAgent,
    ) -> None:
        self.metrics = metrics
        self.repository = repository
        self.login_detection = login_detection
        self.application_agent = application_agent
        self.tracking_agent = tracking_agent

    def execute(
        self,
        *,
        user_id: str,
        jobs: list[JobRecord],
        optimized_resumes: dict[str, dict[str, object]],
    ) -> dict[str, object]:
        applied_records: list[ApplicationRecord] = []
        login_required_jobs: list[JobRecord] = []
        for job in jobs:
            requires_login = self.login_detection.evaluate(job).payload["requires_login"]
            if requires_login:
                self.repository.create(
                    Application(
                        id=secrets.token_hex(16),
                        user_id=user_id,
                        job_id=job.id,
                        status="login_required",
                    )
                )
                login_required_jobs.append(job)
                continue
            application = self.application_agent.apply(job, optimized_resumes).payload["application"]
            if isinstance(application, ApplicationRecord):
                applied_records.append(application)
                self.repository.create(
                    Application(
                        id=secrets.token_hex(16),
                        user_id=user_id,
                        job_id=job.id,
                        status="applied",
                        applied_at=datetime.now(tz=UTC),
                    )
                )
        summary = self.tracking_agent.summarize(applied_records, login_required_jobs).payload["summary"]
        self.metrics.increment("applications.execute.success", len(applied_records))
        return {
            "applications": applied_records,
            "login_required": login_required_jobs,
            "summary": summary if isinstance(summary, dict) else {},
        }

    def list_for_user(self, user_id: str) -> list[Application]:
        return self.repository.list_by_user_id(user_id)

