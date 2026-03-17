from __future__ import annotations

from dataclasses import dataclass

from applyengine.agents.profile_analyzer import ProfileAnalyzerAgent
from applyengine.agents.resume_optimizer import ResumeOptimizerAgent
from applyengine.core.config import Settings
from applyengine.core.telemetry import MetricsRegistry
from applyengine.repositories.memory import (
    InMemoryProfileRepository,
    InMemoryResumeRepository,
    InMemoryUserRepository,
)
from applyengine.services.auth import AuthService
from applyengine.services.profile import ProfileService
from applyengine.services.storage import LocalObjectStore


@dataclass(slots=True)
class ServiceContainer:
    settings: Settings
    metrics: MetricsRegistry
    user_repository: InMemoryUserRepository
    profile_repository: InMemoryProfileRepository
    resume_repository: InMemoryResumeRepository
    object_store: LocalObjectStore
    auth_service: AuthService
    profile_service: ProfileService


def build_service_container(settings: Settings) -> ServiceContainer:
    metrics = MetricsRegistry()
    user_repository = InMemoryUserRepository()
    profile_repository = InMemoryProfileRepository()
    resume_repository = InMemoryResumeRepository()
    object_store = LocalObjectStore()
    auth_service = AuthService(settings=settings, metrics=metrics, users=user_repository)
    profile_service = ProfileService(
        metrics=metrics,
        profiles=profile_repository,
        resumes=resume_repository,
        object_store=object_store,
        profile_analyzer=ProfileAnalyzerAgent(),
        resume_optimizer=ResumeOptimizerAgent(),
    )
    return ServiceContainer(
        settings=settings,
        metrics=metrics,
        user_repository=user_repository,
        profile_repository=profile_repository,
        resume_repository=resume_repository,
        object_store=object_store,
        auth_service=auth_service,
        profile_service=profile_service,
    )
