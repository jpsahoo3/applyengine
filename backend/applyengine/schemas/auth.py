from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SignupRequest:
    email: str
    password: str
    full_name: str


@dataclass(slots=True)
class LoginRequest:
    email: str
    password: str

