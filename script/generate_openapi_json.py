import json
import os
import secrets
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def generate_openapi_json(*, app: FastAPI, path: Path = Path(os.getcwd())) -> None:
    with open("openapi.json", "w") as handle:
        openapi_dict: dict[str, Any] = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        json.dump(openapi_dict, handle)


def reset_env_var(key: str, val: str | None) -> None:
    if val is None:
        del os.environ[key]
    else:
        os.environ[key] = val


if __name__ == "__main__":

    secret_key_old: str | None = os.getenv("ECRET_KEY")
    mariadb_pass_old: str | None = os.getenv("MARIADB_PASSWORD")
    mariadb_addr_old: str | None = os.getenv("MARIADB_ADDRESS")

    os.environ["SECRET_KEY"] = secrets.token_hex(32)
    os.environ["MARIADB_PASSWORD"] = secrets.token_hex(32)
    os.environ["MARIADB_ADDRESS"] = "127.0.0.1"

    from hyd.backend.app import app

    generate_openapi_json(app=app)

    reset_env_var("SECRET_KEY", secret_key_old)
    reset_env_var("MARIADB_PASSWORD", mariadb_pass_old)
    reset_env_var("MARIADB_ADDRESS", mariadb_addr_old)
