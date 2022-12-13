import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from hyd.project.models import VersionEntry
import hyd.project.service as project_service
from hyd.util.logger import HydLogger

LOGGER = HydLogger("MountHelper")


class MountHelper:
    app: FastAPI

    @classmethod
    def set_app(cls, app: FastAPI) -> None:
        cls.app = app

    @classmethod
    def mount_version(cls, version_entry: VersionEntry) -> None:
        id = version_entry.project_entry.id
        name = version_entry.project_entry.name
        vers = version_entry.ver_str

        relativ_url = f"/project/{name}/v/{vers}"
        path = f"data/projects/{id}/{vers}"

        cls.app.mount(relativ_url, StaticFiles(directory=path, html=True))
        LOGGER.info("Add: %s -> %s", relativ_url, path)

    @classmethod
    def mount_existing_projects(cls, *, db: Session):
        project_entries = project_service.read_projects(db=db)

        for project_entry in project_entries:
            for version_entry in project_entry.version_entries:
                cls.mount_version(version_entry=version_entry)
