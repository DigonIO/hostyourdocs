from sqlalchemy.orm import Session

from hyd.backend.tag.models import TagEntry
from hyd.backend.util.models import NameStr, PrimaryKey


def create_tag_entry(project_id: PrimaryKey, tag: NameStr, primary: bool, db: Session) -> TagEntry:
    tag_entry = TagEntry(project_id=project_id, tag=tag, primary=primary)
    db.add(tag_entry)
    db.commit()
    return tag_entry


def read_tag_entry(project_id: PrimaryKey, tag: NameStr, db: Session) -> TagEntry:
    return db.query(TagEntry).get((project_id, tag))


def delete_tag_entry_by_ref(tag_entry: TagEntry, db: Session) -> None:
    db.delete(tag_entry)
    db.commit()
