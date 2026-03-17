from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from applyengine.db.models import User


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

