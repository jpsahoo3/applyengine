from __future__ import annotations

import secrets

from applyengine.agents.profile_analyzer import ProfileAnalyzerAgent
from applyengine.agents.resume_optimizer import ResumeOptimizerAgent
from applyengine.core.telemetry import MetricsRegistry
from applyengine.db.models import Profile, Resume
from applyengine.repositories.memory import InMemoryProfileRepository, InMemoryResumeRepository
from applyengine.schemas.profile import ProfileSnapshot, ProfileUpsertRequest, ResumeParseRequest
from applyengine.services.storage import LocalObjectStore


class ProfileService:
    def __init__(
        self,
        *,
        metrics: MetricsRegistry,
        profiles: InMemoryProfileRepository,
        resumes: InMemoryResumeRepository,
        object_store: LocalObjectStore,
        profile_analyzer: ProfileAnalyzerAgent,
        resume_optimizer: ResumeOptimizerAgent,
    ) -> None:
        self.metrics = metrics
        self.profiles = profiles
        self.resumes = resumes
        self.object_store = object_store
        self.profile_analyzer = profile_analyzer
        self.resume_optimizer = resume_optimizer

    def onboard_profile(self, request: ProfileUpsertRequest) -> dict[str, object]:
        profile = Profile(
            id=secrets.token_hex(16),
            user_id=request.user_id,
            headline=request.headline,
            target_roles=request.target_roles,
            skills=sorted(set(request.skills)),
            years_experience=request.years_experience,
        )
        stored = self.profiles.upsert(profile)
        self.metrics.increment("profile.onboard.success")
        return {
            "profile_id": stored.id,
            "headline": stored.headline,
            "target_roles": stored.target_roles,
        }

    def parse_resume(self, request: ResumeParseRequest) -> dict[str, object]:
        storage_key = f"resumes/{request.user_id}/{secrets.token_hex(8)}-{request.filename}"
        self.object_store.put_text(storage_key, request.content)
        resume = Resume(
            id=secrets.token_hex(16),
            user_id=request.user_id,
            storage_key=storage_key,
            source_filename=request.filename,
            parsed_text=request.content,
        )
        stored_resume = self.resumes.create(resume)
        profile_payload = self.profile_analyzer.analyze_resume(request.content).payload["profile"]
        if not isinstance(profile_payload, ProfileSnapshot):
            raise TypeError("Profile analyzer returned an invalid payload")
        optimized = self.resume_optimizer.optimize(profile_payload).payload["variants"]
        profile = Profile(
            id=secrets.token_hex(16),
            user_id=request.user_id,
            headline=profile_payload.headline,
            target_roles=profile_payload.target_roles,
            skills=profile_payload.skills,
            years_experience=profile_payload.years_experience,
        )
        stored_profile = self.profiles.upsert(profile)
        self.metrics.increment("profile.resume.parse.success")
        return {
            "resume_id": stored_resume.id,
            "storage_key": stored_resume.storage_key,
            "profile_id": stored_profile.id,
            "profile": profile_payload,
            "optimized_resumes": optimized,
        }

    def get_profile(self, user_id: str) -> dict[str, object]:
        profile = self.profiles.get_by_user_id(user_id)
        if not profile:
            raise LookupError("Profile not found")
        return {
            "profile_id": profile.id,
            "headline": profile.headline,
            "target_roles": profile.target_roles,
            "skills": profile.skills,
            "years_experience": profile.years_experience,
        }

