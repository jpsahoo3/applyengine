from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any

from applyengine.api.router import build_api_spec
from applyengine.core.config import Settings, get_settings
from applyengine.core.database import ServiceContainer, build_service_container
from applyengine.core.logging import configure_logging, get_logger


logger = get_logger(__name__)


def create_application(
    settings: Settings | None = None, container: ServiceContainer | None = None
) -> dict[str, Any]:
    settings = settings or get_settings()
    configure_logging(settings)
    container = container or build_service_container(settings)
    api_spec = build_api_spec(container)
    return {
        "settings": settings,
        "container": container,
        "api": api_spec,
    }


def run() -> None:
    application = create_application()
    api_spec = application["api"]
    logger.info("boot.completed", extra={"event": "boot.completed", "route_count": len(api_spec.routes)})
    payload = asdict(api_spec) if is_dataclass(api_spec) else api_spec
    print(json.dumps(payload, indent=2, default=str))


if __name__ == "__main__":
    run()
