import json, os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Project
from app.schemas import PublishRequest
from app.config import settings
from app.services.instagram_api import create_reels_container, publish_container

router = APIRouter(prefix="/instagram", tags=["instagram"])

@router.post("/publish")
async def publish(req: PublishRequest, db: Session = Depends(get_db)):
    p = db.get(Project, req.project_id)
    if not p:
        from fastapi import HTTPException
        raise HTTPException(404, "Project not found")

    pack = json.loads(p.generation_json or "{}")
    caption = req.caption or (pack.get("caption_variants") or [""])[0]

    # Choose media URL
    media_url = req.media_url
    if not media_url:
        render = json.loads(p.render_json or "{}")
        out_path = (render.get("render") or {}).get("output_path")
        if not out_path:
            from fastapi import HTTPException
            raise HTTPException(400, "No rendered output. Render first or provide media_url.")
        # In dev we serve local static; in production this MUST be a publicly accessible URL.
        fname = os.path.basename(out_path)
        media_url = f"{settings.PUBLIC_BASE_URL}/static/renders/{fname}"

    # Tokens (for MVP we accept env token; in production store per-user OAuth tokens)
    access_token = settings.META_USER_ACCESS_TOKEN
    ig_user_id = settings.META_IG_USER_ID
    if not access_token or not ig_user_id:
        from fastapi import HTTPException
        raise HTTPException(400, "Missing META_USER_ACCESS_TOKEN or META_IG_USER_ID")

    creation_id = await create_reels_container(ig_user_id, media_url, caption, access_token)
    publish_resp = await publish_container(ig_user_id, creation_id, access_token)

    p.publish_json = json.dumps({"creation_id": creation_id, "publish": publish_resp, "media_url": media_url}, ensure_ascii=False)
    p.status = "published"
    db.add(p); db.commit(); db.refresh(p)

    return {"ok": True, "creation_id": creation_id, "publish": publish_resp, "media_url": media_url}
