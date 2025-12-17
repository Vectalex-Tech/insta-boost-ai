import json, os
from pathlib import Path
from sqlalchemy.orm import Session
from app.worker.celery_app import celery
from app.config import settings
from app.db import SessionLocal
from app.models import Project
from app.services.video import render_basic_reel, make_cover_from_frame

@celery.task(name="app.worker.tasks.render_project")
def render_project(project_id: int, variant: str = "A", burn_captions: bool = False) -> dict:
    db: Session = SessionLocal()
    try:
        proj = db.get(Project, project_id)
        if not proj:
            raise RuntimeError("Project not found")

        assets = proj.assets
        video_assets = [a for a in assets if a.kind == "video"]
        if not video_assets:
            raise RuntimeError("No video asset uploaded. MVP renderer expects a video.")

        input_path = os.path.join(settings.UPLOAD_DIR, video_assets[0].filename)
        out_name = f"project_{project_id}_{variant}.mp4"
        output_path = os.path.join(settings.RENDER_DIR, out_name)

        render_info = render_basic_reel(input_path, output_path, burn_captions=burn_captions, captions_srt=None)
        cover_png = os.path.join(settings.RENDER_DIR, f"project_{project_id}_{variant}_cover.png")
        cover_info = make_cover_from_frame(output_path, cover_png)

        proj.render_json = json.dumps({"variant": variant, "render": render_info, "cover": cover_info}, ensure_ascii=False)
        proj.status = "rendered"
        db.add(proj); db.commit(); db.refresh(proj)
        return {"ok": True, "output_path": output_path, "cover_path": cover_png}
    finally:
        db.close()
