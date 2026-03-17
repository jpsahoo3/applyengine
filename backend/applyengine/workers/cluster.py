from __future__ import annotations

from dataclasses import dataclass

from applyengine.core.celery_app import (
    APPLICATION_QUEUE,
    MATCHING_QUEUE,
    OUTREACH_QUEUE,
    SCRAPING_QUEUE,
)


@dataclass(frozen=True, slots=True)
class WorkerPool:
    name: str
    queues: tuple[str, ...]
    concurrency_hint: int


SCRAPING_WORKERS = WorkerPool(name="scraping-workers", queues=(SCRAPING_QUEUE,), concurrency_hint=64)
AI_WORKERS = WorkerPool(name="ai-workers", queues=(MATCHING_QUEUE,), concurrency_hint=48)
APPLICATION_WORKERS = WorkerPool(
    name="application-workers", queues=(APPLICATION_QUEUE,), concurrency_hint=128
)
OUTREACH_WORKERS = WorkerPool(name="outreach-workers", queues=(OUTREACH_QUEUE,), concurrency_hint=32)

WORKER_POOLS = [SCRAPING_WORKERS, AI_WORKERS, APPLICATION_WORKERS, OUTREACH_WORKERS]

