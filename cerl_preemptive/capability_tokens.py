"""Signed, scoped, expiring, revocable consent capabilities."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass, field
from typing import Callable


class CapabilityError(ValueError):
    pass


def _encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _canonical(claims: dict) -> bytes:
    return json.dumps(claims, sort_keys=True, separators=(",", ":")).encode("utf-8")


@dataclass
class RevocationRegistry:
    token_ids: set[str] = field(default_factory=set)
    policy_hashes: set[str] = field(default_factory=set)

    def revoke_token(self, token_id: str) -> None:
        self.token_ids.add(token_id)

    def revoke_policy(self, policy_hash: str) -> None:
        self.policy_hashes.add(policy_hash)


def issue_capability(
    secret: bytes,
    *,
    actor: str,
    scopes: list[str],
    policy_hash: str,
    ttl_seconds: int = 900,
    now: int | None = None,
) -> str:
    if len(secret) < 32:
        raise CapabilityError("signing secret must contain at least 32 bytes")
    if not actor or not scopes or not policy_hash:
        raise CapabilityError("actor, scopes, and policy_hash are required")
    if ttl_seconds <= 0 or ttl_seconds > 86400:
        raise CapabilityError("ttl_seconds must be between 1 and 86400")
    issued = int(time.time() if now is None else now)
    claims = {
        "jti": secrets.token_urlsafe(18),
        "actor": actor,
        "scopes": sorted(set(scopes)),
        "policy_hash": policy_hash,
        "iat": issued,
        "exp": issued + ttl_seconds,
    }
    payload = _encode(_canonical(claims))
    signature = _encode(hmac.new(secret, payload.encode("ascii"), hashlib.sha256).digest())
    return payload + "." + signature


def verify_capability(
    token: str,
    secret: bytes,
    *,
    actor: str,
    required_scope: str,
    pinned_policy_hash: str,
    revocations: RevocationRegistry,
    now: int | None = None,
) -> dict:
    try:
        payload, encoded_signature = token.split(".", 1)
        signature = _decode(encoded_signature)
        expected = hmac.new(secret, payload.encode("ascii"), hashlib.sha256).digest()
        if not hmac.compare_digest(signature, expected):
            raise CapabilityError("invalid capability signature")
        claims = json.loads(_decode(payload))
    except (ValueError, json.JSONDecodeError) as exc:
        if isinstance(exc, CapabilityError):
            raise
        raise CapabilityError("malformed capability") from exc

    current = int(time.time() if now is None else now)
    if current >= int(claims.get("exp", 0)):
        raise CapabilityError("capability expired")
    if claims.get("actor") != actor:
        raise CapabilityError("actor mismatch")
    if required_scope not in claims.get("scopes", []):
        raise CapabilityError("scope denied")
    if claims.get("policy_hash") != pinned_policy_hash:
        raise CapabilityError("policy pin mismatch")
    if claims.get("jti") in revocations.token_ids:
        raise CapabilityError("capability revoked")
    if pinned_policy_hash in revocations.policy_hashes:
        raise CapabilityError("policy revoked")
    return claims
