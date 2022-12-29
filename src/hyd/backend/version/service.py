from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import hyd.backend.project.service as project_service
from hyd.backend.util.error import NameError, UnknownVersionError
from hyd.backend.util.models import NameStr, PrimaryKey
from hyd.backend.version.models import VersionEntry


def create_version(
    project_id: PrimaryKey,
    version: NameStr,
    filename: NameStr,
    content_type: NameStr,
    db=Session,
) -> VersionEntry:
    version_entry = VersionEntry(
        project_id=project_id,
        version=version,
        filename=filename,
        content_type=content_type,
    )
    db.add(version_entry)

    try:
        db.commit()
    except IntegrityError:
        raise NameError

    return version_entry


def read_version(project_id: PrimaryKey, version: NameStr, db=Session) -> VersionEntry:
    project_entry = project_service.read_project(project_id=project_id, db=db)

    version_entries: list[VersionEntry] = project_entry.version_entries
    for tag_entry in version_entries:
        if tag_entry.version == version:
            return tag_entry

    raise UnknownVersionError


def read_versions(project_id: PrimaryKey, db: Session) -> list[VersionEntry]:
    return db.query(VersionEntry).filter(VersionEntry.project_id == project_id).all()


def delete_version_by_ref(*, version_entry: VersionEntry, db=Session) -> None:
    db.delete(version_entry)
    db.commit()
