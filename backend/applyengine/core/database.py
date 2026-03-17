from __future__ import annotations

from dataclasses import dataclass

from applyengine.agents.job_matching import JobMatchingAgent
from applyengine.agents.profile_analyzer import ProfileAnalyzerAgent
from applyengine.agents.resume_optimizer import ResumeOptimizerAgent
from applyengine.core.celery_app import QueueManager
from applyengine.core.config import Settings
from applyengine.core.telemetry import MetricsRegistry
from applyengine.repositories.memory import (
    InMemoryJobRepository,
    InMemoryProfileRepository,
    InMemoryResumeRepository,
    InMemoryUserRepository,
)
from applyengine.services.auth import AuthService
from applyengine.services.discovery import DistributedScrapingEngine, JobDiscoveryService
from applyengine.services.matching import MatchingService
from applyengine.services.orchestration import OrchestrationService
from applyengine.services.profile import ProfileService
from applyengine.services.storage import LocalObjectStore


@dataclass(slots=True)
class ServiceContainer:
    settings: Settings
    metrics: MetricsRegistry
    user_repository: InMemoryUserRepository
    job_repository: InMemoryJobRepository
    profile_repository: InMemoryProfileRepository
    resume_repository: InMemoryResumeRepository
    object_store: LocalObjectStore
    queue_manager: QueueManager
    auth_service: AuthService
    profile_service: ProfileService
    discovery_service: JobDiscoveryService
    matching_service: MatchingService
    orchestration_service: OrchestrationService


def build_service_container(settings: Settings) -> ServiceContainer:
    metrics = MetricsRegistry()
    user_repository = InMemoryUserRepository()
    job_repository = InMemoryJobRepository()
    profile_repository = InMemoryProfileRepository()
    resume_repository = InMemoryResumeRepository()
    object_store = LocalObjectStore()
    queue_manager = QueueManager()
    auth_service = AuthService(settings=settings, metrics=metrics, users=user_repository)
    profile_service = ProfileService(
        metrics=metrics,
        profiles=profile_repository,
        resumes=resume_repository,
        object_store=object_store,
        profile_analyzer=ProfileAnalyzerAgent(),
        resume_optimizer=ResumeOptimizerAgent(),
    )
    discovery_service = JobDiscoveryService(
        metrics=metrics,
        repository=job_repository,
        engine=DistributedScrapingEngine(),
    )
    matching_service = MatchingService(metrics=metrics, matcher=JobMatchingAgent())
    orchestration_service = OrchestrationService()
    return ServiceContainer(
        settings=settings,
        metrics=metrics,
        user_repository=user_repository,
        job_repository=job_repository,
        profile_repository=profile_repository,
        resume_repository=resume_repository,
        object_store=object_store,
        queue_manager=queue_manager,
        auth_service=auth_service,
        profile_service=profile_service,
        discovery_service=discovery_service,
        matching_service=matching_service,
        orchestration_service=orchestration_service,
    )
