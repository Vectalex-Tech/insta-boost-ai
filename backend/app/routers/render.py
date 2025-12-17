import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Project
from app.schemas import RenderRequest
from app.worker.tasks import render_project

router = APIRouter(prefix="/render", tags=["render"])

@router.post("")
def render(req: RenderRequest, db: Session = Depends(get_db)):
    p = db.get(Project, req.project_id)
    if not p:
        from fastapi import HTTPException
        raise HTTPException(404, "Project not found")
    job = render_project.delay(req.project_id, req.variant, req.burn_captions)
    return {"ok": True, "task_id": job.id}
