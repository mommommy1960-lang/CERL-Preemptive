import json
import secrets
import time
from pathlib import Path

TOKENS = Path(__file__).resolve().parents[0] / "tokens.jsonl"

def issue_token(actor: str, scope: str, expiry_hours: int = 24):
    """Create an opaque local prototype token with a short lifetime."""
    if not actor or not scope or expiry_hours <= 0:
        raise ValueError("Actor, scope, and positive expiry are required")
    token_id = secrets.token_urlsafe(32)
    expiry = time.time() + expiry_hours * 3600
    record = {"event": "issue", "token": token_id, "actor": actor, "scope": scope, "expiry": expiry}
    with open(TOKENS, "a", encoding="utf-8") as f:
        json.dump(record, f)
        f.write("\n")
    print(f"[TOKEN] Issued token {token_id[:8]} for {actor} ({scope})")
    return token_id

def revoke_token(token_id: str) -> None:
    """Append a revocation event; an unknown token remains invalid."""
    if not token_id:
        raise ValueError("Token is required")
    with open(TOKENS, "a", encoding="utf-8") as f:
        json.dump({"event": "revoke", "token": token_id}, f)
        f.write("\n")


def validate_token(token_id: str, actor: str | None = None, scope: str | None = None) -> bool:
    """Check the local token ledger, including optional actor and scope binding."""
    if not token_id:
        return False
    now = time.time()
    issued = None
    revoked = False
    try:
        with open(TOKENS, "r", encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                if rec.get("token") != token_id:
                    continue
                if rec.get("event", "issue") == "revoke":
                    revoked = True
                elif rec.get("event", "issue") == "issue":
                    issued = rec
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return False
    return bool(
        issued and not revoked and isinstance(issued.get("expiry"), (int, float))
        and now < issued["expiry"]
        and (actor is None or issued.get("actor") == actor)
        and (scope is None or issued.get("scope") == scope)
    )

if __name__ == "__main__":
    t = issue_token("commons_system", "ledger_write", 1)
    validate_token(t)
