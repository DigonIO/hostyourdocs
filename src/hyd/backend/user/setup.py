from sqlalchemy.orm import Session

from hyd.backend.user.models import UserEntry
from hyd.backend.user.service import create_user, read_users_by_username
from hyd.backend.util.error import UnknownUserError


def setup_admin_user(db: Session) -> None:
    try:
        _: UserEntry = read_users_by_username(username="admin", db=db)
    except UnknownUserError:
        _: UserEntry = create_user(username="admin", password="1234", is_admin=True, db=db)
