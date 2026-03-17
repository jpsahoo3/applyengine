from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ApplicationRecord:
    job_id: str
    company: str
    title: str
    source: str
    status: str
    resume_variant: str

