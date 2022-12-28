from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

import hyd.backend.project.service as project_service
import hyd.backend.version.service as version_service
from hyd.backend.db import get_db
from hyd.backend.mount_helper import MountHelper
from hyd.backend.security import Scopes
from hyd.backend.tag.service import (
    create_tag_entry,
    delete_tag_entry_by_ref,
    read_tag_entry,
)
from hyd.backend.user.authentication import authenticate_user
from hyd.backend.user.models import UserEntry
from hyd.backend.util.logger import HydLogger
from hyd.backend.util.models import NameStr, PrimaryKey

LOGGER = HydLogger("TagAPI")

v1_router = APIRouter(tags=["tag"])

####################################################################################################
#### Scope: TAG
####################################################################################################


@v1_router.post("/create")
async def _create(
    project_id: PrimaryKey,
    tag: NameStr,
    primary: bool = False,
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.PROJECT]),
):
    tag_entry = create_tag_entry(project_id=project_id, tag=tag, primary=primary, db=db)

    project_entry = tag_entry.project_entry
    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, project_id: %d, project_name: %s, tag: %s}",
        user_entry.get_session_token_entry().id,
        user_entry.id,
        user_entry.username,
        project_entry.id,
        project_entry.name,
        tag,
    )
    return tag_entry


@v1_router.get("/list")
async def _list(
    project_id: PrimaryKey,
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.PROJECT]),
):
    project_entry = project_service.read_project(project_id=project_id, db=db)
    return project_entry.tag_entries


@v1_router.post("/move")
async def _move(
    project_id: PrimaryKey,
    tag: NameStr,
    version: NameStr,
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.PROJECT]),
):
    user_entry.check_token_project_permission(project_id=project_id)

    tag_entry = read_tag_entry(project_id=project_id, tag=tag, db=db)
    _ = version_service.read_version(project_id=project_id, version=version, db=db)  # TODO needed?

    if tag_entry.version is not None:
        MountHelper.unmount_tag(project_name=tag_entry.project_entry.name, tag=tag_entry.tag)

    tag_entry.version = version
    db.commit()

    MountHelper.mount_tag(tag_entry=tag_entry)

    project_entry = tag_entry.project_entry
    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, project_id: %d, project_name: %s, tag: %s, version: %s}",
        user_entry.get_session_token_entry().id,
        user_entry.id,
        user_entry.username,
        project_entry.id,
        project_entry.name,
        tag,
        version,
    )
    return tag_entry


@v1_router.post("/delete")
async def _delete(
    project_id: PrimaryKey,
    tag: NameStr,
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.PROJECT]),
):
    user_entry.check_token_project_permission(project_id=project_id)

    tag_entry = read_tag_entry(project_id=project_id, tag=tag, db=db)
    if tag_entry.version is not None:
        MountHelper.unmount_tag(project_name=tag_entry.project_entry.name, tag=tag_entry.tag)
    delete_tag_entry_by_ref(tag_entry=tag_entry, db=db)

    project_entry = tag_entry.project_entry
    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, project_id: %d, project_name: %s, tag: %s}",
        user_entry.get_session_token_entry().id,
        user_entry.id,
        user_entry.username,
        project_entry.id,
        project_entry.name,
        tag,
    )
    return tag_entry
