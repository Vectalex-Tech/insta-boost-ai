import os
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db import get_db
from app.config import settings
from app.models import Asset, Project
from app.schemas import AssetOut

router = APIRouter(prefix="/assets", tags=["assets"])

@router.post("", response_model=AssetOut)
async def upload_asset(
    project_id: int = Form(...),
    kind: str = Form(...),  # image|video|audio|link|text
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    proj = db.get(Project, project_id)
    if not proj:
        from fastapi import HTTPException
        raise HTTPException(404, "Project not found")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    safe_name = f"p{project_id}_{file.filename}".replace("..",".")
    dest = os.path.join(settings.UPLOAD_DIR, safe_name)

    content = await file.read()
    with open(dest, "wb") as f:
        f.write(content)

    url = f"{settings.PUBLIC_BASE_URL}/static/uploads/{safe_name}"
    asset = Asset(project_id=project_id, kind=kind, filename=safe_name, content_type=file.content_type or "", url=url)
    db.add(asset); db.commit(); db.refresh(asset)
    return asset
