from __future__ import annotations

from applyengine.api.spec import ApiSpec, RouteSpec
from applyengine.core.database import ServiceContainer


def register_workflow_routes(api: ApiSpec, container: ServiceContainer) -> None:
    orchestration = container.orchestration_service
    profile_service = container.profile_service

    def run_workflow(user_id: str) -> dict[str, object]:
        profile_payload = profile_service.get_profile(user_id)
        profile = profile_service.profiles.get_by_user_id(user_id)
        if not profile:
            raise LookupError("Profile not found")
        return orchestration.run(
            user_id=user_id,
            profile=profile_payload_to_snapshot(profile_payload),
        )

    def graph_state_machine() -> dict[str, object]:
        return orchestration.graph.state_machine()

    api.add(
        RouteSpec(method="POST", path="/api/v1/workflows/{user_id}/run", name="workflow_run", handler=run_workflow),
        RouteSpec(
            method="GET",
            path="/api/v1/workflows/state-machine",
            name="workflow_state_machine",
            handler=graph_state_machine,
        ),
    )


def profile_payload_to_snapshot(profile_payload: dict[str, object]):
    from applyengine.schemas.profile import ProfileSnapshot

    return ProfileSnapshot(
        headline=str(profile_payload["headline"]),
        target_roles=list(profile_payload["target_roles"]),
        skills=list(profile_payload["skills"]),
        years_experience=int(profile_payload["years_experience"]),
        resume_summary=f"{profile_payload['headline']} profile ready for orchestration.",
    )
