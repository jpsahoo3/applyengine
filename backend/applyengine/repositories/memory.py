from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from applyengine.db.models import Profile, Resume, User
from applyengine.schemas.job import JobRecord


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users_by_id: dict[str, User] = {}
        self._users_by_email: dict[str, User] = {}

    def create(self, user: User) -> User:
        stored = replace(user)
        self._users_by_id[stored.id] = stored
        self._users_by_email[stored.email.lower()] = stored
        return replace(stored)

    def get_by_email(self, email: str) -> User | None:
        found = self._users_by_email.get(email.lower())
        return replace(found) if found else None

    def list_all(self) -> Iterable[User]:
        return [replace(user) for user in self._users_by_id.values()]


class InMemoryProfileRepository:
    def __init__(self) -> None:
        self._profiles_by_user_id: dict[str, Profile] = {}

    def upsert(self, profile: Profile) -> Profile:
        stored = replace(profile)
        self._profiles_by_user_id[stored.user_id] = stored
        return replace(stored)

    def get_by_user_id(self, user_id: str) -> Profile | None:
        found = self._profiles_by_user_id.get(user_id)
        return replace(found) if found else None


class InMemoryResumeRepository:
    def __init__(self) -> None:
        self._resumes_by_id: dict[str, Resume] = {}

    def create(self, resume: Resume) -> Resume:
        stored = replace(resume)
        self._resumes_by_id[stored.id] = stored
        return replace(stored)

    def list_all(self) -> Iterable[Resume]:
        return [replace(resume) for resume in self._resumes_by_id.values()]


class InMemoryJobRepository:
    def __init__(self) -> None:
        self._jobs_by_fingerprint: dict[str, JobRecord] = {}

    @staticmethod
    def _fingerprint(job: JobRecord) -> str:
        return f"{job.source}|{job.company.lower()}|{job.title.lower()}|{job.apply_url.lower()}"

    def upsert_many(self, jobs: Iterable[JobRecord]) -> list[JobRecord]:
        stored_jobs: list[JobRecord] = []
        for job in jobs:
            fingerprint = self._fingerprint(job)
            self._jobs_by_fingerprint[fingerprint] = replace(job)
            stored_jobs.append(replace(self._jobs_by_fingerprint[fingerprint]))
        return stored_jobs

    def list_all(self) -> list[JobRecord]:
        return [replace(job) for job in self._jobs_by_fingerprint.values()]
