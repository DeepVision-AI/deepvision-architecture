from typing import Any, Dict

from ..main import supabase_client
from .refresh import serialize_session


def loginUser(email: str, password: str) -> Dict[str, Any]:
    try:
        response = supabase_client.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })

        session = getattr(response, "session", None)
        user = getattr(response, "user", None)
        if session is None:
            return {"success": False, "error": "Authentication succeeded without a session."}

        session_payload = serialize_session(session)
        if user is not None and hasattr(user, "dict"):
            session_payload["user"] = user.dict()
        else:
            session_payload["user"] = None

        return {"success": True, **session_payload}
    except Exception as exc:
        return {"success": False, "error": str(exc)}

