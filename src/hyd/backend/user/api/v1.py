import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import hyd.backend.token.service as token_service
from hyd.backend.db import get_db
from hyd.backend.exc import UnknownUserError
from hyd.backend.security import SCOPES, Scopes, create_jwt, verify_password
from hyd.backend.token.models import TokenSchema
from hyd.backend.user.authentication import (
    HTTPException_USER_DISABLED,
    authenticate_user,
)
from hyd.backend.user.models import UserEntry
from hyd.backend.user.service import read_users_by_username, update_user_pw_by_ref
from hyd.backend.util.const import HEADERS, REMEMBER_ME_DURATION
from hyd.backend.util.logger import HydLogger

UTC = dt.timezone.utc
LOGGER = HydLogger("UserAPI")

v1_router = APIRouter(tags=["user"])

####################################################################################################
#### HTTP Exceptions
####################################################################################################

HTTPException_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Basic"},
)

HTTPException_PASSWORD_REPETITION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="The new password and the repetition must match each other!",
    headers=HEADERS,
)

####################################################################################################
#### No login required
####################################################################################################


@v1_router.post("/login", response_model=TokenSchema)
async def _login(
    remember_me: bool = False,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    username = form_data.username
    try:
        user_entry: UserEntry = read_users_by_username(username=username, db=db)
    except UnknownUserError:
        LOGGER.warning(
            "Unknown username {username: %s}",
            username,
        )
        raise HTTPException_CREDENTIALS

    if not verify_password(
        plain_password=form_data.password, hashed_password=user_entry.hashed_password
    ):
        LOGGER.warning(
            "Wrong password {user_id: %d, username: %s}",
            user_entry.id,
            username,
        )
        raise HTTPException_CREDENTIALS

    if user_entry.is_disabled:
        LOGGER.warning(
            "Disabled {user_id: %d, username: %s}",
            user_entry.id,
            username,
        )
        raise HTTPException_USER_DISABLED

    expires_on = dt.datetime.now(tz=UTC)
    if remember_me:
        expires_on = expires_on + REMEMBER_ME_DURATION

    user_id = user_entry.id
    token_entry = token_service.create_token(
        user_id=user_id,
        expires_on=expires_on,
        scopes=SCOPES,
        is_login_token=True,
        project_id=None,
        db=db,
    )

    access_token: str = create_jwt(
        token_id=token_entry.id, user_id=user_id, username=username, scopes=SCOPES
    )
    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s}",
        token_entry.id,
        user_entry.id,
        username,
    )
    return TokenSchema(access_token=access_token, token_type="bearer")


####################################################################################################
#### Scope: USER
####################################################################################################


@v1_router.post("/logout")
async def _logout(
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.USER]),
    db: Session = Depends(get_db),
):
    token_entry = user_entry.session_token_entry
    token_service.revoke_token_by_ref(token_entry=token_entry, db=db)

    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s}",
        token_entry.id,
        user_entry.id,
        user_entry.username,
    )
    return f"Logout {user_entry.username} :("  # TODO Refactor result


@v1_router.post("/change_password")
async def _change_password(
    current_password: str,
    new_password: str,
    new_password_repetition: str,
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.USER]),
    db: Session = Depends(get_db),
):
    if not verify_password(
        plain_password=current_password, hashed_password=user_entry.hashed_password
    ):
        LOGGER.info(
            "{token_id: %d, user_id: %d, username: %s}",
            user_entry.session_token_entry.id,
            user_entry.id,
            user_entry.username,
        )
        raise HTTPException_CREDENTIALS

    if new_password != new_password_repetition:
        raise HTTPException_PASSWORD_REPETITION

    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s}",
        user_entry.session_token_entry.id,
        user_entry.id,
        user_entry.username,
    )
    update_user_pw_by_ref(user_entry=user_entry, new_password=new_password, db=db)


@v1_router.get("/greet")
async def _greet(user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.USER])):
    return f"Hello {user_entry.username} :)"  # TODO Refactor result
