from __future__ import annotations

import secrets
from dataclasses import dataclass, field


SCRAPING_QUEUE = "scraping"
MATCHING_QUEUE = "matching"
APPLICATION_QUEUE = "application"
OUTREACH_QUEUE = "outreach"


@dataclass(slots=True)
class TaskEnvelope:
    queue: str
    task_name: str
    payload: dict[str, object]
    task_id: str = field(default_factory=lambda: secrets.token_hex(8))
    status: str = "queued"


class QueueManager:
    def __init__(self) -> None:
        self._queues: dict[str, list[TaskEnvelope]] = {
            SCRAPING_QUEUE: [],
            MATCHING_QUEUE: [],
            APPLICATION_QUEUE: [],
            OUTREACH_QUEUE: [],
        }

    def enqueue(self, queue: str, task_name: str, payload: dict[str, object]) -> TaskEnvelope:
        envelope = TaskEnvelope(queue=queue, task_name=task_name, payload=payload)
        self._queues[queue].append(envelope)
        return envelope

    def dequeue(self, queue: str) -> TaskEnvelope | None:
        if not self._queues[queue]:
            return None
        envelope = self._queues[queue].pop(0)
        envelope.status = "processing"
        return envelope

    def snapshot(self) -> dict[str, int]:
        return {queue: len(items) for queue, items in self._queues.items()}

