from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hyd.backend.project.models import ProjectEntry
from hyd.backend.util.error import NameStrError, UnknownProjectError
from hyd.backend.util.models import NameStr, PrimaryKey


def create_project(*, name: NameStr, db: Session) -> ProjectEntry:
    project_entry = ProjectEntry(name=name)
    db.add(project_entry)

    try:
        db.commit()
    except IntegrityError:
        raise NameStrError

    return project_entry


def read_project(*, project_id: PrimaryKey, db: Session) -> ProjectEntry:
    project_entry = db.query(ProjectEntry).get(project_id)

    if project_entry is None:
        raise UnknownProjectError

    return project_entry


def read_project_by_name(*, project_name: NameStr, db: Session) -> list[ProjectEntry]:
    try:
        return db.query(ProjectEntry).filter(ProjectEntry.name == project_name).all()[0]
    except IndexError:
        raise UnknownProjectError


def read_projects(*, db: Session) -> list[ProjectEntry]:
    return db.query(ProjectEntry).all()


def delete_project_by_ref(*, project_entry: ProjectEntry, db: Session) -> None:
    db.delete(project_entry)
    db.commit()
