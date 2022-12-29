import sqlalchemy
import sqlalchemy.orm
from fastapi import Request
from sqlalchemy.orm import declarative_base, sessionmaker

from hyd.backend.util.const import MARIADB_ADDRESS, MARIADB_PASSWORD
from hyd.backend.util.error import HydError

EXTEND_EXISTING = True

if MARIADB_PASSWORD is None:
    raise HydError("MARIADB_PASSWORD is missing!")
if MARIADB_ADDRESS is None:
    raise HydError("MARIADB_ADDRESS is missing!")

URL_MARIADB = (
    f"mariadb+mariadbconnector://hyd_user:{MARIADB_PASSWORD}@{MARIADB_ADDRESS}:3306/hyd_db"
)


engine: sqlalchemy.engine.base.Engine = sqlalchemy.create_engine(
    URL_MARIADB,
    # echo=True prints all SQL statements being executed to the console as they happen
    # echo=True,
    # use sqlalchemy.future.Engine for full 2.0 compatibility
    future=True,
)

DeclarativeMeta: type = declarative_base()

# for typing see https://github.com/sqlalchemy/sqlalchemy/issues/7656
SessionMaker = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Dependency
def get_db(request: Request):
    return request.state.db
