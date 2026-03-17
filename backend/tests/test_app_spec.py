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
                "/api/v1/auth/login",
                "/api/v1/auth/signup",
                "/api/v1/health",
                "/api/v1/profiles/onboard",
                "/api/v1/profiles/{user_id}",
                "/api/v1/resumes/parse",
            ],
        )


if __name__ == "__main__":
    unittest.main()
