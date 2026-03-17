from __future__ import annotations

from applyengine.api.spec import ApiSpec, RouteSpec
from applyengine.core.database import ServiceContainer


def register_job_routes(api: ApiSpec, container: ServiceContainer) -> None:
    discovery = container.discovery_service
    matching = container.matching_service
    profiles = container.profile_repository

    def discover(user_id: str) -> dict[str, object]:
        profile = profiles.get_by_user_id(user_id)
        if not profile:
            raise LookupError("Profile not found")
        jobs = discovery.discover(profile)
        return {"count": len(jobs), "jobs": jobs}

    def match(user_id: str) -> dict[str, object]:
        profile = profiles.get_by_user_id(user_id)
        if not profile:
            raise LookupError("Profile not found")
        jobs = container.job_repository.list_all()
        matches = matching.match(profile, jobs)
        return {"count": len(matches), "jobs": matches}

    api.add(
        RouteSpec(method="POST", path="/api/v1/jobs/{user_id}/discover", name="job_discover", handler=discover),
        RouteSpec(method="POST", path="/api/v1/jobs/{user_id}/match", name="job_match", handler=match),
    )

