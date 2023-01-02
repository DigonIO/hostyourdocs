import datetime as dt
import os
from pathlib import Path

import hyd

####################################################################################################
#### Environment variables
####################################################################################################

SECRET_KEY: str | None = os.getenv("SECRET_KEY")

MARIADB_PASSWORD: str | None = os.getenv("MARIADB_PASSWORD")
MARIADB_ADDRESS: str | None = os.getenv("MARIADB_ADDRESS")

_root_path: str | None = os.getenv("ROOT_PATH")  # optional
ROOT_PATH: str = _root_path if _root_path else ""

NAME_HOSTED_BY: str | None = os.getenv("NAME_HOSTED_BY")  # optional
LINK_HOSTED_BY: str | None = os.getenv("LINK_HOSTED_BY")  # optional
LINK_IMPRESS: str | None = os.getenv("LINK_IMPRESS")  # optional
LINK_PRIVACY: str | None = os.getenv("LINK_PRIVACY")  # optional

###################################################################################################
#### Const values
####################################################################################################

LOADER_HTML_INJECTION = f'<script src="{ROOT_PATH}/footer/loader.js"><!-- Injected by HostYourDocs --></script>'

REMEMBER_ME_DURATION = dt.timedelta(days=30)
LOGIN_DURATION_AFTER_LAST_REQUEST = dt.timedelta(minutes=10)

PKG_PATH = os.path.dirname(hyd.__file__)
STATIC_PATH = PKG_PATH + "/backend/static"
TEMPLATE_PATH = PKG_PATH + "/backend/templates"

PATH_DATA = Path("data")
PATH_PROJECTS = PATH_DATA / "projects"

MAX_LENGTH_STR_ID = 64
MAX_LENGTH_TOKEN_SCOPE = 16

HEADERS = {"WWW-Authenticate": "Bearer"}

HTML_TITLE = "HostYourDocs"
