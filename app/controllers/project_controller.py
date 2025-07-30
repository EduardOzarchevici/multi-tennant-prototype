from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.project_schema import ProjectCreate, ProjectUpdate


def resolve_create_project(session: Session, data: ProjectCreate, Project):
    new_project = Project(**data.dict())
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
    return new_project

def resolve_get_projects(session: Session, Project):
    return session.query(Project).all()


def resolve_delete_project(session: Session, project_id: int, Project):
    project = session.query(Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    session.delete(project)
    session.commit()
    return {"message": "Project deleted"}
