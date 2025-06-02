import secrets
from datetime import datetime, timedelta, timezone

def generate_token():
    return secrets.token_urlsafe(32)

def generate_expiration(minutes=15):
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)