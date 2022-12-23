import datetime as dt

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hyd.backend.token.models import TokenEntry, TokenScopeEntry
from hyd.backend.util.const import SRV_TIMEZONE
from hyd.backend.util.error import UnknownEntryError
from hyd.backend.util.logger import HydLogger
from hyd.backend.util.models import PrimaryKey

LOGGER = HydLogger("TokenService")


def create_token(
    *,
    user_id: PrimaryKey,
    expires: dt.datetime | None,
    scopes: list[str],
    is_login_token: bool,
    db: Session,
) -> TokenEntry:
    token_entry = TokenEntry(user_id=user_id, expires=expires, is_login_token=is_login_token)
    db.add(token_entry)
    db.commit()

    token_id = token_entry.id
    for scope in scopes:
        scope_entry = TokenScopeEntry(token_id=token_id, scope=scope)
        db.add(scope_entry)

    db.commit()
    LOGGER.debug("TokenEntry created {id: %d, scopes: %s}", token_id, scopes)
    return token_entry


def read_token(*, token_id: int, db: Session) -> TokenEntry:
    try:
        token_entry = db.query(TokenEntry).get(token_id)
    except IntegrityError:
        raise UnknownEntryError
    return token_entry


def read_tokens(*, db: Session) -> list[TokenEntry]:
    return db.query(TokenEntry).all()


def revoke_token_by_ref(*, token_entry: TokenEntry, db: Session) -> None:
    token_entry.revoked_at = dt.datetime.now(tz=SRV_TIMEZONE)
    db.commit()
