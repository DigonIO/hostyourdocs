import datetime as dt

from fastapi import status
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, Session, relationship

from hyd.backend.db import EXTEND_EXISTING, DeclarativeMeta
from hyd.backend.util.const import (
    LOGIN_DURATION_AFTER_LAST_REQUEST,
    MAX_LENGTH_STR_COMMENT,
    MAX_LENGTH_TOKEN_SCOPE,
)
from hyd.backend.util.models import (
    BASE_API_RESPONSE_SCHEMA,
    DETAIL_STR,
    CommentStr,
    PrimaryKey,
    TimeStampMixin,
)

UTC = dt.timezone.utc


####################################################################################################
#### SQLAlchemy table definitions
####################################################################################################


class TokenEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "token_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}
    id: Mapped[PrimaryKey] = Column(Integer, primary_key=True)
    user_id: Mapped[PrimaryKey] = Column(Integer, ForeignKey("user_table.id"))
    is_login_token: Mapped[bool] = Column(Boolean)
    is_expired: Mapped[bool] = Column(Boolean, default=False)
    project_id: Mapped[PrimaryKey] = Column(Integer, ForeignKey("project_table.id"), nullable=True)
    _expires_on: Mapped[dt.datetime] = Column(DateTime, nullable=True)
    _last_request: Mapped[dt.datetime] = Column(DateTime, default=dt.datetime.utcnow)
    _revoked_at: Mapped[dt.datetime] = Column(DateTime, nullable=True, default=None)
    comment: Mapped[CommentStr] = Column(String(length=MAX_LENGTH_STR_COMMENT))

    scope_entries: Mapped[list["TokenScopeEntry"]] = relationship(
        "TokenScopeEntry", back_populates="token_entry", cascade="all,delete"
    )
    user_entry: Mapped["UserEntry"] = relationship("UserEntry", back_populates="token_entries")

    @property
    def expires_on(self) -> dt.datetime | None:
        return None if self._expires_on is None else self._expires_on.replace(tzinfo=UTC)

    @expires_on.setter
    def expires_on(self, val: dt.datetime) -> None:
        self._expires_on = val

    @property
    def last_request(self) -> dt.datetime:
        return self._last_request.replace(tzinfo=UTC)

    @last_request.setter
    def last_request(self, val: dt.datetime) -> None:
        self._last_request = val

    @property
    def revoked_at(self) -> dt.datetime | None:
        return None if self._revoked_at is None else self._revoked_at.replace(tzinfo=UTC)

    @revoked_at.setter
    def revoked_at(self, val: dt.datetime) -> None:
        self._revoked_at = val

    def check_expiration(self, *, db: Session) -> bool:
        if self.is_expired:
            return True

        if self.is_login_token:
            # graciously expire token after expiration datetime is reached
            # and the last request is older than a given threshold

            if dt.datetime.now(tz=UTC) < self.expires_on:
                return False
            if LOGIN_DURATION_AFTER_LAST_REQUEST < (dt.datetime.now(tz=UTC) - self.last_request):
                self.is_expired = True
                db.commit()
                return True
        else:
            # expire token after the given datetime is reached
            if self.expires_on is None:
                return False

            if self.expires_on <= dt.datetime.now(tz=UTC):
                self.is_expired = True
                db.commit()
                return True

        return False


class TokenScopeEntry(DeclarativeMeta):
    __tablename__ = "scope_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}
    id = Column(Integer, primary_key=True)
    token_id = Column(Integer, ForeignKey("token_table.id"))
    scope = Column(String(length=MAX_LENGTH_TOKEN_SCOPE))

    token_entry = relationship("TokenEntry", back_populates="scope_entries")


####################################################################################################
#### Response schema
####################################################################################################


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenResponseSchema(BaseModel):
    token_id: PrimaryKey
    user_id: PrimaryKey
    created_at: dt.datetime
    revoked_at: dt.datetime | None
    expires_on: dt.datetime | None
    is_expired: bool
    is_login_token: bool
    scopes: list[str]
    project_id: PrimaryKey | None
    comment: str


class FullTokenResponseSchema(TokenSchema, TokenResponseSchema):
    ...


####################################################################################################
#### OpenAPI definitions
####################################################################################################


API_V1_CREATE__POST = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": FullTokenResponseSchema},
    status.HTTP_400_BAD_REQUEST: DETAIL_STR,
}


API_V1_LIST__GET = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": list[TokenResponseSchema]},
}


API_V1_REVOKE__PATCH = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": TokenResponseSchema},
    status.HTTP_400_BAD_REQUEST: DETAIL_STR,
}
