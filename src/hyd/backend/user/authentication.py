import datetime as dt

from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes
from sqlalchemy.orm import Session

import hyd.backend.token.service as token_service
from hyd.backend.db import get_db
from hyd.backend.security import JWT, OAUTH2_SCHEME, verify_jwt
from hyd.backend.token.models import TokenEntry
from hyd.backend.user.models import UserEntry
from hyd.backend.util.error import VerificationError
from hyd.backend.util.logger import HydLogger

UTC = dt.timezone.utc
LOGGER = HydLogger("Authentication")

HEADERS = {"WWW-Authenticate": "Bearer"}

HTTPException_VALIDATION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token unknown, expired, revoked or corrupted!",
    headers=HEADERS,
)

HTTPException_USER_DISABLED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User is disabled!",
    headers=HEADERS,
)

HTTPException_NO_PERMISSION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not enough permissions!",
    headers=HEADERS,
)


def _authenticate(
    security_scopes: SecurityScopes, token: str, db: Session
) -> tuple[UserEntry, TokenEntry]:
    try:
        jwt: JWT = verify_jwt(token=token)
    except VerificationError as err:
        LOGGER.warning(
            "Token verification failed! {token: %s, error: %s}",
            token,
            err,
        )
        raise HTTPException_VALIDATION

    token_entry: TokenEntry = token_service.read_token(token_id=jwt.id, db=db)  # TODO raise if None
    if token_entry is None:
        LOGGER.warning(
            "Verified token not found in database! {token: %s, error: %s}",
            token,
            err,
        )
        raise HTTPException_VALIDATION

    permitted_scopes: list[str] = [entry.scope for entry in token_entry.scope_entries]
    user_entry: UserEntry = token_entry.user_entry

    # check if an user is disabled, because one login tokens expire while disabling an user
    if user_entry.is_disabled:
        LOGGER.warning(
            "Token belongs to deactivated user! {token_id: %d, user_id: %d, username: %s}",
            token_entry.id,
            user_entry.id,
            user_entry.username,
        )
        raise HTTPException_USER_DISABLED

    # check if a token is expired, login and api tokens
    if token_entry.revoked_at or token_entry.check_expiration(db=db):
        LOGGER.warning(
            "Revoked or expired token used! {token_id: %d, user_id: %d, username: %s}",
            token_entry.id,
            user_entry.id,
            user_entry.username,
        )
        raise HTTPException_VALIDATION

    # check scopes for permission handling
    for scope in security_scopes.scopes:
        if scope not in permitted_scopes:
            LOGGER.warning(
                "Token lacks scopes! {token_id: %d, user_id: %d, username: %s}",
                token_entry.id,
                user_entry.id,
                user_entry.username,
            )
            raise HTTPException_NO_PERMISSION

    user_entry._session_token_entry = token_entry
    user_entry._session_permitted_scopes = permitted_scopes
    token_entry._last_request = dt.datetime.now(tz=UTC)

    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, scopes: %s}",
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
    user_entry, _token_entry = _authenticate(security_scopes, token, db)
    return user_entry
