from __future__ import annotations

from applyengine.core.celery_app import (
    APPLICATION_QUEUE,
    MATCHING_QUEUE,
    OUTREACH_QUEUE,
    SCRAPING_QUEUE,
    QueueManager,
)
from applyengine.schemas.job import JobRecord
from applyengine.schemas.profile import ProfileSnapshot
from applyengine.services.discovery import JobDiscoveryService
from applyengine.services.matching import MatchingService


def queue_scraping_work(queue: QueueManager, profile: ProfileSnapshot) -> dict[str, object]:
    envelope = queue.enqueue(
        SCRAPING_QUEUE,
        "scrape_jobs",
        {"profile": profile},
    )
    return {"task_id": envelope.task_id, "queue": envelope.queue}


def queue_matching_work(
    queue: QueueManager,
    profile: ProfileSnapshot,
    jobs: list[JobRecord],
) -> dict[str, object]:
    envelope = queue.enqueue(
        MATCHING_QUEUE,
        "match_jobs",
        {"profile": profile, "jobs": jobs},
    )
    return {"task_id": envelope.task_id, "queue": envelope.queue}


def queue_application_work(queue: QueueManager, job: JobRecord) -> dict[str, object]:
    envelope = queue.enqueue(APPLICATION_QUEUE, "apply_job", {"job": job})
    return {"task_id": envelope.task_id, "queue": envelope.queue}


def queue_outreach_work(queue: QueueManager, job: JobRecord) -> dict[str, object]:
    envelope = queue.enqueue(OUTREACH_QUEUE, "outreach_job", {"job": job})
    return {"task_id": envelope.task_id, "queue": envelope.queue}


def run_scraping_task(service: JobDiscoveryService, profile: ProfileSnapshot) -> list[JobRecord]:
    return service.discover(profile)


def run_matching_task(
    service: MatchingService,
    profile: ProfileSnapshot,
    jobs: list[JobRecord],
) -> list[JobRecord]:
    return service.match(profile, jobs)

