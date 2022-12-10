from fastapi import APIRouter

v1_router = APIRouter()

api_router = APIRouter()
api_router.include_router(v1_router, prefix="/v1")
