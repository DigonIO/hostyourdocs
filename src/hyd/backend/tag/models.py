from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from hyd.backend.db import EXTEND_EXISTING, DeclarativeMeta
from hyd.backend.project.models import ProjectEntry
from hyd.backend.util.const import MAX_LENGTH_STR_ID
from hyd.backend.util.models import NameStr, TimeStampMixin
from hyd.backend.version.models import VersionEntry


class TagEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "tag_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}
    project_id: Mapped[int] = Column(Integer, ForeignKey("project_table.id"), primary_key=True)
    tag = Column(String(length=MAX_LENGTH_STR_ID), primary_key=True)
    primary: Mapped[bool] = Column(Boolean)  # primary == False will be marked as copy for google
    version = Column(
        String(length=MAX_LENGTH_STR_ID),
        ForeignKey("version_table.version"),
        nullable=True,
        default=None,
    )

    project_entry: Mapped[ProjectEntry] = relationship("ProjectEntry", back_populates="tag_entries")
    version_entry: Mapped[VersionEntry] = relationship(
        "VersionEntry", back_populates="tag_entries"
    )  # no cascade="delete" because delete has to be done manually to remove files from disc


class PrimaryTagEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "primary_tag_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}

    project_id: Mapped[int] = Column(Integer, ForeignKey("project_table.id"), primary_key=True)
    primary_tag: Mapped[NameStr] = Column(String, ForeignKey("tag_table.tag"))
