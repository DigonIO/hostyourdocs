import hyd.backend.token.service as token_service
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordRequestForm
from hyd.backend.db import get_db
from hyd.backend.security import SCOPES, Scopes, create_jwt, verify_password
from hyd.backend.token.models import TokenEntry
from hyd.backend.user.authentication import authenticate_user
from hyd.backend.user.models import TokenSchema, UserEntry
from hyd.backend.user.service import read_users_by_username, update_user_pw_by_ref
from hyd.backend.util.logger import HydLogger
from sqlalchemy.orm import Session

LOGGER = HydLogger("UserAPI")

v1_router = APIRouter(tags=["user"])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Basic"},
)

####################################################################################################
#### No login required
####################################################################################################


@v1_router.post("/login", response_model=TokenSchema)
async def api_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    username = form_data.username
    user_entries: list[UserEntry] = await read_users_by_username(username=username, db=db)
    if not user_entries:
        raise credentials_exception

    user_entry = user_entries[0]

    if not verify_password(
        plain_password=form_data.password, hashed_password=user_entry.hashed_password
    ):
        raise credentials_exception

    if user_entry.is_disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is disabled.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = user_entry.id
    token_entry = await token_service.create_token(
        user_id=user_id, scopes=SCOPES, is_login_token=True, db=db
    )

    access_token: str = create_jwt(
        token_id=token_entry.id, user_id=user_id, username=username, scopes=SCOPES
    )
    LOGGER.info(
        "Login successfully {token_id: %d, user_id: %d, username: %s, scopes: %s}",
        token_entry.id,
        user_entry.id,
        user_entry.username,
        SCOPES,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }  # TODO Refactor result


####################################################################################################
#### Scope: USER
####################################################################################################


@v1_router.post("/logout")
async def api_logout(
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.USER]),
    db: Session = Depends(get_db),
):
    token_entry = user_entry.get_session_token_entry()
    await token_service.expire_token_by_ref(token_entry=token_entry, db=db)
    return f"Logout {user_entry.username} :("  # TODO Refactor result


@v1_router.post("/change_password")
async def api_change_password(
    current_password: str,
    new_password: str,
    new_password_repetition: str,
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.USER]),
    db: Session = Depends(get_db),
):
    if not verify_password(
        plain_password=current_password, hashed_password=user_entry.hashed_password
    ):
        raise credentials_exception

    if new_password != new_password_repetition:
        ...  # TODO Raise exception

    await update_user_pw_by_ref(user_entry=user_entry, new_password=new_password, db=db)


@v1_router.get("/greet")
async def api_greet(user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.USER])):
    return f"Hello {user_entry.username} :)"  # TODO Refactor result
