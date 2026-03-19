"""
Local credential management for CLI-Anything Hub.

Stores auth state in ~/.cli-anything/credentials.json
All CLIs share the same credential store — one login unlocks everything.
"""
import json
import os
import time
from pathlib import Path
from typing import Optional


def get_config_dir() -> Path:
    d = Path.home() / ".cli-anything"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _cred_path() -> Path:
    return get_config_dir() / "credentials.json"


def get_credentials() -> dict:
    p = _cred_path()
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_credentials(**kwargs) -> None:
    creds = get_credentials()
    creds.update(kwargs)
    creds["updated_at"] = int(time.time())
    _cred_path().write_text(
        json.dumps(creds, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    os.chmod(_cred_path(), 0o600)


def clear_credentials() -> None:
    p = _cred_path()
    if p.exists():
        p.unlink()


def is_logged_in() -> bool:
    creds = get_credentials()
    return bool(creds.get("email") and creds.get("access_token"))


def is_pro() -> bool:
    creds = get_credentials()
    if not creds.get("access_token"):
        return False
    plan = creds.get("plan", "free")
    if plan == "free":
        return False
    expires = creds.get("subscription_expires_at", 0)
    if expires and expires < time.time():
        return False
    return True


def get_email() -> Optional[str]:
    return get_credentials().get("email")


def get_plan() -> str:
    return get_credentials().get("plan", "free")


def get_plan_display() -> str:
    plan = get_plan()
    return {"free": "Free", "weekly": "Weekly ($3.99/wk)", "monthly": "Monthly ($9.99/mo)", "yearly": "Yearly ($79.99/yr)"}.get(plan, plan.title())


def get_subscription_status() -> dict:
    creds = get_credentials()
    return {
        "logged_in": is_logged_in(),
        "email": creds.get("email"),
        "plan": get_plan(),
        "plan_display": get_plan_display(),
        "is_pro": is_pro(),
        "subscription_id": creds.get("subscription_id"),
        "expires_at": creds.get("subscription_expires_at"),
        "customer_id": creds.get("customer_id"),
    }
