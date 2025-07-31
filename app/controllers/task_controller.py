from sqlalchemy.orm import Session
from fastapi import HTTPException

from schemas.task_schema import *
from models.user_model import User

def resolve_create_task(db: Session, task_data: TaskCreate, Task, user_data):
    user_email = user_data.get("email")

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")


    new_task = Task(
        createdby=user.id,
        tasktype=task_data.tasktype,
        assignedto=task_data.assignedto,
        tasktitle=task_data.tasktitle,
        duedate=task_data.duedate,
        completed=task_data.completed,
        completedate=task_data.completedate,
        projectKey=task_data.projectKey,
        creationdate=datetime.utcnow()
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def resolve_get_tasks(session: Session, Task):
    return session.query(Task).all()

def resolve_delete_task(session: Session, task_id: int, Task):
    task = session.query(Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted"}