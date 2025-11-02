cerl_preemptive/consent_ledger.py
# cerl_preemptive/consent_ledger.py
# Commons Ethical Research License (CERL-1.0) – Non-Commercial, Non-Derivative
# © 2025 Mya P. Brown & Advanced AI Technology

import hashlib, json, os, time, uuid
from typing import Optional

LEDGER_PATH = "ledger.jsonl"

def _hash(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

def last_hash() -> str:
    if not os.path.exists(LEDGER_PATH):
        return "0" * 64
    with open(LEDGER_PATH, "rb") as f:
        *_, last = f.readlines() or [b"0"]
    try:
        return json.loads(last.decode())["hash"]
    except Exception:
        return "0" * 64

def append_event(actor: str, action: str, payload: dict, consent_token: Optional[str] = None):
    prev = last_hash()
    event = {
        "ts": time.time(),
        "id": str(uuid.uuid4()),
        "actor": actor,
        "action": action,
        "payload": payload,
        "consent_token": consent_token,
        "prev_hash": prev,
    }
    raw = json.dumps(event, sort_keys=True)
    event["hash"] = _hash(raw)
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
    return event["hash"]

def verify_chain() -> bool:
    if not os.path.exists(LEDGER_PATH):
        return True
    prev = "0" * 64
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            event = json.loads(line)
            check = _hash(json.dumps({k: event[k] for k in event if k != "hash"}, sort_keys=True))
            if check != event["hash"] or event["prev_hash"] != prev:
                return False
            prev = event["hash"]
    return True

if __name__ == "__main__":
    print("CERL-Preemptive Ledger initialized.")
    print("Integrity OK?" , verify_chain())
Added CERL Preemptive Ledger module
