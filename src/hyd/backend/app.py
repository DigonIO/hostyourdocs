from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import hyd.backend.util.patch_fastapi  # dirty openapi.json hack
from hyd.backend.api import api_router
from hyd.backend.db import SessionMaker
from hyd.backend.frontend import footer_router, frontend_router
from hyd.backend.util.const import ROOT_PATH

app = FastAPI(root_path=ROOT_PATH)
# https://fastapi.tiangolo.com/tutorial/cors/

####################################################################################################
### Middleware
####################################################################################################

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
