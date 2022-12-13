from pathlib import Path

import hyd.project.service as project_service
from fastapi.staticfiles import StaticFiles
from hyd.util.const import PATH_PROJECTS
from hyd.util.logger import HydLogger
from hyd.util.models import NameStr, PrimaryKey
from hyd.version.models import VersionEntry
from sqlalchemy.orm import Session
from starlette.routing import BaseRoute, Router

LOGGER = HydLogger("MountHelper")

####################################################################################################
#### MountHelper
####################################################################################################


class MountHelper:
    router: Router

    url_route_mapping: dict[str, BaseRoute] = {}

    @classmethod
    def set_router(cls, router: Router) -> None:
        cls.router = router

    @classmethod
    def mount_version(cls, version_entry: VersionEntry) -> None:
        id = version_entry.project_entry.id
        name = version_entry.project_entry.name
        vers = version_entry.ver_str

        relativ_url = _relative_url(name, vers)
        path = path_to_version(id, vers)

        cls.router.mount(relativ_url, StaticFiles(directory=path, html=True))
        cls.url_route_mapping[relativ_url] = cls.router.routes[-1]

        LOGGER.info("%s -> %s", relativ_url, path)

    @classmethod
    def unmount_version(cls, project_name: NameStr, ver_str: NameStr) -> None:
        relativ_url = _relative_url(project_name, ver_str)

        route = cls.url_route_mapping[relativ_url]
        cls.router.routes.remove(route)

    @classmethod
    def mount_existing_projects(cls, *, db: Session):
        project_entries = project_service.read_projects(db=db)

        for project_entry in project_entries:
            for version_entry in project_entry.version_entries:
                cls.mount_version(version_entry=version_entry)


####################################################################################################
#### Util
####################################################################################################


def path_to_version(project_id: PrimaryKey, ver_str: NameStr) -> Path:
    return PATH_PROJECTS / str(project_id) / ver_str


def _relative_url(name: str, ver_str: str) -> str:
    return f"/project/{name}/v/{ver_str}"
