import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.db import engine, Base
from app.routers import projects, assets, generate, render, instagram

app = FastAPI(title="InstaBoost AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables (MVP). In production, use Alembic migrations.
Base.metadata.create_all(bind=engine)

# Static serving for dev (uploads + renders). In production, use S3/CDN.
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.RENDER_DIR, exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.mount("/static/renders", StaticFiles(directory=settings.RENDER_DIR), name="renders")

app.include_router(projects.router)
app.include_router(assets.router)
app.include_router(generate.router)
app.include_router(render.router)
app.include_router(instagram.router)

@app.get("/health")
def health():
    return {"ok": True, "env": settings.APP_ENV}
