import json
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import settings

def _client():
    from openai import OpenAI
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")
    return OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM = """You are an assistant that packages Instagram content to maximize organic early traction ethically.
Do NOT suggest spam, fake engagement, or any manipulation/loopholes.
Focus on: clarity of topic, retention, shares/saves, strong hook, concise on-screen text, and meaningful CTA.
Return strict JSON only (no markdown).
"""

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
def generate_packaging(payload: Dict[str, Any]) -> Dict[str, Any]:
    # payload can include prompt, niche, goal, assets metadata, etc.
    client = _client()

    user = {
        "prompt": payload.get("prompt",""),
        "niche": payload.get("niche",""),
        "goal": payload.get("goal","reach"),
        "language": payload.get("language","pt"),
        "tone": payload.get("tone","direto"),
        "max_duration_sec": payload.get("max_duration_sec", 18),
        "assets": payload.get("assets", []),
    }

    schema = {
        "type":"object",
        "properties":{
            "topic_signal":{"type":"string"},
            "target_viewer":{"type":"string"},
            "hooks":{"type":"array","items":{"type":"string"}, "minItems":3, "maxItems":7},
            "on_screen_text":{"type":"array","items":{"type":"string"}, "minItems":3, "maxItems":12},
            "caption_variants":{"type":"array","items":{"type":"string"}, "minItems":2, "maxItems":4},
            "cta":{"type":"string"},
            "hashtags":{"type":"array","items":{"type":"string"}, "minItems":3, "maxItems":10},
            "shotlist":{"type":"array","items":{"type":"string"}, "minItems":3, "maxItems":12},
            "edit_plan":{"type":"object","properties":{
                "max_duration_sec":{"type":"integer"},
                "notes":{"type":"array","items":{"type":"string"}}
            }, "required":["max_duration_sec","notes"]},
            "compliance_notes":{"type":"array","items":{"type":"string"}}
        },
        "required":["topic_signal","target_viewer","hooks","on_screen_text","caption_variants","cta","hashtags","shotlist","edit_plan","compliance_notes"]
    }

    # Use JSON mode (OpenAI Responses API supports structured outputs; here we keep it simple)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.8,
        messages=[
            {"role":"system","content":SYSTEM},
            {"role":"user","content":f"Create packaging JSON for: {json.dumps(user, ensure_ascii=False)}"}
        ],
        response_format={"type":"json_schema","json_schema":{"name":"packaging","schema":schema}}
    )
    content = resp.choices[0].message.content
    return json.loads(content)
