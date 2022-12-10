from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from hyd.project.models import VersionEntry


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
        cls.app.mount(
            f"/project/{name}/v/{vers}",
            StaticFiles(directory=f"data/projects/{id}/{vers}", html=True),
        )
