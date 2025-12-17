import httpx
from typing import Dict, Any, Optional
from app.config import settings

class MetaAPIError(RuntimeError):
    pass

def _base():
    return f"https://graph.facebook.com/{settings.META_API_VERSION}"

async def create_reels_container(ig_user_id: str, video_url: str, caption: str, access_token: str) -> str:
    # Endpoint pattern from Instagram Graph API content publishing
    url = f"{_base()}/{ig_user_id}/media"
    params = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": access_token,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, params=params)
        data = r.json()
        if r.status_code >= 400:
            raise MetaAPIError(f"Meta error {r.status_code}: {data}")
        return data["id"]

async def publish_container(ig_user_id: str, creation_id: str, access_token: str) -> Dict[str, Any]:
    url = f"{_base()}/{ig_user_id}/media_publish"
    params = {"creation_id": creation_id, "access_token": access_token}
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, params=params)
        data = r.json()
        if r.status_code >= 400:
            raise MetaAPIError(f"Meta error {r.status_code}: {data}")
        return data
