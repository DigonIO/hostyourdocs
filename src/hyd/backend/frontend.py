from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import hyd.backend.project.service as project_service
from hyd.backend.db import get_db
from hyd.backend.project.models import ProjectEntry
from hyd.backend.tag.models import TagEntry
from hyd.backend.util.const import HTML_TITLE, TEMPLATE_PATH
from hyd.backend.util.logger import HydLogger
from hyd.backend.util.models import NameStr
from hyd.backend.version.models import VersionEntry

LOGGER = HydLogger("Frontend")

TEMPLATES = Jinja2Templates(directory=TEMPLATE_PATH)

frontend_router = APIRouter(tags=["frontend"])

####################################################################################################
#### Frontend Endpoints
####################################################################################################


@frontend_router.get("/", response_class=HTMLResponse)
async def frontend_simple(request: Request, db: Session = Depends(get_db)):

    project_entries = project_service.read_projects(db=db)

    return TEMPLATES.TemplateResponse(
        "simple.html",
        {
            "request": request,
            "html_title": HTML_TITLE,
            "projects": [entry.name for entry in project_entries],
        },
    )


@frontend_router.get("/{project_name}", response_class=HTMLResponse)
async def frontend_project(request: Request, project_name: NameStr, db: Session = Depends(get_db)):

    project_entry = project_service.read_project_by_name(project_name=project_name, db=db)

    return TEMPLATES.TemplateResponse(
        "project.html",
        {
            "request": request,
            "html_title": HTML_TITLE,
            "project": project_to_dict(project_entry),
        },
    )


####################################################################################################
#### Util
####################################################################################################


def project_to_dict(project_entry: ProjectEntry) -> dict:
    name = project_entry.name
    tag_entries: list[TagEntry] = project_entry.tag_entries
    version_entries: list[VersionEntry] = project_entry.version_entries

    return {
        "name": name,
        "tags": [
            {"link": f"project/{name}/t/{entry.tag}", "tag": entry.tag}
            for entry in tag_entries
            if entry.version
        ],
        "versions": [
            {"link": f"project/{name}/v/{entry.version}", "version": entry.version}
            for entry in version_entries
        ],
    }
