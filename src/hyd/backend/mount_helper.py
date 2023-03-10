from pathlib import Path

from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.routing import BaseRoute, Router

import hyd.backend.project.service as project_service
from hyd.backend.tag.models import TagEntry
from hyd.backend.util.const import PATH_PROJECTS
from hyd.backend.util.logger import HydLogger
from hyd.backend.util.models import NameStr, PrimaryKey
from hyd.backend.version.models import VersionEntry

LOGGER = HydLogger("MountHelper")

####################################################################################################
#### MountHelper
####################################################################################################


class MountHelper:
    router: Router

    url_route_mapping: dict[str, tuple[Path, BaseRoute]] = {}

    @classmethod
    def set_router(cls, router: Router) -> None:
        cls.router = router

    @classmethod
    def mount_version(cls, version_entry: VersionEntry) -> None:
        id = version_entry.project_id
        name = version_entry.project_entry.name
        vers = version_entry.version

        relative_url = _relative_version_url(name, vers)
        path = path_to_version(id, vers)

        cls.router.mount(relative_url, StaticFiles(directory=path, html=True))
        cls.url_route_mapping[relative_url] = (path, cls.router.routes[-1])

        LOGGER.debug("%s --> %s", relative_url, path)

    @classmethod
    def unmount_version(cls, project_name: NameStr, version: NameStr) -> None:
        relative_url = _relative_version_url(project_name, version)

        path, route = cls.url_route_mapping[relative_url]
        cls.router.routes.remove(route)

        LOGGER.debug("%s -x- %s", relative_url, path)

    @classmethod
    def mount_tag(cls, tag_entry: TagEntry) -> None:
        id = tag_entry.project_id
        tag = tag_entry.tag
        name = tag_entry.project_entry.name
        version = tag_entry.version

        relative_url = _relative_tag_url(name, tag)
        path = path_to_version(id, version)

        cls.router.mount(relative_url, StaticFiles(directory=path, html=True))
        cls.url_route_mapping[relative_url] = (path, cls.router.routes[-1])

        LOGGER.debug("%s --> %s", relative_url, path)

    @classmethod
    def unmount_tag(cls, project_name: NameStr, tag: NameStr) -> None:
        relative_url = _relative_tag_url(project_name, tag)

        path, route = cls.url_route_mapping[relative_url]
        cls.router.routes.remove(route)

        LOGGER.debug("%s -x- %s", relative_url, path)

    @classmethod
    def mount_existing_projects(cls, *, db: Session) -> None:
        project_entries = project_service.read_projects(db=db)

        for project_entry in project_entries:

            version_entries: list[VersionEntry] = project_entry.version_entries
            for version_entry in version_entries:
                cls.mount_version(version_entry=version_entry)

            tag_entries: list[TagEntry] = project_entry.tag_entries
            for tag_entry in tag_entries:
                if tag_entry.version:
                    cls.mount_tag(tag_entry=tag_entry)


####################################################################################################
#### Util
####################################################################################################


def path_to_version(project_id: PrimaryKey, version: NameStr) -> Path:
    return PATH_PROJECTS / str(project_id) / version


def _relative_version_url(name: str, version: str) -> str:
    return f"/project/{name}/v/{version}"


def _relative_tag_url(name: str, tag: str) -> str:
    return f"/project/{name}/t/{tag}"
