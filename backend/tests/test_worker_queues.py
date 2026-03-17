from __future__ import annotations

import unittest

from applyengine.core.celery_app import (
    MATCHING_QUEUE,
    SCRAPING_QUEUE,
    QueueManager,
)
from applyengine.schemas.job import JobRecord
from applyengine.schemas.profile import ProfileSnapshot
from applyengine.services.discovery import DistributedScrapingEngine, JobDiscoveryService
from applyengine.services.matching import MatchingService
from applyengine.core.telemetry import MetricsRegistry
from applyengine.repositories.memory import InMemoryJobRepository
from applyengine.agents.job_matching import JobMatchingAgent
from applyengine.workers.tasks import (
    queue_matching_work,
    queue_scraping_work,
    run_matching_task,
    run_scraping_task,
)


class WorkerQueueTests(unittest.TestCase):
    def test_queue_routing_and_deduplication(self) -> None:
        queue = QueueManager()
        profile = ProfileSnapshot(
            headline="Backend engineer",
            target_roles=["backend"],
            skills=["python", "fastapi", "redis"],
            years_experience=4,
            resume_summary="Backend engineer profile",
        )
        scrape_task = queue_scraping_work(queue, profile)
        self.assertEqual(scrape_task["queue"], SCRAPING_QUEUE)
        match_task = queue_matching_work(queue, profile, [])
        self.assertEqual(match_task["queue"], MATCHING_QUEUE)
        self.assertEqual(queue.snapshot()[SCRAPING_QUEUE], 1)
        self.assertEqual(queue.snapshot()[MATCHING_QUEUE], 1)

        discovery = JobDiscoveryService(
            metrics=MetricsRegistry(),
            repository=InMemoryJobRepository(),
            engine=DistributedScrapingEngine(),
        )
        jobs = run_scraping_task(discovery, profile)
        self.assertGreaterEqual(len(jobs), 8)
        repository = InMemoryJobRepository()
        deduped = repository.upsert_many(
            jobs
            + [
                JobRecord(
                    id=jobs[0].id,
                    source=jobs[0].source,
                    title=jobs[0].title,
                    company=jobs[0].company,
                    location=jobs[0].location,
                    description=jobs[0].description,
                    apply_url=jobs[0].apply_url,
                    login_required=jobs[0].login_required,
                    skills=jobs[0].skills,
                )
            ]
        )
        self.assertEqual(len(repository.list_all()), len(jobs))
        matching = MatchingService(metrics=MetricsRegistry(), matcher=JobMatchingAgent())
        matches = run_matching_task(matching, profile, deduped)
        self.assertGreaterEqual(len(matches), 1)


if __name__ == "__main__":
    unittest.main()
