from typing import Any, Dict

from ..main import supabase_client


def serialize_session(session: Any) -> Dict[str, Any]:
    access_token = getattr(session, "access_token", None)
    refresh_token = getattr(session, "refresh_token", None)
    expires_in = getattr(session, "expires_in", None)
    expires_at = getattr(session, "expires_at", None)
    token_type = getattr(session, "token_type", None)
    return {
        "token": access_token,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": expires_in,
        "expires_at": expires_at,
        "token_type": token_type,
    }


def refreshUserSession(refresh_token: str) -> Dict[str, Any]:
    if not isinstance(refresh_token, str) or not refresh_token.strip():
        return {"success": False, "error": "refresh_token required"}

    try:
        response = supabase_client.auth.refresh_session(refresh_token.strip())
        session = getattr(response, "session", None)
        user = getattr(response, "user", None)
        if session is None:
            return {"success": False, "error": "Failed to refresh session."}

        payload = serialize_session(session)
        if user is not None and hasattr(user, "dict"):
            payload["user"] = user.dict()
        else:
            payload["user"] = None

        return {"success": True, **payload}
    except Exception as exc:
        return {"success": False, "error": str(exc)}
