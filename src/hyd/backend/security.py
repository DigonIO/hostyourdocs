from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose.jwt import decode, encode
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

from hyd.backend.util.error import VerificationError
from hyd.backend.util.models import NameStr, PrimaryKey

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# TODO must not no be in source
# Add this later as env var

ALGORITHM = "HS256"

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Scopes:
    USER = "user"
    TOKEN = "token"


SCOPES = {
    Scopes.USER: "Basic user meta operations.",
    Scopes.TOKEN: "Create and manage tokens.",
}

OAUTH2_SCHEME = OAuth2PasswordBearer(
    tokenUrl="/api/v1/user/login",
    scopes=SCOPES,
)


class JWT(BaseModel):
    id: PrimaryKey
    user_id: PrimaryKey  # key value pair just for debugging
    username: NameStr  # key value pair just for debugging
    scopes: list[str]  # key value pair just for debugging


def hash_password(*, password: str | bytes) -> bytes:
    return _pwd_context.hash(password).encode()


def verify_password(*, plain_password: str | bytes, hashed_password: str | bytes) -> bool:
    return _pwd_context.verify(plain_password, hashed_password)


def create_jwt(
    *, token_id: PrimaryKey, user_id: PrimaryKey, username: NameStr, scopes: list[str]
) -> str:
    return encode(
        {"jti": str(token_id), "uid": str(user_id), "sub": username, "scopes": scopes},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_jwt(*, token: str) -> JWT:
    try:  # check signature
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as err:
        raise VerificationError(err)

    try:  # check for missing fields
        token_id: PrimaryKey = int(payload["jti"])
        user_id: NameStr = int(payload["uid"])
        username: NameStr = payload["sub"]
        scopes: list[str] = payload["scopes"]
    except KeyError as err:
        raise VerificationError(err)

    try:  # check for data type validity
        return JWT(id=token_id, user_id=user_id, username=username, scopes=scopes)
    except ValidationError as err:
        raise VerificationError(err)
