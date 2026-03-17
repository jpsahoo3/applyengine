from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


def utc_now() -> datetime:
    return datetime.now(tz=UTC)


@dataclass(slots=True)
class User:
    id: str
    email: str
    password_hash: str
    full_name: str
    created_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class Profile:
    id: str
    user_id: str
    headline: str
    target_roles: list[str]
    skills: list[str]
    years_experience: int
    created_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class Resume:
    id: str
    user_id: str
    storage_key: str
    source_filename: str
    created_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class JobListing:
    id: str
    source: str
    source_job_id: str
    title: str
    company: str
    location: str
    description: str
    apply_url: str
    is_remote: bool
    created_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class Application:
    id: str
    user_id: str
    job_id: str
    status: str
    applied_at: datetime | None = None
    created_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class Recruiter:
    id: str
    company: str
    full_name: str
    email: str
    linkedin_url: str | None = None
    created_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class OutreachMessage:
    id: str
    recruiter_id: str
    user_id: str
    channel: str
    subject: str
    body: str
    status: str
    created_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class AgentLog:
    id: str
    user_id: str
    agent_name: str
    status: str
    message: str
    created_at: datetime = field(default_factory=utc_now)

