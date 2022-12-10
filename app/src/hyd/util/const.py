"""Hardcoded configuration values"""

import os

import hyd

PATH = os.path.dirname(hyd.__file__)
STATIC_PATH = PATH + "/static"
TEMPLATE_PATH = PATH + "/templates"

USERNAME_MAX_LENGTH = 64
TOKEN_SCOPE_MAX_LENGTH = 16

HTML_TITLE = "HostYourDocs"
