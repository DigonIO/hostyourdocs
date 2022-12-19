from sqlalchemy.orm import Session

from hyd.backend.user.service import create_user, read_users_by_username
from hyd.backend.util.error import UnknownEntryError


def setup_admin_user(db: Session) -> None:
    try:
        _user_entry = read_users_by_username(username="admin", db=db)
    except UnknownEntryError:
        _user_entry = create_user(username="admin", password="1234", is_admin=True, db=db)
