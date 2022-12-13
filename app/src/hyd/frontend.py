import hyd.project.service as project_service
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from hyd.db import get_db
from hyd.project.models import ProjectEntry
from hyd.util.const import HTML_TITLE, TEMPLATE_PATH
from hyd.util.logger import HydLogger
from hyd.util.models import NameStr
from sqlalchemy.orm import Session

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
    return {
        "name": name,
        "versions": [
            {"link": f"project/{name}/v/{entry.ver_str}", "ver_str": entry.ver_str}
            for entry in project_entry.version_entries
        ],
    }
