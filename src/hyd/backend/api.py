from fastapi import APIRouter
from hyd.backend.project.api.v1 import v1_router as v1_router_project
from hyd.backend.tag.api.v1 import v1_router as v1_router_tag
from hyd.backend.token.api.v1 import v1_router as v1_router_token
from hyd.backend.user.api.v1 import v1_router as v1_router_user
from hyd.backend.version.api.v1 import v1_router as v1_router_version

v1_router = APIRouter()
v1_router.include_router(v1_router_token, prefix="/token")
v1_router.include_router(v1_router_user, prefix="/user")
v1_router.include_router(v1_router_project, prefix="/project")
v1_router.include_router(v1_router_version, prefix="/version")
v1_router.include_router(v1_router_tag, prefix="/tag")

api_router = APIRouter()
api_router.include_router(v1_router, prefix="/v1")
