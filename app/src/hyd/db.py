import sqlalchemy
import sqlalchemy.orm
from fastapi import Request
from sqlalchemy.orm import declarative_base, sessionmaker

EXTEND_EXISTING = True
URL_SQLITE = "sqlite:///data/hyd.db"

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
