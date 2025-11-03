import time, json, hashlib
from pathlib import Path

LEDGER_PATH = Path(__file__).resolve().parents[0] / "ledger.json"

def heartbeat(interval=60):
    """Appends a cryptographic heartbeat every `interval` seconds to prove the ledger is alive."""
    while True:
        event = {
            "id": hashlib.sha256(str(time.time()).encode()).hexdigest(),
            "actor": "system",
            "payload": "ledger_heartbeat",
            "timestamp": time.time()
        }
        try:
            with open(LEDGER_PATH, "r", encoding="utf-8") as f:
                ledger = json.load(f)
        except:
            ledger = []
        ledger.append(event)
        with open(LEDGER_PATH, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)
        print(f"[HEARTBEAT] Recorded at {time.ctime()}")
        time.sleep(interval)

if __name__ == "__main__":
    print("[HEARTBEAT] Commons Ethics Framework monitor active.")
    heartbeat(300)  # 5-minute cycle