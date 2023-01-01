import datetime as dt

from fastapi import status
from pydantic.types import conint, constr
from sqlalchemy import Column, DateTime, event
from sqlalchemy.orm import Mapped

from hyd.backend.util.const import MAX_LENGTH_STR_ID

####################################################################################################
#### pydantic types
####################################################################################################


PrimaryKey = conint(gt=0, lt=2147483647)
NameStr = constr(
    regex=r"^(?!\s*$).+",
    strip_whitespace=True,
    min_length=3,
    max_length=MAX_LENGTH_STR_ID,
)

####################################################################################################
#### SQLAlchemy table mixins
####################################################################################################


class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at: Mapped[dt.datetime] = Column(DateTime, default=dt.datetime.utcnow)
    updated_at: Mapped[dt.datetime | None] = Column(DateTime, default=None)
    # NOTE maybe this a better solution https://stackoverflow.com/questions/3923910/sqlalchemy-move-mixin-columns-to-end
    created_at._creation_order = 9998
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = dt.datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)


####################################################################################################
#### OpenAPI definitions
####################################################################################################


DETAIL_STR = {"content": {"application/json": {"example": {"detail": "string"}}}}

BASE_API_RESPONSE_SCHEMA = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "content": {"application/json": {"example": "Internal Server Error"}},
    },
    status.HTTP_401_UNAUTHORIZED: DETAIL_STR,
}
