from hyd.backend.app import app
from hyd.backend.db import DeclarativeMeta, SessionMaker, engine
from hyd.backend.mount_helper import MountHelper
from hyd.backend.user.setup import setup_admin_user
from hyd.backend.util.const import PATH_PROJECTS
from hyd.backend.util.injection import reinject_js_loader_to_html

####################################################################################################
### Setup Backend
####################################################################################################

# Edits ALL existing html files in storage (not ideal)
try:
    for dir_path in PATH_PROJECTS.iterdir():
        reinject_js_loader_to_html(dir_path=dir_path)
except FileNotFoundError:
    ...  # If FileNotFoundError was raised no projected was uploaded, so just ignore the Exception

# Only useful for local development
# DeclarativeMeta.metadata.drop_all(bind=engine)
DeclarativeMeta.metadata.create_all(bind=engine)

MountHelper.set_router(router=app.router)

with SessionMaker() as db:
    setup_admin_user(db=db)
    MountHelper.mount_existing_projects(db=db)
