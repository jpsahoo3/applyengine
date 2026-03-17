from __future__ import annotations

import secrets
from dataclasses import replace

from applyengine.core.telemetry import MetricsRegistry
from applyengine.repositories.memory import InMemoryJobRepository
from applyengine.schemas.job import JobRecord
from applyengine.schemas.profile import ProfileSnapshot


class BaseJobSourceAdapter:
    source_name = "base"

    def fetch(self, profile: ProfileSnapshot) -> list[JobRecord]:
        return [
            JobRecord(
                id=secrets.token_hex(8),
                source=self.source_name,
                title=f"{profile.target_roles[0].title()} Engineer",
                company=f"{self.source_name.title()} Talent",
                location="Remote",
                description=f"{self.source_name} role aligned to {', '.join(profile.skills[:4])}",
                apply_url=f"https://{self.source_name}.jobs.example.com/apply/{secrets.token_hex(4)}",
                login_required=self.source_name in {"workday", "linkedin"},
                skills=profile.skills[:4],
            )
        ]


class LinkedInAdapter(BaseJobSourceAdapter):
    source_name = "linkedin"


class IndeedAdapter(BaseJobSourceAdapter):
    source_name = "indeed"


class NaukriAdapter(BaseJobSourceAdapter):
    source_name = "naukri"


class WellfoundAdapter(BaseJobSourceAdapter):
    source_name = "wellfound"


class RemoteOkAdapter(BaseJobSourceAdapter):
    source_name = "remoteok"


class GreenhouseAdapter(BaseJobSourceAdapter):
    source_name = "greenhouse"


class LeverAdapter(BaseJobSourceAdapter):
    source_name = "lever"


class WorkdayAdapter(BaseJobSourceAdapter):
    source_name = "workday"


class DistributedScrapingEngine:
    def __init__(self, adapters: list[BaseJobSourceAdapter] | None = None) -> None:
        self.adapters = adapters or [
            LinkedInAdapter(),
            IndeedAdapter(),
            NaukriAdapter(),
            WellfoundAdapter(),
            RemoteOkAdapter(),
            GreenhouseAdapter(),
            LeverAdapter(),
            WorkdayAdapter(),
        ]

    def scrape(self, profile: ProfileSnapshot) -> list[JobRecord]:
        raw_jobs: list[JobRecord] = []
        for adapter in self.adapters:
            raw_jobs.extend(adapter.fetch(profile))
        return self.normalize_and_dedupe(raw_jobs)

    def normalize_and_dedupe(self, jobs: list[JobRecord]) -> list[JobRecord]:
        unique: dict[str, JobRecord] = {}
        for job in jobs:
            normalized = replace(job)
            normalized.title = " ".join(normalized.title.split())
            normalized.company = normalized.company.strip()
            fingerprint = (
                f"{normalized.company.lower()}|{normalized.title.lower()}|{normalized.apply_url.lower()}"
            )
            unique[fingerprint] = normalized
        return list(unique.values())


class JobDiscoveryService:
    def __init__(
        self,
        *,
        metrics: MetricsRegistry,
        repository: InMemoryJobRepository,
        engine: DistributedScrapingEngine,
    ) -> None:
        self.metrics = metrics
        self.repository = repository
        self.engine = engine

    def discover(self, profile: ProfileSnapshot) -> list[JobRecord]:
        jobs = self.engine.scrape(profile)
        stored = self.repository.upsert_many(jobs)
        self.metrics.increment("jobs.discovery.success", len(stored))
        return stored

