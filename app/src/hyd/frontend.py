from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from hyd.util.const import TEMPLATE_PATH, HTML_TITLE
from hyd.util.logger import HydLogger

LOGGER = HydLogger("Frontend")

TEMPLATES = Jinja2Templates(directory=TEMPLATE_PATH)

frontend_router = APIRouter(tags=["frontend"])


@frontend_router.get("/", response_class=HTMLResponse)
@frontend_router.get("/index.html", response_class=HTMLResponse)
async def frontend_landing(request: Request):
    return TEMPLATES.TemplateResponse(
        "landing.html", {"request": request, "html_title": HTML_TITLE, "id": 1}
    )
