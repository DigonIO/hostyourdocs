from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from hyd.util.const import MAX_LENGTH_STR_ID
from hyd.db import EXTEND_EXISTING, DeclarativeMeta
from hyd.util.models import TimeStampMixin


class ProjectEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "project_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}

    id: Mapped[int] = Column(Integer, primary_key=True)
    name = Column(String(length=MAX_LENGTH_STR_ID), unique=True)

    version_entries: Mapped[list["VersionEntry"]] = relationship(
        "VersionEntry", back_populates="project_entry", cascade="all,delete"
    )
