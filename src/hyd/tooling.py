"""
A collection of tools used during development and by CIs.
"""

import json
import os
import secrets
from pathlib import Path
from typing import Any

from fastapi.openapi.utils import get_openapi


def set_envvars() -> tuple[str | None, str | None, str | None]:
    secret_key_old: str | None = os.getenv("ECRET_KEY")
    mariadb_pass_old: str | None = os.getenv("MARIADB_PASSWORD")
    mariadb_addr_old: str | None = os.getenv("MARIADB_ADDRESS")

    os.environ["SECRET_KEY"] = secrets.token_hex(32)
    os.environ["MARIADB_PASSWORD"] = secrets.token_hex(32)
    os.environ["MARIADB_ADDRESS"] = "127.0.0.1"

    return secret_key_old, mariadb_pass_old, mariadb_addr_old


def reset_envvars(old_vals: tuple) -> None:
    _reset_env_var("SECRET_KEY", old_vals[0])
    _reset_env_var("MARIADB_PASSWORD", old_vals[1])
    _reset_env_var("MARIADB_ADDRESS", old_vals[2])


def _reset_env_var(key: str, val: str | None) -> None:
    if val is None:
        del os.environ[key]
    else:
        os.environ[key] = val


def generate_openapi_json(*, path: Path = Path(os.getcwd())) -> None:

    old_vals = set_envvars()

    from hyd.backend.app import app

    with open(path / "openapi.json", "w") as handle:
        openapi_dict: dict[str, Any] = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        json.dump(openapi_dict, handle)

    reset_envvars(old_vals)
