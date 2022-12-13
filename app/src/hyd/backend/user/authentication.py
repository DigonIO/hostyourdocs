import hyd.token.service as token_service
from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes
from hyd.db import get_db
from hyd.security import JWT, OAUTH2_SCHEME, verify_jwt
from hyd.token.models import TokenEntry
from hyd.user.models import UserEntry
from hyd.util.error import VerificationError
from hyd.util.logger import HydLogger
from sqlalchemy.orm import Session

LOGGER = HydLogger("Authentication")

HEADERS = {"WWW-Authenticate": "Bearer"}

HTTPException_NO_PERMISSION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not enough permissions.",
    headers=HEADERS,
)


async def _authenticate(
    security_scopes: SecurityScopes, token: str, db: Session
) -> tuple[UserEntry, TokenEntry]:
    try:
        jwt: JWT = verify_jwt(token=token)
    except VerificationError as err:
        LOGGER.error("Faulty or manipulated token used {token: %s, error: %s}", token, err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers=HEADERS,
        )

    token_entry: TokenEntry = await token_service.read_token(token_id=jwt.id, db=db)
    permitted_scopes: list[str] = [entry.scope for entry in token_entry.scope_entries]
    user_entry: UserEntry = token_entry.user_entry

    # check if an user is disabled, because one login tokens expire while disabling an user
    if user_entry.is_disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is disabled.",
            headers=HEADERS,
        )

    # check if a token is expired, login and api tokens
    if token_entry.is_expired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token expired.",
            headers=HEADERS,
        )

    # check scopes for permission handling
    for scope in security_scopes.scopes:
        if scope not in permitted_scopes:
            raise HTTPException_NO_PERMISSION

    user_entry._current_session_token_entry = token_entry
    user_entry._current_permitted_scopes = permitted_scopes

    LOGGER.info(
        "Authentication successfully {token_id: %d, user_id: %d, username: %s, scopes: %s}",
        jwt.id,
        user_entry.id,
        user_entry.username,
        permitted_scopes,
    )
    return user_entry, token_entry


async def authenticate_user(
    security_scopes: SecurityScopes,
    token: str = Depends(OAUTH2_SCHEME),
    db: Session = Depends(get_db),
) -> UserEntry:
    user_entry, _token_entry = await _authenticate(security_scopes, token, db)
    return user_entry
