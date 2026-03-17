from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ResumeParseRequest:
    user_id: str
    filename: str
    content: str


@dataclass(slots=True)
class ProfileUpsertRequest:
    user_id: str
    headline: str
    target_roles: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    years_experience: int = 0


@dataclass(slots=True)
class ProfileSnapshot:
    headline: str
    target_roles: list[str]
    skills: list[str]
    years_experience: int
    resume_summary: str

