from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, relationship

from hyd.backend.db import EXTEND_EXISTING, DeclarativeMeta
from hyd.backend.project.models import ProjectEntry
from hyd.backend.util.const import MAX_LENGTH_STR_ID
from hyd.backend.util.models import NameStr, PrimaryKey, TimeStampMixin
from hyd.backend.version.models import VersionEntry


class TagEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "tag_table"
    __table_args__ = (
        ForeignKeyConstraint(
            ["project_id", "version"], [VersionEntry.project_id, VersionEntry.version]
        ),
        {"extend_existing": EXTEND_EXISTING},
    )
    project_id: Mapped[PrimaryKey] = Column(Integer, ForeignKey(ProjectEntry.id), primary_key=True)
    version: Mapped[NameStr] = Column(String(length=MAX_LENGTH_STR_ID), nullable=True, default=None)

    tag: Mapped[NameStr] = Column(String(length=MAX_LENGTH_STR_ID), primary_key=True)
    primary: Mapped[bool] = Column(Boolean)  # primary == False will be marked as copy for google

    project_entry: Mapped[ProjectEntry] = relationship(
        ProjectEntry, back_populates="tag_entries", viewonly=True
    )
    version_entry: Mapped[VersionEntry] = relationship(
        VersionEntry, back_populates="tag_entries", viewonly=True
    )
    # no cascade="delete" because delete has to be done manually to remove files from disc


class PrimaryTagEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "primary_tag_table"
    __table_args__ = (
        ForeignKeyConstraint(["project_id", "primary_tag"], [TagEntry.project_id, TagEntry.tag]),
        {"extend_existing": EXTEND_EXISTING},
    )

    project_id: Mapped[PrimaryKey] = Column(Integer, primary_key=True)
    primary_tag: Mapped[NameStr] = Column(String(length=MAX_LENGTH_STR_ID))


#
