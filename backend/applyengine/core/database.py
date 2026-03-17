from __future__ import annotations

from dataclasses import dataclass

from applyengine.core.config import Settings
from applyengine.core.telemetry import MetricsRegistry
from applyengine.repositories.memory import InMemoryUserRepository
from applyengine.services.auth import AuthService


@dataclass(slots=True)
class ServiceContainer:
    settings: Settings
    metrics: MetricsRegistry
    user_repository: InMemoryUserRepository
    auth_service: AuthService


def build_service_container(settings: Settings) -> ServiceContainer:
    metrics = MetricsRegistry()
    user_repository = InMemoryUserRepository()
    auth_service = AuthService(settings=settings, metrics=metrics, users=user_repository)
    return ServiceContainer(
        settings=settings,
        metrics=metrics,
        user_repository=user_repository,
        auth_service=auth_service,
    )

