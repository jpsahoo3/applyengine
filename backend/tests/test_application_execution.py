from __future__ import annotations

import unittest

from applyengine.core.database import build_service_container
from applyengine.core.config import Settings
from applyengine.schemas.profile import ResumeParseRequest


class ApplicationExecutionTests(unittest.TestCase):
    def test_execute_applications_and_dashboard_snapshot(self) -> None:
        container = build_service_container(Settings(jwt_secret="test-secret"))
        parse_result = container.profile_service.parse_resume(
            ResumeParseRequest(
                user_id="user-1",
                filename="resume.txt",
                content=(
                    "Python FastAPI Redis Docker Kubernetes AWS engineer with 5 years "
                    "building distributed backend systems."
                ),
            )
        )
        profile = parse_result["profile"]
        container.discovery_service.discover(profile)
        jobs = container.matching_service.match(profile, container.job_repository.list_all())
        result = container.application_service.execute(
            user_id="user-1",
            jobs=jobs,
            optimized_resumes=parse_result["optimized_resumes"],
        )
        applied_jobs = [job for job in jobs if job.id in {item.job_id for item in result["applications"]}]
        container.outreach_service.execute(user_id="user-1", profile=profile, jobs=applied_jobs)
        dashboard = container.dashboard_service.snapshot("user-1")
        self.assertGreaterEqual(dashboard["sections"]["applications_sent"], 1)
        self.assertGreaterEqual(dashboard["sections"]["login_required"], 1)


if __name__ == "__main__":
    unittest.main()
