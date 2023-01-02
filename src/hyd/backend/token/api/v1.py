import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session

from hyd.backend.db import get_db
from hyd.backend.exc import (
    HTTPException_UNKNOWN_PROJECT,
    UnknownProjectError,
    UnknownTokenError,
)
from hyd.backend.project import service as project_services
from hyd.backend.security import Scopes, create_jwt
from hyd.backend.token.models import (
    API_V1_CREATE__POST,
    API_V1_LIST__GET,
    API_V1_REVOKE__PATCH,
    FullTokenResponseSchema,
    TokenEntry,
    TokenResponseSchema,
    TokenSchema,
)
from hyd.backend.token.service import create_token, read_token, revoke_token_by_ref
from hyd.backend.user.authentication import authenticate_user
from hyd.backend.user.models import UserEntry
from hyd.backend.util.const import HEADERS
from hyd.backend.util.logger import HydLogger
from hyd.backend.util.models import PrimaryKey

UTC = dt.timezone.utc
LOGGER = HydLogger("TokenAPI")

v1_router = APIRouter(tags=["token"])

####################################################################################################
#### HTTP Exceptions
####################################################################################################

HTTPException_TIMEZONE_AWARE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Expiration datetime must be timezone aware!",
    headers=HEADERS,
)

HTTPException_UNKNOWN_TOKEN = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Unknown token!",
    headers=HEADERS,
)

HTTPException_TOKEN_ALREADY_REVOKED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Token has already been revoked!",
    headers=HEADERS,
)

####################################################################################################
#### Scope: TOKEN
####################################################################################################


@v1_router.post("/create", responses=API_V1_CREATE__POST)
async def _create(
    project_id: PrimaryKey | None,
    expires_on: dt.datetime | dt.timedelta | None = None,
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.TOKEN]),
    db: Session = Depends(get_db),
) -> FullTokenResponseSchema:
    if isinstance(expires_on, dt.datetime):
        if expires_on.tzinfo is None:
            raise HTTPException_TIMEZONE_AWARE
        expires_on = expires_on.astimezone(UTC)
    elif isinstance(expires_on, dt.timedelta):
        expires_on = dt.datetime.now(tz=UTC) + expires_on

    try:
        _ = project_services.read_project(project_id=project_id, db=db)
    except UnknownProjectError:
        raise HTTPException_UNKNOWN_PROJECT

    user_id = user_entry.id
    scopes = [Scopes.PROJECT, Scopes.VERSION, Scopes.TAG]
    token_entry = create_token(
        user_id=user_id,
        expires_on=expires_on,
        scopes=scopes,
        is_login_token=False,
        project_id=project_id,
        db=db,
    )

    access_token: str = create_jwt(
        token_id=token_entry.id, user_id=user_id, username=user_entry.username, scopes=scopes
    )

    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, project_id: %d}",
        user_entry.session_token_entry.id,
        user_entry.id,
        user_entry.username,
        project_id if project_id else 0,
    )
    return FullTokenResponseSchema(
        access_token=access_token,
        token_id=token_entry.id,
        user_id=token_entry.user_id,
        created_at=token_entry.created_at,
        is_login_token=token_entry.is_login_token,
        is_expired=token_entry.is_expired,
        revoked_at=token_entry._revoked_at,
        scopes=[entry.scope for entry in token_entry.scope_entries],
        project_id=token_entry.project_id,
    )


@v1_router.post("/list", responses=API_V1_LIST__GET)
async def _list(
    include_expired_revoked: bool = False,
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.TOKEN]),
    db: Session = Depends(get_db),
) -> list[TokenResponseSchema]:
    if include_expired_revoked:
        return [_token_entry_to_response_schema(entry) for entry in user_entry.token_entries]
    else:
        return [
            _token_entry_to_response_schema(entry)
            for entry in user_entry.token_entries
            if (not entry._revoked_at and not entry.check_expiration(db=db))
        ]


@v1_router.patch("/revoke", responses=API_V1_REVOKE__PATCH)
async def _revoke(
    token_id: PrimaryKey,
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.TOKEN]),
    db: Session = Depends(get_db),
) -> TokenResponseSchema:
    try:
        token_entry = read_token(token_id=token_id, db=db)
    except UnknownTokenError:
        raise HTTPException_UNKNOWN_TOKEN

    if token_entry.revoked_at:
        raise HTTPException_TOKEN_ALREADY_REVOKED

    revoke_token_by_ref(token_entry=token_entry, db=db)

    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, revoked_token_id: %d}",
        user_entry.session_token_entry.id,
        user_entry.id,
        user_entry.username,
        token_id,
    )
    return _token_entry_to_response_schema(token_entry)


####################################################################################################
#### Util
####################################################################################################


def _token_entry_to_response_schema(token_entry: TokenEntry) -> TokenResponseSchema:
    return TokenResponseSchema(
        token_id=token_entry.id,
        user_id=token_entry.user_id,
        created_at=token_entry.created_at,
        is_login_token=token_entry.is_login_token,
        is_expired=token_entry.is_expired,
        revoked_at=token_entry._revoked_at,
        scopes=[entry.scope for entry in token_entry.scope_entries],
        project_id=token_entry.project_id,
    )
