import shutil
from pathlib import Path

from fastapi import APIRouter, Depends
from hyd.db import get_db
from hyd.project.service import (
    create_project,
    delete_project_by_ref,
    read_project,
    read_projects,
)
from hyd.util.const import PATH_PROJECTS
from hyd.util.logger import HydLogger
from hyd.util.models import NameStr, PrimaryKey
from hyd.version.api.v1 import version_rm_mount_and_files
from sqlalchemy.orm import Session

LOGGER = HydLogger("ProjectAPI")

v1_router = APIRouter(tags=["project"])

####################################################################################################
#### Scope: PROJECT
####################################################################################################


@v1_router.get("/list")
async def api_list(db: Session = Depends(get_db)):
    project_entries = read_projects(db=db)
    return project_entries


@v1_router.get("/get")
async def api_list(project_id: PrimaryKey, db: Session = Depends(get_db)):
    project_entries = read_project(project_id=project_id, db=db)
    return project_entries


@v1_router.post("/create")
async def api_create(name: NameStr, db: Session = Depends(get_db)):
    project_entry = create_project(name=name, db=db)
    return project_entry


@v1_router.post("/delete")
async def api_delete(project_id: PrimaryKey, db: Session = Depends(get_db)):
    project_entry = read_project(project_id=project_id, db=db)

    for version_entry in project_entry.version_entries:
        version_rm_mount_and_files(version_entry=version_entry, db=db)

    delete_project_by_ref(project_entry=project_entry, db=db)

    shutil.rmtree(_path_to_project(project_id))

    return project_entry


####################################################################################################
#### Util
####################################################################################################


def _path_to_project(project_id: PrimaryKey) -> Path:
    return PATH_PROJECTS / str(project_id)
