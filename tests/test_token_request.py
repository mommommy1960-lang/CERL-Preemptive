import json
from pathlib import Path
import pytest
from cerl_preemptive import consent_token_manager as tokens
from cerl_preemptive import consent_validator as validator


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.setattr(tokens, "TOKENS", tmp_path/"tokens.jsonl")
    events = []
    monkeypatch.setattr(validator, "append_event", lambda **kwargs: events.append(kwargs))
    return validator.ConsentValidator(), events


def test_private_and_ordinary_names_require_stored_scope(setup):
    v, events = setup
    args = dict(action="read", target="customer-record", purpose="support", actor="alice")
    token = tokens.issue_token("alice", v.token_scope("read", "customer-record", "support"), 1)
    assert v.validate_token_request(**args, token_id=token)
    for field, value in [("actor", "bob"), ("target", "another-record"), ("purpose", "marketing"), ("action", "send")]:
        with pytest.raises(validator.ConsentViolationError):
            v.validate_token_request(**{**args, field:value}, token_id=token)
    tokens.revoke_token(token)
    with pytest.raises(validator.ConsentViolationError): v.validate_token_request(**args, token_id=token)
    assert all(token not in json.dumps(e) for e in events)


@pytest.mark.parametrize("hours", [True, float("inf"), float("nan"), "1", 0, -1, 1e308])
def test_invalid_lifetime_cannot_issue(setup, hours):
    with pytest.raises(ValueError): tokens.issue_token("alice", "read", hours)


def test_nonobject_and_nonfinite_records_fail_closed(setup):
    for record in [[], "bad", {"token":"t", "actor":"alice", "scope":"read", "expiry":float("inf")},
                   {"token":"t", "actor":"alice", "scope":"read", "expiry":True}]:
        tokens.TOKENS.write_text(json.dumps(record)+"\n")
        assert not tokens.validate_token("t", "alice", "read")


def test_scope_is_not_ambiguous(setup):
    v, _ = setup
    assert v.token_scope("a:b", "c", "d") != v.token_scope("a", "b:c", "d")
