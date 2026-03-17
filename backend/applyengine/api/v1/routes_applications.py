from __future__ import annotations

from applyengine.api.spec import ApiSpec, RouteSpec
from applyengine.core.database import ServiceContainer
from applyengine.schemas.profile import ProfileSnapshot


def register_application_routes(api: ApiSpec, container: ServiceContainer) -> None:
    applications = container.application_service
    outreach = container.outreach_service
    dashboard = container.dashboard_service

    def execute(user_id: str) -> dict[str, object]:
        profile_model = container.profile_repository.get_by_user_id(user_id)
        if not profile_model:
            raise LookupError("Profile not found")
        profile = ProfileSnapshot(
            headline=profile_model.headline,
            target_roles=profile_model.target_roles,
            skills=profile_model.skills,
            years_experience=profile_model.years_experience,
            resume_summary=f"{profile_model.headline} profile ready for applications.",
        )
        optimized_resumes = container.profile_service.resume_optimizer.optimize(profile).payload["variants"]
        jobs = container.matching_service.match(profile, container.job_repository.list_all())
        result = applications.execute(
            user_id=user_id,
            jobs=jobs,
            optimized_resumes=optimized_resumes if isinstance(optimized_resumes, dict) else {},
        )
        outreach.execute(
            user_id=user_id,
            profile=profile,
            jobs=[job for job in jobs if job.id in {item.job_id for item in result["applications"]}],
        )
        return {"execution": result, "dashboard": dashboard.snapshot(user_id)}

    def list_dashboard(user_id: str) -> dict[str, object]:
        return dashboard.snapshot(user_id)

    api.add(
        RouteSpec(
            method="POST",
            path="/api/v1/applications/{user_id}/execute",
            name="application_execute",
            handler=execute,
        ),
        RouteSpec(
            method="GET",
            path="/api/v1/dashboard/{user_id}",
            name="dashboard_get",
            handler=list_dashboard,
        ),
    )

