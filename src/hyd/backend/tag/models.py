import datetime as dt
from typing import TypedDict

from fastapi import status
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
from hyd.backend.util.models import (
    BASE_API_RESPONSE_SCHEMA,
    DETAIL_STR,
    NameStr,
    PrimaryKey,
    TimeStampMixin,
)
from hyd.backend.version.models import VersionEntry

####################################################################################################
#### SQLAlchemy table definitions
####################################################################################################


class TagEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "tag_table"
    __table_args__ = (
        ForeignKeyConstraint(
            ["project_id", "version"], [VersionEntry.project_id, VersionEntry.version]
        ),
        {"extend_existing": EXTEND_EXISTING},
    )
    project_id: Mapped[PrimaryKey] = Column(Integer, ForeignKey(ProjectEntry.id), primary_key=True)
    version: Mapped[NameStr | None] = Column(
        String(length=MAX_LENGTH_STR_ID), nullable=True, default=None
    )

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


####################################################################################################
#### Response schema
####################################################################################################


class TagResponseSchema(TypedDict):
    project_id: PrimaryKey
    tag: NameStr
    created_at: dt.datetime
    updated_at: dt.datetime | None
    version: NameStr | None
    primary: bool


####################################################################################################
#### OpenAPI definitions
####################################################################################################


API_V1_CREATE__POST = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": TagResponseSchema},
    status.HTTP_400_BAD_REQUEST: DETAIL_STR,
}


API_V1_LIST__GET = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": list[TagResponseSchema]},
}


API_V1_MOVE__PATCH = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": TagResponseSchema},
    status.HTTP_400_BAD_REQUEST: DETAIL_STR,
}


API_V1_DELETE__DELETE = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": TagResponseSchema},
    status.HTTP_400_BAD_REQUEST: DETAIL_STR,
}
