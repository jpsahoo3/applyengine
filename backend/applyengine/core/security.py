from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from datetime import UTC, datetime, timedelta

from applyengine.core.config import Settings


def hash_password(password: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120_000)
    return f"{salt}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    salt, _separator, _digest = encoded.partition("$")
    return hmac.compare_digest(hash_password(password, salt), encoded)


def create_access_token(subject: str, settings: Settings, ttl_minutes: int | None = None) -> str:
    issued_at = datetime.now(tz=UTC)
    expires_at = issued_at + timedelta(minutes=ttl_minutes or settings.access_token_ttl_minutes)
    payload = {
        "sub": subject,
        "aud": settings.jwt_audience,
        "iss": settings.jwt_issuer,
        "iat": issued_at.isoformat(),
        "exp": expires_at.isoformat(),
    }
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
    signature = hmac.new(
        settings.jwt_secret.encode("utf-8"),
        encoded_payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{encoded_payload}.{signature}"

