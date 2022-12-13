from hyd.db import EXTEND_EXISTING, DeclarativeMeta
from hyd.project.models import ProjectEntry
from hyd.util.const import MAX_LENGTH_STR_ID
from hyd.util.models import TimeStampMixin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship


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
