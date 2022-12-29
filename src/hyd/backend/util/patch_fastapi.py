import re

from fastapi.routing import APIRoute
from fastapi.utils import generate_unique_id


def custom_generate_unique_id(route: APIRoute) -> str:
    operation_id = route.path_format
    operation_id = re.sub("[^0-9a-zA-Z_]", "_", operation_id)
    assert route.methods
    operation_id = operation_id + "_" + list(route.methods)[0].lower()
    return operation_id[1:]


generate_unique_id.__code__ = custom_generate_unique_id.__code__
