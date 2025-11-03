import json, base64
from cryptography.fernet import Fernet
from pathlib import Path

KEY_FILE = Path(__file__).resolve().parents[0] / "exchange.key"

def generate_key():
    """Generate or load encryption key for distributed consent exchange."""
    if not KEY_FILE.exists():
        key = Fernet.generate_key()
        KEY_FILE.write_bytes(key)
    else:
        key = KEY_FILE.read_bytes()
    return Fernet(key)

def encrypt_token(data: dict) -> str:
    """Encrypt a consent token payload for secure transmission."""
    f = generate_key()
    payload = json.dumps(data).encode()
    return f.encrypt(payload).decode()

def decrypt_token(token: str) -> dict:
    """Decrypt the received token payload."""
    f = generate_key()
    return json.loads(f.decrypt(token.encode()).decode())
