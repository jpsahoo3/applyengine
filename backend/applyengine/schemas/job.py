from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class JobRecord:
    id: str
    source: str
    title: str
    company: str
    location: str
    description: str
    apply_url: str
    login_required: bool = False
    skills: list[str] = field(default_factory=list)
    semantic_score: float = 0.0

