from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import hyd.backend.project.service as project_service
import hyd.backend.version.service as version_service
from hyd.backend.db import get_db
from hyd.backend.mount_helper import MountHelper
from hyd.backend.tag.service import (
    create_tag_entry,
    delete_tag_entry_by_ref,
    read_tag_entry,
)
from hyd.backend.util.logger import HydLogger
from hyd.backend.util.models import NameStr, PrimaryKey

LOGGER = HydLogger("TagAPI")

v1_router = APIRouter(tags=["tag"])

####################################################################################################
#### Scope: TAG
####################################################################################################


@v1_router.get("/list")
async def api_tag_list(project_id: PrimaryKey, db: Session = Depends(get_db)):
    project_entry = project_service.read_project(project_id=project_id, db=db)
    return project_entry.tag_entries


@v1_router.post("/create")
async def api_tag_create(
    project_id: PrimaryKey, tag: NameStr, primary: bool = False, db: Session = Depends(get_db)
):
    return create_tag_entry(project_id=project_id, tag=tag, primary=primary, db=db)


@v1_router.post("/delete")
async def api_tag_delete(project_id: PrimaryKey, tag: NameStr, db: Session = Depends(get_db)):
    tag_entry = read_tag_entry(project_id=project_id, tag=tag, db=db)
    if tag_entry.version is not None:
        MountHelper.unmount_tag(project_name=tag_entry.project_entry.name, tag=tag_entry.tag)
    delete_tag_entry_by_ref(tag_entry=tag_entry, db=db)
    return tag_entry


@v1_router.post("/move")
async def api_tag_set(
    project_id: PrimaryKey, tag: NameStr, version: NameStr, db: Session = Depends(get_db)
):
    tag_entry = read_tag_entry(project_id=project_id, tag=tag, db=db)
    _ = version_service.read_version(project_id=project_id, version=version, db=db)  # TODO needed?

    if tag_entry.version is not None:
        MountHelper.unmount_tag(project_name=tag_entry.project_entry.name, tag=tag_entry.tag)

    tag_entry.version = version
    db.commit()

    MountHelper.mount_tag(tag_entry=tag_entry)
    return tag_entry
