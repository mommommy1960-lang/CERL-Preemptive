import uuid, time, json
from pathlib import Path

TOKENS = Path(__file__).resolve().parents[0] / "tokens.jsonl"

def issue_token(actor: str, scope: str, expiry_hours: int = 24):
    """Create a signed consent token with a short lifetime."""
    token_id = str(uuid.uuid4())
    expiry = time.time() + expiry_hours * 3600
    record = {"token": token_id, "actor": actor, "scope": scope, "expiry": expiry}
    with open(TOKENS, "a", encoding="utf-8") as f:
        json.dump(record, f)
        f.write("\n")
    print(f"[TOKEN] Issued token {token_id[:8]} for {actor} ({scope})")
    return token_id

def validate_token(token_id: str) -> bool:
    """Return True if the token exists and is still valid."""
    now = time.time()
    try:
        with open(TOKENS, "r", encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                if rec["token"] == token_id:
                    if now <= rec["expiry"]:
                        print(f"[TOKEN] Valid token for {rec['actor']}")
                        return True
                    print(f"[TOKEN] Expired token for {rec['actor']}")
                    return False
    except FileNotFoundError:
        pass
    print("[TOKEN] Token not found")
    return False

if __name__ == "__main__":
    t = issue_token("commons_system", "ledger_write", 1)
    validate_token(t)