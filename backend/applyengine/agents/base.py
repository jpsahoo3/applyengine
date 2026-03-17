from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AgentResult:
    agent_name: str
    payload: dict[str, object]

