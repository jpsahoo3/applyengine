from __future__ import annotations

from applyengine.api.spec import ApiSpec, RouteSpec
from applyengine.core.database import ServiceContainer
from applyengine.schemas.profile import ProfileUpsertRequest, ResumeParseRequest


def register_profile_routes(api: ApiSpec, container: ServiceContainer) -> None:
    profile_service = container.profile_service

    def onboard(payload: ProfileUpsertRequest) -> dict[str, object]:
        return profile_service.onboard_profile(payload)

    def parse_resume(payload: ResumeParseRequest) -> dict[str, object]:
        return profile_service.parse_resume(payload)

    def get_profile(user_id: str) -> dict[str, object]:
        return profile_service.get_profile(user_id)

    api.add(
        RouteSpec(method="POST", path="/api/v1/profiles/onboard", name="profile_onboard", handler=onboard),
        RouteSpec(method="POST", path="/api/v1/resumes/parse", name="resume_parse", handler=parse_resume),
        RouteSpec(method="GET", path="/api/v1/profiles/{user_id}", name="profile_get", handler=get_profile),
    )

