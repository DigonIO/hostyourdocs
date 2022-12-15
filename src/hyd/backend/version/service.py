from sqlalchemy.orm import Session

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
    db.commit()
    return version_entry


def read_version(project_id: PrimaryKey, version: NameStr, db=Session) -> VersionEntry:
    return db.query(VersionEntry).get((project_id, version))  # TODO exception


def read_versions(project_id: PrimaryKey, db: Session) -> list[VersionEntry]:
    return db.query(VersionEntry).filter(VersionEntry.project_id == project_id).all()


def delete_version_by_ref(*, version_entry: VersionEntry, db=Session) -> None:
    db.delete(version_entry)
    db.commit()
