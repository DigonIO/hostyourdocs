from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose.jwt import decode, encode
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

from hyd.backend.exc import HydError, VerificationError
from hyd.backend.util.const import SECRET_KEY
from hyd.backend.util.models import NameStr, PrimaryKey

if SECRET_KEY is None:
    raise HydError("SECRET_KEY is missing!")

# https://docs.python.org/3/library/secrets.html#how-many-bytes-should-tokens-use
if len(SECRET_KEY) < 64:
    raise HydError("SECRET_KEY is to short, use 32 byte or more!")

ALGORITHM = "HS256"

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Scopes:
    USER = "user"
    TOKEN = "token"
    PROJECT = "project"
    VERSION = "version"
    TAG = "tag"


SCOPES = [
    Scopes.USER,
    Scopes.TOKEN,
    Scopes.PROJECT,
    Scopes.VERSION,
    Scopes.TAG,
]

OAUTH2_SCHEME = OAuth2PasswordBearer(
    tokenUrl="/api/v1/user/login",
    scopes={
        Scopes.USER: "Basic user operations.",
        Scopes.TOKEN: "Manage tokens.",
        Scopes.PROJECT: "Create, delete and list projects.",
        Scopes.VERSION: "Manage versions for a project.",
        Scopes.TAG: "Manage tags for a project.",
    },
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
