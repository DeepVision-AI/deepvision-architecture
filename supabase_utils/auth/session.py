from typing import Any, Optional

from ..main import supabase_client


def _ensure_active_session() -> Optional[Any]:
    session = supabase_client.auth.get_session()
    if session is None:
        return None

    access_token = getattr(session, "access_token", None)
    if access_token:
        return session

    refresh_token = getattr(session, "refresh_token", None)
    if refresh_token:
        try:
            refreshed = supabase_client.auth.refresh_session(refresh_token)
            new_session = getattr(refreshed, "session", None)
            if new_session is not None:
                return new_session
        except Exception:
            return session

    return session


def getAccessToken() -> Optional[str]:
    session = _ensure_active_session()
    if session is None:
        return None
    return getattr(session, "access_token", None)


def getRefreshToken() -> Optional[str]:
    session = _ensure_active_session()
    if session is None:
        return None
    return getattr(session, "refresh_token", None)


def getCurrentUser():
    user_response = supabase_client.auth.get_user()
    return getattr(user_response, "user", None)

