from sqlalchemy.orm import Session

import hyd.backend.project.service as project_service
from hyd.backend.tag.models import PrimaryTagEntry, TagEntry
from hyd.backend.util.models import NameStr, PrimaryKey


def create_tag_entry(project_id: PrimaryKey, tag: NameStr, primary: bool, db: Session) -> TagEntry:

    _ = project_service.read_project(project_id=project_id, db=db)

    if primary and db.query(PrimaryTagEntry).get(project_id):
        raise Exception("There can only be one primary tag for a project!")  # TODO

    tag_entry = TagEntry(project_id=project_id, tag=tag, primary=primary)
    db.add(tag_entry)

    if primary:
        primary_tag_entry = PrimaryTagEntry(project_id=project_id, primary_tag=tag)
        db.add(primary_tag_entry)

    db.commit()
    return tag_entry


def read_tag_entry(project_id: PrimaryKey, tag: NameStr, db: Session) -> TagEntry:
    return db.query(TagEntry).get((project_id, tag))


def delete_tag_entry_by_ref(tag_entry: TagEntry, db: Session) -> None:
    if tag_entry.primary:
        primary_tag_entry: PrimaryTagEntry = db.query(PrimaryTagEntry).get(tag_entry.project_id)
        db.delete(primary_tag_entry)

    db.delete(tag_entry)
    db.commit()
