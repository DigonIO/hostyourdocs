from fastapi import APIRouter

from hyd.token.api.v1 import v1_router as v1_router_token
from hyd.user.api.v1 import v1_router as v1_router_user

v1_router = APIRouter()
v1_router.include_router(v1_router_token, prefix="/token")
v1_router.include_router(v1_router_user, prefix="/user")

api_router = APIRouter()
api_router.include_router(v1_router, prefix="/v1")
