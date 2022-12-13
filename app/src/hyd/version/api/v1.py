import os
import io
import tarfile
import shutil

from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session

from hyd.util.logger import HydLogger
from hyd.util.models import NameStr, PrimaryKey
from hyd.db import get_db
from hyd.version.service import (
    create_version,
    read_versions,
    read_version,
    delete_version_by_ref,
)
from hyd.version.models import VersionEntry
from hyd.mount_helper import MountHelper, path_to_version


LOGGER = HydLogger("VersionAPI")

v1_router = APIRouter(tags=["version"])

####################################################################################################
#### Scope: VERSION
####################################################################################################


@v1_router.get("/version/list")
async def api_version_list(project_id: PrimaryKey, db: Session = Depends(get_db)):
    version_entries = read_versions(project_id=project_id, db=db)
    return version_entries


@v1_router.post("/version/upload")
async def api_version_upload(
    file: UploadFile,
    project_id: PrimaryKey = Form(...),
    ver_str: NameStr = Form(...),
    db: Session = Depends(get_db),
):
    return _version_upload(file=file, project_id=project_id, ver_str=ver_str, db=db)


@v1_router.post("/version/delete")
async def api_version_delete(
    project_id: PrimaryKey, ver_str: NameStr, db: Session = Depends(get_db)
):
    version_entry = read_version(project_id=project_id, ver_str=ver_str, db=db)
    version_rm_mount_and_files(version_entry=version_entry, db=db)
    return version_entry


####################################################################################################
#### Util
####################################################################################################


def _version_upload(
    *, file: UploadFile, project_id: PrimaryKey, ver_str: NameStr, db: Session
) -> VersionEntry:

    file_content = file.file.read()
    if not file_content:
        raise HTTPException()  # TODO msg

    version_entry = create_version(
        project_id=project_id,
        ver_str=ver_str,
        filename=file.filename,
        content_type=file.content_type,
        db=db,
    )

    file_like_object = io.BytesIO(file_content)
    tar = tarfile.open(fileobj=file_like_object, mode="r:gz")
    target = path_to_version(version_entry.project_id, version_entry.ver_str)
    os.makedirs(target, exist_ok=True)
    tar.extractall(target)  # Create doc files on disc

    MountHelper.mount_version(version_entry=version_entry)

    return version_entry


def version_rm_mount_and_files(*, version_entry: VersionEntry, db: Session) -> None:
    id = version_entry.project_id
    name = version_entry.project_entry.name
    ver_str = version_entry.ver_str
    MountHelper.unmount_version(project_name=name, ver_str=ver_str)
    delete_version_by_ref(version_entry=version_entry, db=db)

    target = path_to_version(id, ver_str)
    shutil.rmtree(target)  # Delete doc files from disc
