from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from hyd.backend.db import EXTEND_EXISTING, DeclarativeMeta
from hyd.backend.security import Scopes
from hyd.backend.token.models import TokenEntry
from hyd.backend.util.const import MAX_LENGTH_STR_ID
from hyd.backend.util.models import TimeStampMixin


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class UserEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "user_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}
    id = Column(Integer, primary_key=True)
    username = Column(String(length=MAX_LENGTH_STR_ID), unique=True)
    hashed_password = Column(LargeBinary)
    is_admin = Column(Boolean)
    is_disabled = Column(Boolean, default=False)

    token_entries = relationship("TokenEntry", back_populates="user_entry")
    login_token_entries = relationship(
        "TokenEntry",
        primaryjoin=("and_(TokenEntry.user_id==UserEntry.id, TokenEntry.is_login_token==True)"),
        viewonly=True,
    )

    _session_token_entry: TokenEntry | None = None
    _session_permitted_scopes: list[str] | None = None

    def get_session_token_entry(this) -> TokenEntry:  # TODO raise if None
        return this._current_session_token_entry

    def check_scope_permission(this, *, scope: Scopes) -> bool:  # TODO raise if None
        """Check if the given scope is permitted for the given session."""
        return scope.value in this._session_permitted_scopes
