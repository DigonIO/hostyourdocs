from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session

import hyd.backend.project.service as project_service
import hyd.backend.version.service as version_service
from hyd.backend.db import get_db
from hyd.backend.exc import (
    HTTPException_UNKNOWN_PROJECT,
    HTTPException_UNKNOWN_VERSION,
    PrimaryTagError,
    UnknownProjectError,
    UnknownTagError,
    UnknownVersionError,
)
from hyd.backend.mount_helper import MountHelper
from hyd.backend.security import Scopes
from hyd.backend.tag.models import (
    API_V1_CREATE__POST,
    API_V1_DELETE__DELETE,
    API_V1_LIST__GET,
    API_V1_MOVE__PATCH,
    TagEntry,
    TagResponseSchema,
)
from hyd.backend.tag.service import (
    create_tag_entry,
    delete_tag_entry_by_ref,
    read_tag_entry,
)
from hyd.backend.user.authentication import authenticate_user
from hyd.backend.user.models import UserEntry
from hyd.backend.util.const import HEADERS
from hyd.backend.util.logger import HydLogger
from hyd.backend.util.models import NameStr, PrimaryKey

LOGGER = HydLogger("TagAPI")

v1_router = APIRouter(tags=["tag"])

####################################################################################################
#### HTTP Exceptions
####################################################################################################

HTTPException_PRIMARY_TAG = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Only one primary tag allowed!",
    headers=HEADERS,
)

HTTPException_UNKNOWN_TAG = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Unknown tag!",
    headers=HEADERS,
)


####################################################################################################
#### Scope: TAG
####################################################################################################


@v1_router.post("/create", responses=API_V1_CREATE__POST)
async def _create(
    project_id: PrimaryKey,
    tag: NameStr,
    primary: bool = False,
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.PROJECT]),
):
    try:
        tag_entry = create_tag_entry(project_id=project_id, tag=tag, primary=primary, db=db)
    except UnknownProjectError:
        raise HTTPException_UNKNOWN_PROJECT
    except PrimaryTagError:
        raise HTTPException_PRIMARY_TAG

    project_entry = tag_entry.project_entry
    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, project_id: %d, project_name: %s, tag: %s}",
        user_entry.session_token_entry.id,
        user_entry.id,
        user_entry.username,
        project_entry.id,
        project_entry.name,
        tag,
    )
    return _tag_entry_to_response_schema(tag_entry)


@v1_router.get("/list", responses=API_V1_LIST__GET)
async def _list(
    project_id: PrimaryKey,
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.PROJECT]),
):
    try:
        project_entry = project_service.read_project(project_id=project_id, db=db)
    except UnknownProjectError:
        raise HTTPException_UNKNOWN_PROJECT

    return [_tag_entry_to_response_schema(tag_entry) for tag_entry in project_entry.tag_entries]


@v1_router.patch("/move", responses=API_V1_MOVE__PATCH)
async def _move(
    project_id: PrimaryKey,
    tag: NameStr,
    version: NameStr,
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.PROJECT]),
):
    user_entry.check_token_project_permission(project_id=project_id)

    try:
        tag_entry = read_tag_entry(project_id=project_id, tag=tag, db=db)
    except UnknownProjectError:
        raise HTTPException_UNKNOWN_PROJECT
    except UnknownTagError:
        raise HTTPException_UNKNOWN_TAG

    # verify that the target version exists
    try:
        _ = version_service.read_version(project_id=project_id, version=version, db=db)
    except UnknownVersionError:
        raise HTTPException_UNKNOWN_VERSION

    # rm old mount point if one exists
    if tag_entry.version is not None:
        MountHelper.unmount_tag(project_name=tag_entry.project_entry.name, tag=tag_entry.tag)

    tag_entry.version = version
    db.commit()

    MountHelper.mount_tag(tag_entry=tag_entry)

    project_entry = tag_entry.project_entry
    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, project_id: %d, project_name: %s, tag: %s, version: %s}",
        user_entry.session_token_entry.id,
        user_entry.id,
        user_entry.username,
        project_entry.id,
        project_entry.name,
        tag,
        version,
    )
    return _tag_entry_to_response_schema(tag_entry)


@v1_router.delete("/delete", responses=API_V1_DELETE__DELETE)
async def _delete(
    project_id: PrimaryKey,
    tag: NameStr,
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.PROJECT]),
):
    user_entry.check_token_project_permission(project_id=project_id)

    try:
        tag_entry = read_tag_entry(project_id=project_id, tag=tag, db=db)
    except UnknownTagError:
        raise HTTPException_UNKNOWN_TAG

    # rm old mount point if one exists
    if tag_entry.version is not None:
        MountHelper.unmount_tag(project_name=tag_entry.project_entry.name, tag=tag_entry.tag)

    delete_tag_entry_by_ref(tag_entry=tag_entry, db=db)

    project_entry = tag_entry.project_entry
    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, project_id: %d, project_name: %s, tag: %s}",
        user_entry.session_token_entry.id,
        user_entry.id,
        user_entry.username,
        project_entry.id,
        project_entry.name,
        tag,
    )
    return _tag_entry_to_response_schema(tag_entry)


####################################################################################################
#### Util
####################################################################################################


def _tag_entry_to_response_schema(tag_entry: TagEntry) -> TagResponseSchema:
    return TagResponseSchema(
        project_id=tag_entry.project_id,
        tag=tag_entry.tag,
        created_at=tag_entry.created_at,
        updated_at=tag_entry.updated_at,
        version=tag_entry.version,
        primary=tag_entry.primary,
    )
