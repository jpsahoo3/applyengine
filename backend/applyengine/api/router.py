from __future__ import annotations

from applyengine.api.v1.routes_auth import register_auth_routes
from applyengine.api.v1.routes_health import register_health_routes
from applyengine.api.v1.routes_jobs import register_job_routes
from applyengine.api.v1.routes_profiles import register_profile_routes
from applyengine.api.v1.routes_workflow import register_workflow_routes
from applyengine.api.spec import ApiSpec
from applyengine.core.database import ServiceContainer


def build_api_spec(container: ServiceContainer) -> ApiSpec:
    api = ApiSpec(version="v1", title="ApplyEngine API")
    register_health_routes(api, container)
    register_auth_routes(api, container)
    register_profile_routes(api, container)
    register_job_routes(api, container)
    register_workflow_routes(api, container)
    return api
