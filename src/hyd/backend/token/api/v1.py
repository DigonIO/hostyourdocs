import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session

from hyd.backend.db import get_db
from hyd.backend.project import service as project_services
from hyd.backend.security import Scopes, create_jwt
from hyd.backend.token.models import TokenEntry, TokenMetaSchema, TokenSchema
from hyd.backend.token.service import create_token, read_token, revoke_token_by_ref
from hyd.backend.user.authentication import authenticate_user
from hyd.backend.user.models import UserEntry
from hyd.backend.util.const import HEADERS
from hyd.backend.util.error import UnknownEntryError
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
    detail="Expiration datetime must be timezone aware.",
    headers=HEADERS,
)

####################################################################################################
#### Scope: TOKEN
####################################################################################################


@v1_router.post("/create")
async def _create(
    project_id: PrimaryKey,
    expires_on: dt.datetime | dt.timedelta | None = None,
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.TOKEN]),
    db: Session = Depends(get_db),
):

    if isinstance(expires_on, dt.timedelta):
        expires_on = dt.datetime.now(tz=UTC) + expires_on
    elif isinstance(expires_on, dt.datetime) and expires_on.tzinfo is None:
        raise HTTPException_TIMEZONE_AWARE

    try:
        _ = project_services.read_project(project_id=project_id, db=db)
    except UnknownEntryError:
        raise HTTPException  # TODO better msg

    user_id = user_entry.id
    scopes = [Scopes.PROJECT, Scopes.VERSION, Scopes.TAG]
    token_entry = create_token(
        user_id=user_id,
        expires_on=expires_on.astimezone(UTC),
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
        user_entry.get_session_token_entry().id,
        user_entry.id,
        user_entry.username,
        project_id if project_id else 0,
    )
    return TokenSchema(access_token=access_token, token_type="bearer")


@v1_router.post("/list")
async def _list(
    include_expired_revoked: bool = False,
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.TOKEN]),
    db: Session = Depends(get_db),
):
    if include_expired_revoked:
        return [token_entry_to_meta_schema(entry) for entry in user_entry.token_entries]
    else:
        return [
            token_entry_to_meta_schema(entry)
            for entry in user_entry.token_entries
            if (not entry._revoked_at and not entry.check_expiration(db=db))
        ]


@v1_router.post("/revoke")
async def _revoke(
    token_id: PrimaryKey,
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.TOKEN]),
    db: Session = Depends(get_db),
):
    token_entry = read_token(token_id=token_id, db=db)
    revoke_token_by_ref(token_entry=token_entry, db=db)

    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, revoked_token_id: %d}",
        user_entry.get_session_token_entry().id,
        user_entry.id,
        user_entry.username,
        token_id,
    )
    return token_entry_to_meta_schema(token_entry)


####################################################################################################
#### Util
####################################################################################################


def token_entry_to_meta_schema(token_entry: TokenEntry) -> TokenMetaSchema:
    return TokenMetaSchema(
        token_id=token_entry.id,
        user_id=token_entry.user_id,
        is_login_token=token_entry.is_login_token,
        is_expired=token_entry.is_expired,
        revoked_at=token_entry._revoked_at,
        scopes=[entry.scope for entry in token_entry.scope_entries],
        project_id=token_entry.project_id,
    )
