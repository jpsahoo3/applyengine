from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


Handler = Callable[..., Any]


@dataclass(slots=True)
class RouteSpec:
    method: str
    path: str
    name: str
    handler: Handler


@dataclass(slots=True)
class ApiSpec:
    version: str
    title: str
    routes: list[RouteSpec] = field(default_factory=list)

    def add(self, *routes: RouteSpec) -> None:
        self.routes.extend(routes)

