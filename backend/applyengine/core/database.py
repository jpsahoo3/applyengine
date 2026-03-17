from __future__ import annotations

from dataclasses import dataclass

from applyengine.agents.application_tracking import ApplicationTrackingAgent
from applyengine.agents.cold_outreach import ColdOutreachAgent
from applyengine.agents.linkedin_networking import LinkedInNetworkingAgent
from applyengine.agents.login_detection import LoginDetectionAgent
from applyengine.agents.mass_application import MassApplicationAgent
from applyengine.agents.job_matching import JobMatchingAgent
from applyengine.agents.profile_analyzer import ProfileAnalyzerAgent
from applyengine.agents.recruiter_finder import RecruiterFinderAgent
from applyengine.agents.resume_optimizer import ResumeOptimizerAgent
from applyengine.core.celery_app import QueueManager
from applyengine.core.config import Settings
from applyengine.core.telemetry import MetricsRegistry
from applyengine.repositories.memory import (
    InMemoryApplicationRepository,
    InMemoryJobRepository,
    InMemoryOutreachRepository,
    InMemoryProfileRepository,
    InMemoryRecruiterRepository,
    InMemoryResumeRepository,
    InMemoryUserRepository,
)
from applyengine.services.application import ApplicationService
from applyengine.services.auth import AuthService
from applyengine.services.dashboard import DashboardService
from applyengine.services.discovery import DistributedScrapingEngine, JobDiscoveryService
from applyengine.services.matching import MatchingService
from applyengine.services.orchestration import OrchestrationService
from applyengine.services.outreach import OutreachService
from applyengine.services.profile import ProfileService
from applyengine.services.storage import LocalObjectStore


@dataclass(slots=True)
class ServiceContainer:
    settings: Settings
    metrics: MetricsRegistry
    user_repository: InMemoryUserRepository
    job_repository: InMemoryJobRepository
    application_repository: InMemoryApplicationRepository
    recruiter_repository: InMemoryRecruiterRepository
    outreach_repository: InMemoryOutreachRepository
    profile_repository: InMemoryProfileRepository
    resume_repository: InMemoryResumeRepository
    object_store: LocalObjectStore
    queue_manager: QueueManager
    auth_service: AuthService
    profile_service: ProfileService
    discovery_service: JobDiscoveryService
    matching_service: MatchingService
    application_service: ApplicationService
    outreach_service: OutreachService
    dashboard_service: DashboardService
    orchestration_service: OrchestrationService


def build_service_container(settings: Settings) -> ServiceContainer:
    metrics = MetricsRegistry()
    user_repository = InMemoryUserRepository()
    job_repository = InMemoryJobRepository()
    application_repository = InMemoryApplicationRepository()
    recruiter_repository = InMemoryRecruiterRepository()
    outreach_repository = InMemoryOutreachRepository()
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
    application_service = ApplicationService(
        metrics=metrics,
        repository=application_repository,
        login_detection=LoginDetectionAgent(),
        application_agent=MassApplicationAgent(),
        tracking_agent=ApplicationTrackingAgent(),
    )
    outreach_service = OutreachService(
        metrics=metrics,
        recruiter_repository=recruiter_repository,
        outreach_repository=outreach_repository,
        recruiter_finder=RecruiterFinderAgent(),
        cold_outreach=ColdOutreachAgent(),
        linkedin_networking=LinkedInNetworkingAgent(),
    )
    dashboard_service = DashboardService(
        applications=application_repository,
        outreach=outreach_repository,
    )
    orchestration_service = OrchestrationService()
    return ServiceContainer(
        settings=settings,
        metrics=metrics,
        user_repository=user_repository,
        job_repository=job_repository,
        application_repository=application_repository,
        recruiter_repository=recruiter_repository,
        outreach_repository=outreach_repository,
        profile_repository=profile_repository,
        resume_repository=resume_repository,
        object_store=object_store,
        queue_manager=queue_manager,
        auth_service=auth_service,
        profile_service=profile_service,
        discovery_service=discovery_service,
        matching_service=matching_service,
        application_service=application_service,
        outreach_service=outreach_service,
        dashboard_service=dashboard_service,
        orchestration_service=orchestration_service,
    )
