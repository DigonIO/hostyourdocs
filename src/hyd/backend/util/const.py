"""Hardcoded configuration values"""

import datetime as dt
import os
from pathlib import Path

import hyd

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

# HTTPS: bool
# _https = os.getenv("HTTPS")
# if _https == "True":
#    HTTPS = True
# elif _https == "False" or _https is None:
#    HTTPS = False
# else:
#    raise ValueError("Environment variable 'HTTPS' has to be literal 'True' or 'False'!")

NAME_HOSTED_BY: str | None = os.getenv("NAME_HOSTED_BY")
LINK_HOSTED_BY: str | None = os.getenv("LINK_HOSTED_BY")
LINK_IMPRESS: str | None = os.getenv("LINK_IMPRESS")
LINK_PRIVACY: str | None = os.getenv("LINK_PRIVACY")
