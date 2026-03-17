from __future__ import annotations

import secrets

from applyengine.core.config import Settings
from applyengine.core.security import create_access_token, hash_password, verify_password
from applyengine.core.telemetry import MetricsRegistry
from applyengine.db.models import User
from applyengine.repositories.memory import InMemoryUserRepository
from applyengine.schemas.auth import LoginRequest, SignupRequest


class AuthError(RuntimeError):
    """Raised when authentication fails."""


class AuthService:
    def __init__(
        self,
        *,
        settings: Settings,
        metrics: MetricsRegistry,
        users: InMemoryUserRepository,
    ) -> None:
        self.settings = settings
        self.metrics = metrics
        self.users = users

    def signup(self, request: SignupRequest) -> dict[str, object]:
        existing = self.users.get_by_email(request.email)
        if existing:
            raise AuthError("User already exists")
        user = User(
            id=secrets.token_hex(16),
            email=request.email.strip().lower(),
            password_hash=hash_password(request.password),
            full_name=request.full_name.strip(),
        )
        stored = self.users.create(user)
        self.metrics.increment("auth.signup.success")
        return {
            "user_id": stored.id,
            "email": stored.email,
            "access_token": create_access_token(stored.id, self.settings),
        }

    def login(self, request: LoginRequest) -> dict[str, object]:
        user = self.users.get_by_email(request.email)
        if not user or not verify_password(request.password, user.password_hash):
            self.metrics.increment("auth.login.failure")
            raise AuthError("Invalid credentials")
        self.metrics.increment("auth.login.success")
        return {
            "user_id": user.id,
            "email": user.email,
            "access_token": create_access_token(user.id, self.settings),
        }

