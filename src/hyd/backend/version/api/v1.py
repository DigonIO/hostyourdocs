import io
import os
import shutil
import tarfile
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Security,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from hyd.backend.db import get_db
from hyd.backend.exc import HTTPException_UNKNOWN_VERSION, UnknownVersionError
from hyd.backend.mount_helper import MountHelper, path_to_version
from hyd.backend.security import Scopes
from hyd.backend.tag.models import TagEntry
from hyd.backend.user.authentication import authenticate_user
from hyd.backend.user.models import UserEntry
from hyd.backend.util.const import HEADERS
from hyd.backend.util.logger import HydLogger
from hyd.backend.util.models import NameStr, PrimaryKey
from hyd.backend.version.models import (
    API_V1_DELETE__DELETE,
    API_V1_LIST__GET,
    API_V1_UPLOAD__POST,
    VersionEntry,
    VersionResponseSchema,
)
from hyd.backend.version.service import (
    create_version,
    delete_version_by_ref,
    read_version,
    read_versions,
)

LOGGER = HydLogger("VersionAPI")

v1_router = APIRouter(tags=["version"])

####################################################################################################
#### HTTP Exceptions
####################################################################################################

HTTPException_EMPTY_FILE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The uploaded file has no content!",
    headers=HEADERS,
)

####################################################################################################
#### Scope: VERSION
####################################################################################################


@v1_router.post("/upload", responses=API_V1_UPLOAD__POST)
async def _upload(
    file: UploadFile,
    project_id: PrimaryKey = Form(...),
    version: NameStr = Form(...),
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.VERSION]),
):
    user_entry.check_token_project_permission(project_id=project_id)

    version_entry = _version_upload(file=file, project_id=project_id, version=version, db=db)

    project_entry = version_entry.project_entry
    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, project_id: %d, project_name: %s, version: %s}",
        user_entry.session_token_entry.id,
        user_entry.id,
        user_entry.username,
        project_entry.id,
        project_entry.name,
        version,
    )
    return _version_entry_to_response_schema(version_entry)


@v1_router.get("/list", responses=API_V1_LIST__GET)
async def _list(
    project_id: PrimaryKey,
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.VERSION]),
):
    version_entries = read_versions(project_id=project_id, db=db)
    return [_version_entry_to_response_schema(entry) for entry in version_entries]


@v1_router.delete("/delete", responses=API_V1_DELETE__DELETE)
async def _delete(
    project_id: PrimaryKey,
    version: NameStr,
    db: Session = Depends(get_db),
    user_entry: UserEntry = Security(authenticate_user, scopes=[Scopes.VERSION]),
):
    user_entry.check_token_project_permission(project_id=project_id)

    try:
        version_entry = read_version(project_id=project_id, version=version, db=db)
    except UnknownVersionError:
        raise HTTPException_UNKNOWN_VERSION

    project_entry = version_entry.project_entry
    version_rm_mount_and_files(version_entry=version_entry, db=db)

    LOGGER.info(
        "{token_id: %d, user_id: %d, username: %s, project_id: %d, project_name: %s, version: %s}",
        user_entry.session_token_entry.id,
        user_entry.id,
        user_entry.username,
        project_entry.id,
        project_entry.name,
        version,
    )

    response = _version_entry_to_response_schema(version_entry)
    delete_version_by_ref(version_entry=version_entry, db=db)
    return response


####################################################################################################
#### Util
####################################################################################################


def version_rm_mount_and_files(*, version_entry: VersionEntry, db: Session) -> None:
    id = version_entry.project_id
    name = version_entry.project_entry.name
    version = version_entry.version

    MountHelper.unmount_version(project_name=name, version=version)

    tag_entries: list[TagEntry] = version_entry.tag_entries
    for entry in tag_entries:
        if entry.version:
            MountHelper.unmount_tag(project_name=name, tag=entry.tag)
            entry.version = None
    db.commit()

    target = path_to_version(id, version)
    shutil.rmtree(target)  # Delete doc files from disc


def _version_entry_to_response_schema(version_entry: VersionEntry) -> VersionResponseSchema:
    tag_entries: list[TagEntry] = version_entry.tag_entries

    return VersionResponseSchema(
        project_id=version_entry.project_id,
        version=version_entry.version,
        created_at=version_entry.created_at,
        tags=[t_entry.tag for t_entry in tag_entries],
    )


def _version_upload(
    *, file: UploadFile, project_id: PrimaryKey, version: NameStr, db: Session
) -> VersionEntry:

    file_content = file.file.read()
    if not file_content:
        raise HTTPException_EMPTY_FILE

    version_entry = create_version(
        project_id=project_id,
        version=version,
        filename=file.filename,
        content_type=file.content_type,
        db=db,
    )

    # Extract doc files to disc
    file_like_object = io.BytesIO(file_content)
    tar = tarfile.open(fileobj=file_like_object, mode="r:gz")
    target = path_to_version(version_entry.project_id, version_entry.version)
    os.makedirs(target, exist_ok=True)
    tar.extractall(target)

    _inject_js_loader_to_html(dir_path=target)

    MountHelper.mount_version(version_entry=version_entry)

    return version_entry


_LOADER_HTML_INJECTION = """

<!-- Injected by HostYourDocs -->
<script src="/footer/loader.js"></script>
"""


def _inject_js_loader_to_html(*, dir_path: Path) -> None:
    html_files: list[Path] = []
    _recursiv_html_file_search(dir_path=dir_path, html_files=html_files)

    for file in html_files:
        with open(file, "a") as handle:
            handle.write(_LOADER_HTML_INJECTION)


def _recursiv_html_file_search(*, dir_path: Path, html_files: list[Path]) -> None:
    for entry in dir_path.iterdir():
        if entry.is_dir():
            _recursiv_html_file_search(dir_path=entry, html_files=html_files)
        elif entry.is_file() and entry.suffix == ".html":
            html_files.append(entry)
