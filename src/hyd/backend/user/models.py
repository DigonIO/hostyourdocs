from fastapi import HTTPException
from sqlalchemy import Boolean, Column, Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, relationship

from hyd.backend.db import EXTEND_EXISTING, DeclarativeMeta
from hyd.backend.token.models import TokenEntry
from hyd.backend.util.const import MAX_LENGTH_STR_ID
from hyd.backend.util.error import HTTPException_NO_PERMISSION
from hyd.backend.util.models import PrimaryKey, TimeStampMixin


class UserEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "user_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}
    id = Column(Integer, primary_key=True)
    username = Column(String(length=MAX_LENGTH_STR_ID), unique=True)
    hashed_password = Column(LargeBinary)
    is_admin = Column(Boolean)
    is_disabled = Column(Boolean, default=False)

    token_entries: Mapped[list[TokenEntry]] = relationship(
        "TokenEntry", back_populates="user_entry"
    )
    login_token_entries: Mapped[list[TokenEntry]] = relationship(
        "TokenEntry",
        primaryjoin=("and_(TokenEntry.user_id==UserEntry.id, TokenEntry.is_login_token==True)"),
        viewonly=True,
    )

    _session_token_entry: TokenEntry | None = None
    _session_permitted_scopes: list[str] | None = None

    @property
    def session_token_entry(self) -> TokenEntry:
        return self._session_token_entry

    def check_scope_permission(self, *, scope: str) -> bool:  # TODO raise if None
        """Check if the given scope is permitted for the given session."""
        return scope in self._session_permitted_scopes

    def check_token_project_permission(self, *, project_id: PrimaryKey) -> None:
        token_project_id = self._session_token_entry.project_id
        if token_project_id is None:
            return
        if token_project_id != project_id:
            raise HTTPException_NO_PERMISSION
