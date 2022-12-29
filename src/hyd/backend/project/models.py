from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from hyd.backend.db import EXTEND_EXISTING, DeclarativeMeta
from hyd.backend.util.const import MAX_LENGTH_STR_ID
from hyd.backend.util.models import NameStr, PrimaryKey, TimeStampMixin


class ProjectEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "project_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}

    id: Mapped[PrimaryKey] = Column(Integer, primary_key=True)
    name: Mapped[NameStr] = Column(String(length=MAX_LENGTH_STR_ID), unique=True)

    version_entries: Mapped[list["VersionEntry"]] = relationship(
        "VersionEntry", back_populates="project_entry"
    )  # no cascade="delete" because delete has to be done manually to remove files from disc

    tag_entries: Mapped[list["TagEntry"]] = relationship(
        "TagEntry", back_populates="project_entry", cascade="all,delete"
    )
