from datetime import datetime

from fastapi import status
from hyd.backend.util.const import MAX_LENGTH_STR_ID
from pydantic.types import conint, constr
from sqlalchemy import Column, DateTime, event

PrimaryKey = conint(gt=0, lt=2147483647)
NameStr = constr(
    regex=r"^(?!\s*$).+",
    strip_whitespace=True,
    min_length=3,
    max_length=MAX_LENGTH_STR_ID,
)


class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=None)
    # NOTE maybe this a better solution https://stackoverflow.com/questions/3923910/sqlalchemy-move-mixin-columns-to-end
    created_at._creation_order = 9998
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)


DEFAULT_STR = {"content": {"application/json": {"example": "string"}}}
DEFAULT_MSG = {"content": {"application/json": {"example": {"msg": "string"}}}}
# see https://fastapi.tiangolo.com/advanced/additional-responses/
DEFAULT_PDF = {"content": {"application/pdf": {}}}
DEFAULT_MSG_ID = {"content": {"application/json": {"example": {"msg": "string", "id": 1}}}}
DEFAULT_MSG_IDS = {"content": {"application/json": {"example": {"msg": "string", "ids": [1]}}}}

BASE_API_RESPONSE_SCHEMA = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "content": {"application/json": {"example": "Internal Server Error"}},
    },
}
