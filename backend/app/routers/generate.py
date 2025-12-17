import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Project
from app.schemas import GenerationRequest
from app.services.llm import generate_packaging

router = APIRouter(prefix="/generate", tags=["generate"])

@router.post("")
def generate(project: GenerationRequest, db: Session = Depends(get_db)):
    p = db.get(Project, project.project_id)
    if not p:
        from fastapi import HTTPException
        raise HTTPException(404, "Project not found")

    payload = {
        "prompt": p.prompt,
        "niche": p.niche,
        "goal": p.goal,
        "language": project.language,
        "tone": project.tone,
        "max_duration_sec": project.max_duration_sec if hasattr(p, "max_duration_sec") else project.max_duration_sec,
        "assets": [{"kind": a.kind, "url": a.url, "filename": a.filename} for a in p.assets],
    }
    pack = generate_packaging(payload)
    p.generation_json = json.dumps(pack, ensure_ascii=False)
    p.status = "generated"
    db.add(p); db.commit(); db.refresh(p)
    return {"ok": True, "project_id": p.id, "packaging": pack}
