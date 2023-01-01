import shutil
from pathlib import Path
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session

from hyd.backend.db import get_db
from hyd.backend.exc import (
    HTTPException_UNKNOWN_PROJECT,
    NameStrError,
    UnknownProjectError,
)
from hyd.backend.project.service import (
    create_project,
    delete_project_by_ref,
    read_project,
    read_projects,
)
from hyd.backend.security import Scopes
from hyd.backend.user.authentication import authenticate_user
from hyd.backend.user.models import UserEntry
from hyd.backend.util.const import HEADERS, PATH_PROJECTS
from hyd.backend.util.logger import HydLogger
from hyd.backend.util.models import NameStr, PrimaryKey
from hyd.backend.version.api.v1 import version_rm_mount_and_files

LOGGER = HydLogger("ProjectAPI")

v1_router = APIRouter(tags=["project"])

####################################################################################################
#### HTTP Exceptions
####################################################################################################

HTTPException_PROJECT_NAME_NOT_AVAILABLE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Project name not available!",
    headers=HEADERS,
)

####################################################################################################
#### Scope: PROJECT
####################################################################################################


@v1_router.post("/create")
async def _create(
    name: NameStr,
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.PROJECT]),
):
    try:
        project_entry = create_project(name=name, db=db)
    except NameStrError:
        raise HTTPException_PROJECT_NAME_NOT_AVAILABLE

    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, project_id: %d, project_name: %s}",
        user_entry.session_token_entry.id,
        user_entry.id,
        user_entry.username,
        project_entry.id,
        name,
    )
    return project_entry


@v1_router.get("/list")
async def _list(
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.PROJECT]),
):
    project_entries = read_projects(db=db)
    return project_entries


@v1_router.get("/get")
async def _get(
    project_id: Union[int, str],
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.PROJECT]),
):
    user_entry.check_token_project_permission(project_id=project_id)
    try:
        return read_project(project_id=project_id, db=db)
    except UnknownProjectError:
        raise HTTPException_UNKNOWN_PROJECT


@v1_router.post("/delete")
async def _delete(
    project_id: PrimaryKey,
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.PROJECT]),
):
    user_entry.check_token_project_permission(project_id=project_id)

    try:
        project_entry = read_project(project_id=project_id, db=db)
    except UnknownProjectError:
        raise HTTPException_UNKNOWN_PROJECT

    for version_entry in project_entry.version_entries:
        version_rm_mount_and_files(version_entry=version_entry, db=db)

    delete_project_by_ref(project_entry=project_entry, db=db)

    shutil.rmtree(_path_to_project(project_id))

    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, project_id: %d, project_name: %s}",
        user_entry.session_token_entry.id,
        user_entry.id,
        user_entry.username,
        project_entry.id,
        project_entry.name,
    )
    return project_entry


####################################################################################################
#### Util
####################################################################################################


def _path_to_project(project_id: PrimaryKey) -> Path:
    return PATH_PROJECTS / str(project_id)
