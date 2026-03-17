from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field


@dataclass(slots=True)
class MetricsRegistry:
    counters: Counter[str] = field(default_factory=Counter)

    def increment(self, metric: str, value: int = 1) -> None:
        self.counters[metric] += value

    def snapshot(self) -> dict[str, int]:
        return dict(self.counters)

