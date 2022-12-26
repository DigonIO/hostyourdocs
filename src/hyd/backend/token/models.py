import datetime as dt

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, Session, relationship

from hyd.backend.db import EXTEND_EXISTING, DeclarativeMeta
from hyd.backend.util.const import (
    LOGIN_DURATION_AFTER_LAST_REQUEST,
    MAX_LENGTH_TOKEN_SCOPE,
    SRV_TIMEZONE,
)
from hyd.backend.util.models import PrimaryKey, TimeStampMixin


class TokenMetaSchema(BaseModel):
    token_id: PrimaryKey
    user_id: PrimaryKey
    expires_on: dt.datetime | None
    is_login_token: bool
    is_expired: bool
    revoked_at: dt.datetime | None
    scopes: list[str]
    project_id: PrimaryKey | None


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "token_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    expires_on = Column(DateTime(timezone=True), nullable=True)
    is_expired = Column(Boolean, default=False)
    last_request = Column(DateTime(timezone=True), default=dt.datetime.now(tz=SRV_TIMEZONE))
    is_login_token = Column(Boolean)
    revoked_at = Column(DateTime(timezone=True), nullable=True, default=None)
    project_id: Mapped[PrimaryKey] = Column(Integer, ForeignKey("project_table.id"), nullable=True)

    scope_entries: Mapped[list["TokenScopeEntry"]] = relationship(
        "TokenScopeEntry", back_populates="token_entry", cascade="all,delete"
    )
    user_entry: Mapped["UserEntry"] = relationship("UserEntry", back_populates="token_entries")

    def check_expiration(self, *, db: Session) -> bool:
        if self.is_expired:
            return True

        if self.is_login_token:
            # graciously expire token after expiration datetime is reached
            # and the last request is older than a given threshold
            import pdb

            pdb.set_trace()
            if dt.datetime.now(tz=SRV_TIMEZONE) < self.expires_on:
                return False
            if LOGIN_DURATION_AFTER_LAST_REQUEST < (
                dt.datetime.now(tz=SRV_TIMEZONE) - self.last_request
            ):
                self.is_expired = True
                db.commit()
                return True
        else:
            # expire token after the given datetime is reached
            if self.expires_on is None:
                return False

            if self.expires_on <= dt.datetime.now(tz=SRV_TIMEZONE):
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
