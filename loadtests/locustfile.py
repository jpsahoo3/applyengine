from __future__ import annotations

from locust import HttpUser, between, task


class ApplyEngineUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def dashboard(self) -> None:
        self.client.get("/api/v1/dashboard/demo-user")

    @task(1)
    def execute_applications(self) -> None:
        self.client.post("/api/v1/applications/demo-user/execute")

