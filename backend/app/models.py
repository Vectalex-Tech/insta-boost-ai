from sqlalchemy import String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db import Base

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    title: Mapped[str] = mapped_column(String(200), default="New project")
    prompt: Mapped[str] = mapped_column(Text, default="")
    niche: Mapped[str] = mapped_column(String(120), default="")
    goal: Mapped[str] = mapped_column(String(120), default="reach")

    status: Mapped[str] = mapped_column(String(40), default="draft")  # draft | generated | rendered | published
    generation_json: Mapped[str] = mapped_column(Text, default="{}")
    render_json: Mapped[str] = mapped_column(Text, default="{}")
    publish_json: Mapped[str] = mapped_column(Text, default="{}")

    assets: Mapped[list["Asset"]] = relationship(back_populates="project", cascade="all, delete-orphan")

class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    kind: Mapped[str] = mapped_column(String(20))  # image | video | audio | link | text
    filename: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(120), default="application/octet-stream")
    url: Mapped[str] = mapped_column(Text, default="")  # public URL (prod) or local served URL (dev)

    project: Mapped["Project"] = relationship(back_populates="assets")
