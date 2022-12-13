from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from hyd.util.const import TEMPLATE_PATH, HTML_TITLE
from hyd.util.logger import HydLogger
from hyd.db import get_db
from hyd.project.models import ProjectEntry
import hyd.project.service as project_service
from hyd.util.models import NameStr

LOGGER = HydLogger("Frontend")

TEMPLATES = Jinja2Templates(directory=TEMPLATE_PATH)

frontend_router = APIRouter(tags=["frontend"])

####################################################################################################
#### Frontend Endpoints
####################################################################################################


@frontend_router.get("/", response_class=HTMLResponse)
async def frontend_landing(request: Request, db: Session = Depends(get_db)):

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
async def frontend_landing(
    request: Request, project_name: NameStr, db: Session = Depends(get_db)
):

    project_entries = project_service.read_project_by_name(
        project_name=project_name, db=db
    )
    if not project_entries:
        ...  # TODO raise

    project_entry = project_entries[0]

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
