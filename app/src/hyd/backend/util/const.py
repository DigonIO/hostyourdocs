"""Hardcoded configuration values"""

import os
from pathlib import Path

import hyd

PKG_PATH = os.path.dirname(hyd.__file__)
STATIC_PATH = PKG_PATH + "/backend/static"
TEMPLATE_PATH = PKG_PATH + "/backend/templates"

PATH_DATA = Path("data")
PATH_PROJECTS = PATH_DATA / "projects"

MAX_LENGTH_STR_ID = 64
MAX_LENGTH_TOKEN_SCOPE = 16

HTML_TITLE = "HostYourDocs"
