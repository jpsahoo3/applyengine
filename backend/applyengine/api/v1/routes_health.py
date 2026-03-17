from __future__ import annotations

from applyengine.api.spec import ApiSpec, RouteSpec
from applyengine.core.database import ServiceContainer


def register_health_routes(api: ApiSpec, container: ServiceContainer) -> None:
    def health() -> dict[str, object]:
        return {
            "status": "ok",
            "service": "applyengine",
            "environment": container.settings.app_env,
            "components": {
                "api": "ready",
                "repository": "ready",
                "auth": "ready",
            },
        }

    api.add(RouteSpec(method="GET", path="/api/v1/health", name="health", handler=health))
