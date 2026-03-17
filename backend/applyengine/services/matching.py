from __future__ import annotations

from applyengine.agents.job_matching import JobMatchingAgent
from applyengine.core.telemetry import MetricsRegistry
from applyengine.schemas.job import JobRecord
from applyengine.schemas.profile import ProfileSnapshot


class MatchingService:
    def __init__(self, *, metrics: MetricsRegistry, matcher: JobMatchingAgent) -> None:
        self.metrics = metrics
        self.matcher = matcher

    def match(self, profile: ProfileSnapshot, jobs: list[JobRecord]) -> list[JobRecord]:
        matched = self.matcher.match(profile, jobs).payload["jobs"]
        results = list(matched) if isinstance(matched, list) else []
        self.metrics.increment("jobs.match.success", len(results))
        return results

