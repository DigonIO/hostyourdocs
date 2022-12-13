from hyd.db import EXTEND_EXISTING, DeclarativeMeta
from hyd.util.const import MAX_LENGTH_STR_ID
from hyd.util.models import TimeStampMixin
from sqlalchemy import Boolean, Column, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, relationship


class ProjectEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "project_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}

    id: Mapped[int] = Column(Integer, primary_key=True)
    name = Column(String(length=MAX_LENGTH_STR_ID), unique=True)

    version_entries: Mapped[list["VersionEntry"]] = relationship(
        "VersionEntry", back_populates="project_entry"
    )


class VersionEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "version_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}

    project_id: Mapped[int] = Column(Integer, ForeignKey("project_table.id"), primary_key=True)
    ver_str = Column(String(length=MAX_LENGTH_STR_ID), primary_key=True)

    filename = Column(String(length=MAX_LENGTH_STR_ID))
    content_type = Column(String(length=MAX_LENGTH_STR_ID))

    project_entry: Mapped[ProjectEntry] = relationship(
        "ProjectEntry", back_populates="version_entries"
    )


# class TagEntry(DeclarativeMeta, TimeStampMixin):
#    __tablename__ = "tag_table"
#    __table_args__ = {"extend_existing": EXTEND_EXISTING}
#
#    project_id: Mapped[int] = Column(
#        Integer, ForeignKey("project_table.id"), primary_key=True
#    )
#    tag_str = Column(
#        String(length=MAX_LENGTH_STR_ID),
#        ForeignKey("project_table.id"),
#        primary_key=True,
#    )
#    ver_str = Column(
#        String(length=MAX_LENGTH_STR_ID),
#        ForeignKey("version_table.ver_str"),
#        nullable=True,
#        default=None,
#    )
#
