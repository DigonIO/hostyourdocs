from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from hyd.util.const import MAX_LENGTH_TOKEN_SCOPE
from hyd.db import EXTEND_EXISTING, DeclarativeMeta
from hyd.util.models import TimeStampMixin


class TokenEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "token_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    is_login_token = Column(Boolean)
    is_expired = Column(Boolean, default=False)

    scope_entries = relationship(
        "TokenScopeEntry", back_populates="token_entry", cascade="all,delete"
    )
    user_entry = relationship("UserEntry", back_populates="token_entries")


class TokenScopeEntry(DeclarativeMeta):
    __tablename__ = "scope_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}
    id = Column(Integer, primary_key=True)
    token_id = Column(Integer, ForeignKey("token_table.id"))
    scope = Column(String(length=MAX_LENGTH_TOKEN_SCOPE))

    token_entry = relationship("TokenEntry", back_populates="scope_entries")
