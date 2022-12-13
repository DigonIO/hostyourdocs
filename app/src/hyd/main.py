import os

from fastapi import FastAPI, Request, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import hyd.util.patch_fastapi  # dirty openapi.json hack

from hyd.api import api_router
from hyd.frontend import frontend_router
from hyd.db import DeclarativeMeta, SessionMaker, engine
from hyd.util.logger import HydLogger
from hyd.util.const import STATIC_PATH
from hyd.mount_helper import MountHelper

LOGGER = HydLogger("App")

# DeclarativeMeta.metadata.drop_all(bind=engine)
DeclarativeMeta.metadata.create_all(bind=engine)


app = FastAPI()
# https://fastapi.tiangolo.com/tutorial/cors/

MountHelper.set_app(app=app)

####################################################################################################
### FastAPI config
####################################################################################################


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

####################################################################################################
### Middleware callbacks
####################################################################################################


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        request.state.db = SessionMaker()
        return await call_next(request)
    finally:
        request.state.db.close()


####################################################################################################
### Route setup
####################################################################################################

app.include_router(api_router, prefix="/api")
app.include_router(frontend_router, prefix="/simple")
