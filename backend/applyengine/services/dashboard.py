from __future__ import annotations

from applyengine.repositories.memory import InMemoryApplicationRepository, InMemoryOutreachRepository


class DashboardService:
    def __init__(
        self,
        *,
        applications: InMemoryApplicationRepository,
        outreach: InMemoryOutreachRepository,
    ) -> None:
        self.applications = applications
        self.outreach = outreach

    def snapshot(self, user_id: str) -> dict[str, object]:
        applications = self.applications.list_by_user_id(user_id)
        outreach = self.outreach.list_by_user_id(user_id)
        applied = [item for item in applications if item.status == "applied"]
        login_required = [item for item in applications if item.status == "login_required"]
        interviews = [item for item in applications if item.status == "interview"]
        recruiter_responses = [item for item in outreach if item.status == "replied"]
        response_rate = round(len(recruiter_responses) / max(1, len(outreach)), 3)
        interview_rate = round(len(interviews) / max(1, len(applied)), 3)
        return {
            "metrics": {
                "applications_per_day": len(applied),
                "response_rate": response_rate,
                "interview_rate": interview_rate,
            },
            "sections": {
                "applications_sent": len(applied),
                "pending": len([item for item in applications if item.status == "pending"]),
                "login_required": len(login_required),
                "interviews": len(interviews),
                "recruiter_responses": len(recruiter_responses),
            },
        }

