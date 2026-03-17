from __future__ import annotations

import unittest

from applyengine.core.config import Settings
from applyengine.core.telemetry import MetricsRegistry
from applyengine.repositories.memory import InMemoryUserRepository
from applyengine.schemas.auth import LoginRequest, SignupRequest
from applyengine.services.auth import AuthError, AuthService


class AuthServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = AuthService(
            settings=Settings(jwt_secret="test-secret"),
            metrics=MetricsRegistry(),
            users=InMemoryUserRepository(),
        )

    def test_signup_and_login_round_trip(self) -> None:
        signup = self.service.signup(
            SignupRequest(email="user@example.com", password="secret", full_name="User")
        )
        login = self.service.login(LoginRequest(email="user@example.com", password="secret"))
        self.assertEqual(signup["email"], "user@example.com")
        self.assertEqual(login["email"], "user@example.com")
        self.assertIn("access_token", login)

    def test_duplicate_signup_is_rejected(self) -> None:
        self.service.signup(SignupRequest(email="dup@example.com", password="secret", full_name="Dup"))
        with self.assertRaises(AuthError):
            self.service.signup(
                SignupRequest(email="dup@example.com", password="secret", full_name="Dup")
            )

    def test_invalid_login_is_rejected(self) -> None:
        self.service.signup(
            SignupRequest(email="wrong@example.com", password="secret", full_name="Wrong")
        )
        with self.assertRaises(AuthError):
            self.service.login(LoginRequest(email="wrong@example.com", password="bad"))


if __name__ == "__main__":
    unittest.main()

