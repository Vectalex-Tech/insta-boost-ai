import os, subprocess, json
from pathlib import Path
from typing import Optional, Dict, Any
from app.config import settings

def run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{proc.stdout}")

def ensure_dirs():
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.RENDER_DIR).mkdir(parents=True, exist_ok=True)

def render_basic_reel(input_path: str, output_path: str, burn_captions: bool = False, captions_srt: Optional[str] = None) -> Dict[str, Any]:
    """Minimal renderer.
    - Keeps original audio.
    - Optionally burns captions if SRT provided.
    """
    ensure_dirs()
    filters = []
    if burn_captions and captions_srt:
        # FFmpeg subtitles filter requires libass; many builds support it. If not, disable burn_captions.
        filters.append(f"subtitles={captions_srt}")
    vf = ",".join(filters) if filters else None

    cmd = ["ffmpeg", "-y", "-i", input_path, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k"]
    if vf:
        cmd += ["-vf", vf]
    cmd += [output_path]
    run(cmd)
    return {"output_path": output_path, "burn_captions": burn_captions}

def make_cover_from_frame(input_path: str, output_png: str, t: float = 0.2) -> Dict[str, Any]:
    ensure_dirs()
    cmd = ["ffmpeg", "-y", "-ss", str(t), "-i", input_path, "-vframes", "1", "-q:v", "2", output_png]
    run(cmd)
    return {"cover_path": output_png, "timestamp": t}
