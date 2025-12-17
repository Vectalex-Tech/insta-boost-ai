import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectOut

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("", response_model=ProjectOut)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    p = Project(title=payload.title, prompt=payload.prompt, niche=payload.niche, goal=payload.goal)
    db.add(p); db.commit(); db.refresh(p)
    return ProjectOut(
        id=p.id, created_at=p.created_at, title=p.title, prompt=p.prompt, niche=p.niche, goal=p.goal,
        status=p.status, generation_json=json.loads(p.generation_json), render_json=json.loads(p.render_json), publish_json=json.loads(p.publish_json)
    )

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    p = db.get(Project, project_id)
    if not p:
        from fastapi import HTTPException
        raise HTTPException(404, "Not found")
    return ProjectOut(
        id=p.id, created_at=p.created_at, title=p.title, prompt=p.prompt, niche=p.niche, goal=p.goal,
        status=p.status, generation_json=json.loads(p.generation_json), render_json=json.loads(p.render_json), publish_json=json.loads(p.publish_json)
    )
