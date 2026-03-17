from __future__ import annotations

import unittest

from applyengine.core.telemetry import MetricsRegistry
from applyengine.repositories.memory import InMemoryProfileRepository, InMemoryResumeRepository
from applyengine.schemas.profile import ResumeParseRequest
from applyengine.services.profile import ProfileService
from applyengine.services.storage import LocalObjectStore
from applyengine.agents.profile_analyzer import ProfileAnalyzerAgent
from applyengine.agents.resume_optimizer import ResumeOptimizerAgent


class ProfilePipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = ProfileService(
            metrics=MetricsRegistry(),
            profiles=InMemoryProfileRepository(),
            resumes=InMemoryResumeRepository(),
            object_store=LocalObjectStore(),
            profile_analyzer=ProfileAnalyzerAgent(),
            resume_optimizer=ResumeOptimizerAgent(),
        )

    def test_resume_parsing_creates_profile_and_variants(self) -> None:
        result = self.service.parse_resume(
            ResumeParseRequest(
                user_id="user-1",
                filename="resume.txt",
                content=(
                    "Senior Python engineer with 6 years experience building FastAPI, PostgreSQL, "
                    "Redis, Docker, Kubernetes, AWS, LangGraph, and React systems."
                ),
            )
        )
        profile = result["profile"]
        self.assertEqual(profile.years_experience, 6)
        self.assertIn("python", profile.skills)
        self.assertIn("backend", profile.target_roles)
        self.assertIn("ai", result["optimized_resumes"])


if __name__ == "__main__":
    unittest.main()
