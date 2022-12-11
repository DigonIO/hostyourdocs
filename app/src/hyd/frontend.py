from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from hyd.util.const import TEMPLATE_PATH, HTML_TITLE
from hyd.util.logger import HydLogger
from hyd.db import get_db
from hyd.project.models import ProjectEntry
import hyd.project.service as project_service

LOGGER = HydLogger("Frontend")

TEMPLATES = Jinja2Templates(directory=TEMPLATE_PATH)

frontend_router = APIRouter(tags=["frontend"])

####################################################################################################
#### Frontend Endpoints
####################################################################################################


@frontend_router.get("/", response_class=HTMLResponse)
@frontend_router.get("/index.html", response_class=HTMLResponse)
async def frontend_landing(request: Request, db: Session = Depends(get_db)):

    project_entries = await project_service.read_projects(db=db)

    return TEMPLATES.TemplateResponse(
        "landing.html",
        {
            "request": request,
            "html_title": HTML_TITLE,
            "projects": [project_to_dict(entry) for entry in project_entries],
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
