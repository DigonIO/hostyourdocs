from hyd.project.models import ProjectEntry, VersionEntry
from hyd.util.models import NameStr, PrimaryKey
from sqlalchemy.orm import Session


def create_project(name: NameStr, db: Session) -> ProjectEntry:
    project_entry = ProjectEntry(name=name)
    db.add(project_entry)
    db.commit()
    return project_entry


def read_project(project_id: PrimaryKey, db: Session) -> list[ProjectEntry]:
    return db.query(ProjectEntry).get(project_id)


def read_project_by_name(project_name: NameStr, db: Session) -> list[ProjectEntry]:
    return db.query(ProjectEntry).filter(ProjectEntry.name == project_name).all()


def read_projects(db: Session) -> list[ProjectEntry]:
    return db.query(ProjectEntry).all()


def delete_project(project_id: PrimaryKey, db: Session) -> ProjectEntry:
    project_entry = read_project(project_id=project_id, db=db)
    db.delete(project_entry)
    db.commit()
    return project_entry


def create_version(
    project_id: PrimaryKey,
    ver_str: NameStr,
    filename: NameStr,
    content_type: NameStr,
    db=Session,
) -> VersionEntry:
    version_entry = VersionEntry(
        project_id=project_id,
        ver_str=ver_str,
        filename=filename,
        content_type=content_type,
    )
    db.add(version_entry)
    db.commit()
    return version_entry


def read_versions(db: Session) -> list[VersionEntry]:
    return db.query(VersionEntry).all()


def read_version(project_id: PrimaryKey, ver_str: NameStr, db=Session) -> VersionEntry:
    return db.query(VersionEntry).get((project_id, ver_str))


def delete_version(project_id: PrimaryKey, ver_str: NameStr, db=Session) -> VersionEntry:
    version_entry = read_version(project_id=project_id, ver_str=ver_str, db=db)
    db.delete(version_entry)
    db.commit()
    return version_entry
