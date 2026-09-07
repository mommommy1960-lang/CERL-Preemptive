import pytest

from cerl_preemptive.capability_tokens import (
    CapabilityError, RevocationRegistry, issue_capability, verify_capability,
)


SECRET = b"x" * 32
POLICY = "sha256:policy-v1"


def token(now=100):
    return issue_capability(
        SECRET, actor="service", scopes=["ledger:read"], policy_hash=POLICY,
        ttl_seconds=60, now=now,
    )


def verify(value, **changes):
    args = dict(
        token=value, secret=SECRET, actor="service",
        required_scope="ledger:read", pinned_policy_hash=POLICY,
        revocations=RevocationRegistry(), now=120,
    )
    args.update(changes)
    return verify_capability(**args)


def test_valid_capability():
    assert verify(token())["actor"] == "service"


@pytest.mark.parametrize("changes", [
    {"actor": "other"},
    {"required_scope": "ledger:write"},
    {"pinned_policy_hash": "sha256:other"},
    {"now": 160},
])
def test_binding_and_expiry_fail_closed(changes):
    with pytest.raises(CapabilityError):
        verify(token(), **changes)


def test_tampering_is_detected():
    value = token()
    with pytest.raises(CapabilityError):
        verify("A" + value[1:])


def test_token_revocation_is_immediate():
    value = token()
    claims = verify(value)
    registry = RevocationRegistry()
    registry.revoke_token(claims["jti"])
    with pytest.raises(CapabilityError):
        verify(value, revocations=registry)


def test_policy_revocation_is_immediate():
    registry = RevocationRegistry()
    registry.revoke_policy(POLICY)
    with pytest.raises(CapabilityError):
        verify(token(), revocations=registry)
