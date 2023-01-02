from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import hyd.backend.util.patch_fastapi  # dirty openapi.json hack
from hyd.backend.api import api_router
from hyd.backend.db import DeclarativeMeta, SessionMaker, engine
from hyd.backend.frontend import footer_router, frontend_router
from hyd.backend.mount_helper import MountHelper
from hyd.backend.user.setup import setup_admin_user
from hyd.backend.util.const import PATH_PROJECTS, ROOT_PATH
from hyd.backend.util.injection import reinject_js_loader_to_html
from hyd.backend.util.logger import HydLogger

LOGGER = HydLogger("App")

# edits ALL existing html files in storage (not ideal)
for dir_path in PATH_PROJECTS.iterdir():
    reinject_js_loader_to_html(dir_path=dir_path)

# Only useful for local development
# DeclarativeMeta.metadata.drop_all(bind=engine)
DeclarativeMeta.metadata.create_all(bind=engine)

app = FastAPI(root_path=ROOT_PATH)
# https://fastapi.tiangolo.com/tutorial/cors/

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
app.include_router(footer_router, prefix="/footer")
MountHelper.set_router(router=app.router)

####################################################################################################
### Setup Backend
####################################################################################################

db = SessionMaker()

setup_admin_user(db=db)
MountHelper.mount_existing_projects(db=db)

db.close()
