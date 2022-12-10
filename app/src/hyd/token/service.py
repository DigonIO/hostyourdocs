from sqlalchemy.orm import Session

from hyd.util.models import PrimaryKey
from hyd.token.models import TokenEntry, TokenScopeEntry
from hyd.util.logger import HydLogger

LOGGER = HydLogger("TokenService")


async def create_token(
    *, user_id: PrimaryKey, scopes: list[str], is_login_token: bool, db: Session
) -> TokenEntry:
    token_entry = TokenEntry(user_id=user_id, is_login_token=is_login_token)
    db.add(token_entry)
    db.commit()

    token_id = token_entry.id
    for scope in scopes:
        scope_entry = TokenScopeEntry(token_id=token_id, scope=scope)
        db.add(scope_entry)

    db.commit()
    LOGGER.debug("TokenEntry created {id: %d, scopes: %s}", token_id, scopes)
    return token_entry


async def read_token(*, token_id: int, db: Session) -> TokenEntry:
    # TODO unknown entry ID error
    return db.query(TokenEntry).get(token_id)


async def read_tokens(*, db: Session) -> list[TokenEntry]:
    return db.query(TokenEntry).all()


async def expire_token_by_ref(*, token_entry: TokenEntry, db: Session) -> None:
    token_entry.is_expired = True
    db.commit()
