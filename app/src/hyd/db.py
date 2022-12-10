import sqlalchemy
import sqlalchemy.orm
from fastapi import Request
from sqlalchemy.orm import declarative_base, sessionmaker

from hyd.util.const import PATH_DATA

EXTEND_EXISTING = True
URL_SQLITE = f"sqlite:///{PATH_DATA}/hyd.db"
# URL_MARIADB = f"mariadb+mariadbconnector://hyd_user:hyd_pw@127.0.0.1:3306/hyd_db"

engine: sqlalchemy.engine.base.Engine = sqlalchemy.create_engine(
    URL_SQLITE,
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
