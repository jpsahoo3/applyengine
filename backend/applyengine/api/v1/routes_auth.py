from __future__ import annotations

from applyengine.api.spec import ApiSpec, RouteSpec
from applyengine.core.database import ServiceContainer
from applyengine.schemas.auth import LoginRequest, SignupRequest


def register_auth_routes(api: ApiSpec, container: ServiceContainer) -> None:
    auth = container.auth_service

    def signup(payload: SignupRequest) -> dict[str, object]:
        return auth.signup(payload)

    def login(payload: LoginRequest) -> dict[str, object]:
        return auth.login(payload)

    api.add(
        RouteSpec(method="POST", path="/api/v1/auth/signup", name="signup", handler=signup),
        RouteSpec(method="POST", path="/api/v1/auth/login", name="login", handler=login),
    )
