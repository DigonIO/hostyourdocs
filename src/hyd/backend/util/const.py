"""Hardcoded configuration values"""

import datetime as dt
import os
from pathlib import Path

import hyd

SRV_TIMEZONE = dt.timezone.utc

REMEMBER_ME_DURATION = dt.timedelta(days=30)
LOGIN_DURATION_AFTER_LAST_REQUEST = dt.timedelta(minutes=10)

PKG_PATH = os.path.dirname(hyd.__file__)
STATIC_PATH = PKG_PATH + "/backend/static"
TEMPLATE_PATH = PKG_PATH + "/backend/templates"

PATH_DATA = Path("data")
PATH_PROJECTS = PATH_DATA / "projects"

MAX_LENGTH_STR_ID = 64
MAX_LENGTH_TOKEN_SCOPE = 16

HTML_TITLE = "HostYourDocs"
