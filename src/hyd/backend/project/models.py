import datetime as dt
from typing import TypedDict

from fastapi import status
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from hyd.backend.db import EXTEND_EXISTING, DeclarativeMeta
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


####################################################################################################
#### Response schema
####################################################################################################


class ProjectResponseSchema(TypedDict):
    id: PrimaryKey
    name: NameStr
    created_at: dt.datetime
    versions: list[NameStr]
    tags: list[NameStr]


####################################################################################################
#### OpenAPI definitions
####################################################################################################


API_V1_CREATE__POST = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": ProjectResponseSchema},
    status.HTTP_400_BAD_REQUEST: DETAIL_STR,
}


API_V1_LIST__GET = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": list[ProjectResponseSchema]},
}


API_V1_GET__GET = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": ProjectResponseSchema},
    status.HTTP_400_BAD_REQUEST: DETAIL_STR,
}


API_V1_DELETE__DELETE = {
    **BASE_API_RESPONSE_SCHEMA,
    status.HTTP_200_OK: {"model": ProjectResponseSchema},
    status.HTTP_400_BAD_REQUEST: DETAIL_STR,
}
