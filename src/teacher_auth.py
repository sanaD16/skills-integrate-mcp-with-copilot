import hashlib
import hmac
import json
import secrets
from pathlib import Path


TEACHERS_FILE = Path(__file__).with_name("teachers.json")
PASSWORD_ITERATIONS = 310_000


def create_password_record(password: str) -> dict[str, str]:
    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS
    )
    return {"salt": salt.hex(), "password_hash": password_hash.hex()}


def verify_password(username: str, password: str) -> bool:
    try:
        teachers = json.loads(TEACHERS_FILE.read_text(encoding="utf-8"))["teachers"]
        record = teachers[username]
        salt = bytes.fromhex(record["salt"])
        expected_hash = record["password_hash"]
    except (FileNotFoundError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return False

    actual_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS
    ).hex()
    return hmac.compare_digest(actual_hash, expected_hash)