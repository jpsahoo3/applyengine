from __future__ import annotations

import unittest

from applyengine.main import create_application


class AppSpecTests(unittest.TestCase):
    def test_app_boots_with_routes(self) -> None:
        application = create_application()
        api = application["api"]
        paths = sorted(route.path for route in api.routes)
        self.assertEqual(
            paths,
            [
                "/api/v1/applications/{user_id}/execute",
                "/api/v1/auth/login",
                "/api/v1/auth/signup",
                "/api/v1/dashboard/{user_id}",
                "/api/v1/health",
                "/api/v1/jobs/{user_id}/discover",
                "/api/v1/jobs/{user_id}/match",
                "/api/v1/profiles/onboard",
                "/api/v1/profiles/{user_id}",
                "/api/v1/resumes/parse",
                "/api/v1/workflows/state-machine",
                "/api/v1/workflows/{user_id}/run",
            ],
        )


if __name__ == "__main__":
    unittest.main()
