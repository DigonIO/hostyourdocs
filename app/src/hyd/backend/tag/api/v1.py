import io
import os
import tarfile

from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from hyd.db import get_db
from hyd.mount_helper import MountHelper
from hyd.project.models import ProjectEntry
from hyd.project.service import (
    create_project,
    create_version,
    delete_project,
    read_projects,
    read_versions,
)
from hyd.util.const import PATH_PROJECTS
from hyd.util.logger import HydLogger
from hyd.util.models import NameStr, PrimaryKey
from sqlalchemy.orm import Session

LOGGER = HydLogger("ProjectAPI")

v1_router = APIRouter(tags=["project"])

####################################################################################################
#### Scope: PROJECT
####################################################################################################


@v1_router.get("/list")
async def api_list(db: Session = Depends(get_db)):
    project_entries = await read_projects(db=db)
    return project_entries


@v1_router.post("/create")
async def api_create(name: NameStr, db: Session = Depends(get_db)):
    project_entry = await create_project(name=name, db=db)
    return project_entry


@v1_router.post("/delete")
async def api_delete(project_id: PrimaryKey, db: Session = Depends(get_db)):
    project_entry = await delete_project(project_id=project_id, db=db)
    return project_entry


@v1_router.get("/doc/list")
async def api_doc_list(db: Session = Depends(get_db)):
    version_entries = await read_versions(db=db)
    return version_entries


@v1_router.post("/doc/upload")
async def api_doc_upload(
    file: UploadFile,
    project_id: PrimaryKey = Form(...),
    ver_str: NameStr = Form(...),
    db: Session = Depends(get_db),
):

    file_content = file.file.read()
    if not file_content:
        raise HTTPException()  # TODO msg

    version_entry = await create_version(
        project_id=project_id,
        ver_str=ver_str,
        filename=file.filename,
        content_type=file.content_type,
        db=db,
    )

    file_like_object = io.BytesIO(file_content)
    tar = tarfile.open(fileobj=file_like_object, mode="r:gz")

    target = PATH_PROJECTS / str(project_id) / ver_str
    os.makedirs(target, exist_ok=True)

    tar.extractall(target)

    MountHelper.mount_version(version_entry=version_entry)

    return version_entry


@v1_router.post("/doc/delete")
async def api_doc_delete(request: Request):
    ...


@v1_router.get("/tag/list")
async def api_tag_list(request: Request):
    ...


@v1_router.post("/tag/create")
async def api_tag_create(request: Request):
    ...


@v1_router.post("/tag/delete")
async def api_tag_delete(request: Request):
    ...


@v1_router.post("/tag/set")
async def api_tag_set(request: Request):
    ...


@v1_router.post("/tag/unset")
async def api_tag_unset(request: Request):
    ...
