from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hyd.backend.security import hash_password
from hyd.backend.user.models import UserEntry
from hyd.backend.util.error import UnknownEntryError, UsernameError
from hyd.backend.util.models import PrimaryKey


def create_user(*, username: str, password: str, is_admin: bool, db: Session) -> UserEntry:
    hashed_password: bytes = hash_password(password=password)
    try:
        user_entry = UserEntry(
            username=username, hashed_password=hashed_password, is_admin=is_admin
        )
        db.add(user_entry)
        db.commit()
    except IntegrityError:
        raise UsernameError(f"Username '{username}' is already taken!")

    return user_entry


def read_user(*, user_id: PrimaryKey, db: Session) -> UserEntry:
    try:
        return db.query(UserEntry).get(user_id)
    except IntegrityError:
        raise UnknownEntryError(f"Unknown user_id '{user_id}'!")


def read_users_by_username(*, username: str, db: Session) -> UserEntry:
    try:
        return db.query(UserEntry).filter(UserEntry.username == username).all()[0]
    except IndexError:
        raise UnknownEntryError(f"Unknown username '{username}'!")


def read_users(*, db: Session) -> list[UserEntry]:
    return db.query(UserEntry).all()


def enable_user_by_ref(*, user_entry: PrimaryKey, db: Session) -> None:
    user_entry.is_disabled = False
    db.commit()


def disable_user_by_ref(*, user_entry: PrimaryKey, db: Session) -> None:
    user_entry.is_disabled = True
    db.commit()


# def update_user_pw(*, user_id: PrimaryKey, new_password: str, db: Session) -> UserEntry:
#    user_entry = read_user(user_id=user_id, db=db)
#    update_user_pw_by_ref(user_entry=user_entry, new_password=new_password, db=db)
#    return user_entry


def update_user_pw_by_ref(*, user_entry: UserEntry, new_password: str, db: Session) -> None:
    user_entry.hashed_password = hash_password(password=new_password)
    db.commit()
