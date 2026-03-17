from __future__ import annotations

from dataclasses import dataclass, field

from applyengine.schemas.application import ApplicationRecord
from applyengine.schemas.job import JobRecord
from applyengine.schemas.profile import ProfileSnapshot


@dataclass(slots=True)
class WorkflowState:
    user_id: str
    profile: ProfileSnapshot
    optimized_resumes: dict[str, dict[str, object]] = field(default_factory=dict)
    discovered_jobs: list[JobRecord] = field(default_factory=list)
    matched_jobs: list[JobRecord] = field(default_factory=list)
    applications: list[ApplicationRecord] = field(default_factory=list)
    dashboard_queue: list[JobRecord] = field(default_factory=list)
    recruiters: dict[str, list[dict[str, str]]] = field(default_factory=dict)
    outreach_messages: list[dict[str, str]] = field(default_factory=list)
    networking_actions: list[dict[str, str]] = field(default_factory=list)
    interview_briefs: list[dict[str, object]] = field(default_factory=list)
    tracking_summary: dict[str, int] = field(default_factory=dict)
    trace: list[str] = field(default_factory=list)

