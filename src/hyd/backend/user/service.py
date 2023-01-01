from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hyd.backend.exc import NameStrError, UnknownUserError
from hyd.backend.security import hash_password
from hyd.backend.user.models import UserEntry
from hyd.backend.util.models import PrimaryKey


def create_user(*, username: str, password: str, is_admin: bool, db: Session) -> UserEntry:
    hashed_password: bytes = hash_password(password=password)

    user_entry = UserEntry(username=username, hashed_password=hashed_password, is_admin=is_admin)
    db.add(user_entry)

    try:
        db.commit()
    except IntegrityError:
        raise NameStrError

    return user_entry


def read_user(*, user_id: PrimaryKey, db: Session) -> UserEntry:
    user_entry = db.query(UserEntry).get(user_id)

    if user_entry is None:
        raise UnknownUserError

    return user_entry


def read_users_by_username(*, username: str, db: Session) -> UserEntry:
    try:
        return db.query(UserEntry).filter(UserEntry.username == username).all()[0]
    except IndexError:
        raise UnknownUserError


def read_users(*, db: Session) -> list[UserEntry]:
    return db.query(UserEntry).all()


def enable_user_by_ref(*, user_entry: UserEntry, db: Session) -> None:
    user_entry.is_disabled = False
    db.commit()


def disable_user_by_ref(*, user_entry: UserEntry, db: Session) -> None:
    user_entry.is_disabled = True
    db.commit()


def update_user_pw_by_ref(*, user_entry: UserEntry, new_password: str, db: Session) -> None:
    user_entry.hashed_password = hash_password(password=new_password)
    db.commit()
