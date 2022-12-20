import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session

from hyd.backend.db import get_db
from hyd.backend.security import Scopes, create_jwt
from hyd.backend.token.models import TokenEntry, TokenMetaSchema, TokenSchema
from hyd.backend.token.service import create_token, read_token, revoke_token_by_ref
from hyd.backend.user.authentication import authenticate_user
from hyd.backend.user.models import UserEntry
from hyd.backend.util.const import SRV_TIMEZONE
from hyd.backend.util.logger import HydLogger
from hyd.backend.util.models import PrimaryKey

LOGGER = HydLogger("TokenAPI")

v1_router = APIRouter(tags=["token"])

####################################################################################################
#### Scope: TOKEN
####################################################################################################


@v1_router.post("/create")
async def api_create(
    project_scope: bool = False,
    version_scope: bool = False,
    tag_scope: bool = False,
    expires: dt.datetime | dt.timedelta | None = None,
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.TOKEN]),
    db: Session = Depends(get_db),
):

    scopes = []
    if project_scope:
        scopes.append(Scopes.PROJECT)
    if version_scope:
        scopes.append(Scopes.VERSION)
    if tag_scope:
        scopes.append(Scopes.TAG)

    if isinstance(expires, dt.timedelta):
        expires = dt.datetime.now(tz=SRV_TIMEZONE) + expires
    elif isinstance(expires, dt.datetime) and expires.tzinfo is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expiration datetime must be timezone aware.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = user_entry.id
    token_entry = create_token(
        user_id=user_id, expires=expires, scopes=scopes, is_login_token=False, db=db
    )

    access_token: str = create_jwt(
        token_id=token_entry.id, user_id=user_id, username=user_entry.username, scopes=scopes
    )

    LOGGER.info(
        "Token created {token_id: %d, user_id: %d, username: %s, scopes: %s}",
        token_entry.id,
        user_entry.id,
        user_entry.username,
        scopes,
    )
    return TokenSchema(access_token=access_token, token_type="bearer")


@v1_router.post("/list")
async def api_list(
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
            if (not entry.was_revoked and not entry.check_expiration(db=db))
        ]


@v1_router.post("/revoke")
async def api_revoke(
    token_id: PrimaryKey,
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.TOKEN]),
    db: Session = Depends(get_db),
):
    token_entry = read_token(token_id=token_id, db=db)
    revoke_token_by_ref(token_entry=token_entry, db=db)
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
        was_revoked=token_entry.was_revoked,
        scopes=[entry.scope for entry in token_entry.scope_entries],
    )
