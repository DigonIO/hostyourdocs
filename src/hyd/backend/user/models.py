import datetime as dt
from typing import TypedDict

from fastapi import status
from sqlalchemy import Boolean, Column, Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, relationship

from hyd.backend.db import EXTEND_EXISTING, DeclarativeMeta
from hyd.backend.exc import HTTPException_NO_PERMISSION
from hyd.backend.token.models import TokenEntry, TokenSchema
from hyd.backend.util.const import MAX_LENGTH_STR_ID
from hyd.backend.util.models import (
    BASE_API_RESPONSE_SCHEMA,
    DETAIL_STR,
    NameStr,
    PrimaryKey,
    TimeStampMixin,
)

####################################################################################################
#### SQLAlchemy table definitions
####################################################################################################


class UserEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "user_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}
    id: Mapped[PrimaryKey] = Column(Integer, primary_key=True)
    username: Mapped[NameStr] = Column(String(length=MAX_LENGTH_STR_ID), unique=True)
    hashed_password: Mapped[bytes] = Column(LargeBinary)
    is_admin: Mapped[bool] = Column(Boolean)
    is_disabled: Mapped[bool] = Column(Boolean, default=False)

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


####################################################################################################
#### Response schema
####################################################################################################

# NOTE currently unused
class UserResponseSchema(TypedDict):
    id: PrimaryKey
    username: NameStr
    is_admin: bool
    is_disabled: bool
    created_at: dt.datetime


####################################################################################################
#### OpenAPI definitions
####################################################################################################


API_V1_LOGIN__POST = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": TokenSchema},
    status.HTTP_400_BAD_REQUEST: DETAIL_STR,
}


API_V1_LOGOUT__PATCH = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": str},
}

API_V1_CHANGE_PASSWORD__PATCH = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": str},
    status.HTTP_400_BAD_REQUEST: DETAIL_STR,
}


API_V1_GREET__GET = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": str},
}
