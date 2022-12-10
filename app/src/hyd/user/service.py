from sqlalchemy.orm import Session

from hyd.util.models import PrimaryKey
from hyd.security import hash_password
from hyd.user.models import UserEntry


async def create_user(
    *, username: str, password: str, is_admin: bool, db: Session
) -> UserEntry:
    hashed_password: bytes = hash_password(password=password)
    user_entry = UserEntry(
        username=username, hashed_password=hashed_password, is_admin=is_admin
    )
    db.add(user_entry)
    db.commit()
    return user_entry


async def read_user(*, user_id: PrimaryKey, db: Session) -> UserEntry:
    return db.query(UserEntry).get(user_id)


async def read_users_by_username(*, username: str, db: Session) -> list[UserEntry]:
    return db.query(UserEntry).filter(UserEntry.username == username).all()


async def read_users(*, db: Session) -> list[UserEntry]:
    return db.query(UserEntry).all()


async def enable_user_by_ref(*, user_entry: PrimaryKey, db: Session) -> None:
    user_entry.is_disabled = False
    db.commit()


async def disable_user_by_ref(*, user_entry: PrimaryKey, db: Session) -> None:
    user_entry.is_disabled = True
    db.commit()


async def update_user_pw(
    *, user_id: PrimaryKey, new_password: str, db: Session
) -> UserEntry:
    user_entry = await read_user(user_id=user_id, db=db)
    await update_user_pw_by_ref(user_entry=user_entry, new_password=new_password, db=db)
    return user_entry


async def update_user_pw_by_ref(
    *, user_entry: UserEntry, new_password: str, db: Session
) -> None:
    user_entry.hashed_password = hash_password(password=new_password)
    db.commit()
