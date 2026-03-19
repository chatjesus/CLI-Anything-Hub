"""
Stripe subscription flow for CLI-Anything Hub.

Talks to the AgentPuter API backend which wraps Stripe Checkout.
The CLI never touches Stripe keys directly — all billing logic is server-side.

API base: https://api.agentputer.com/cli-anything/v1
"""
import json
import webbrowser
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

API_BASE = "https://api.agentputer.com/cli-anything/v1"

PLANS = [
    {
        "id": "weekly",
        "name": "Weekly",
        "price": "$3.99/week",
        "price_cents": 399,
        "interval": "week",
        "description": "Try Pro features weekly, cancel anytime",
    },
    {
        "id": "monthly",
        "name": "Monthly",
        "price": "$9.99/month",
        "price_cents": 999,
        "interval": "month",
        "description": "Most popular — full Pro access",
    },
    {
        "id": "yearly",
        "name": "Yearly",
        "price": "$79.99/year",
        "price_cents": 7999,
        "interval": "year",
        "description": "Best value — save 33% vs monthly",
    },
]


def _api_request(endpoint: str, method: str = "GET", data: Optional[dict] = None, token: Optional[str] = None) -> dict:
    url = f"{API_BASE}{endpoint}"
    headers = {"Content-Type": "application/json", "User-Agent": "cli-anything/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = Request(url, data=body, headers=headers, method=method)
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        try:
            err_body = json.loads(e.read().decode("utf-8"))
            return {"error": True, "message": err_body.get("message", str(e)), "status": e.code}
        except Exception:
            return {"error": True, "message": str(e), "status": e.code}
    except URLError as e:
        return {"error": True, "message": f"Network error: {e.reason}", "status": 0}


def list_plans() -> list[dict]:
    return PLANS


def create_checkout_session(plan_id: str, email: str) -> dict:
    """
    POST /subscribe/create → returns { checkout_url, session_id }
    Opens the Stripe Checkout page in the user's browser.
    """
    result = _api_request("/subscribe/create", method="POST", data={
        "plan": plan_id,
        "email": email,
    })
    if result.get("error"):
        return result
    checkout_url = result.get("checkout_url")
    if checkout_url:
        webbrowser.open(checkout_url)
    return result


def verify_subscription(email: str, token: Optional[str] = None) -> dict:
    """
    GET /subscribe/status?email=xxx → returns subscription state from server.
    Used after payment to confirm and sync local credentials.
    """
    return _api_request(f"/subscribe/status?email={email}", token=token)


def send_login_code(email: str) -> dict:
    """POST /auth/send-code → sends 6-digit code to email."""
    return _api_request("/auth/send-code", method="POST", data={"email": email})


def verify_login_code(email: str, code: str) -> dict:
    """
    POST /auth/verify-code → returns { access_token, plan, customer_id, ... }
    """
    return _api_request("/auth/verify-code", method="POST", data={
        "email": email,
        "code": code,
    })


def activate_license_key(key: str) -> dict:
    """POST /auth/activate → returns { email, plan, access_token, ... }"""
    return _api_request("/auth/activate", method="POST", data={"license_key": key})
