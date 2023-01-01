import datetime as dt
from typing import TypedDict

from fastapi import status
from sqlalchemy import Column, ForeignKey, Integer, String
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

####################################################################################################
#### SQLAlchemy table definitions
####################################################################################################


class VersionEntry(DeclarativeMeta, TimeStampMixin):
    __tablename__ = "version_table"
    __table_args__ = {"extend_existing": EXTEND_EXISTING}

    project_id: Mapped[PrimaryKey] = Column(
        Integer, ForeignKey("project_table.id"), primary_key=True
    )
    version: Mapped[NameStr] = Column(String(length=MAX_LENGTH_STR_ID), primary_key=True)

    filename: Mapped[NameStr] = Column(String(length=MAX_LENGTH_STR_ID))
    content_type: Mapped[NameStr] = Column(String(length=MAX_LENGTH_STR_ID))

    project_entry: Mapped[ProjectEntry] = relationship(
        "ProjectEntry", back_populates="version_entries"
    )

    tag_entries: Mapped[list["TagEntry"]] = relationship(
        "TagEntry", back_populates="version_entry", viewonly=True
    )


####################################################################################################
#### Response schema
####################################################################################################


class VersionResponseSchema(TypedDict):
    project_id: PrimaryKey
    version: NameStr
    created_at: dt.datetime
    tags: list[NameStr]


####################################################################################################
#### OpenAPI definitions
####################################################################################################


API_V1_UPLOAD__POST = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": VersionResponseSchema},
    status.HTTP_400_BAD_REQUEST: DETAIL_STR,
}


API_V1_LIST__GET = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": list[VersionResponseSchema]},
}


API_V1_DELETE__DELETE = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": VersionResponseSchema},
    status.HTTP_400_BAD_REQUEST: DETAIL_STR,
}
