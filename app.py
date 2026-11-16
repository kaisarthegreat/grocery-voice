from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from core.parser import parse_grocery_text

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"

app = FastAPI(title="Grocery Voice", version="0.3.1")


class VoiceTranscriptRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    language: str = Field(default="en-IN", pattern=r"^(en-IN|hi-IN)$")


class GroceryParseRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    language: str = Field(default="en-IN", pattern=r"^(en-IN|hi-IN)$")


@app.get("/api/health")
async def health():
    return {"status": "ok", "app": "Grocery Voice", "version": "0.3.1"}


@app.post("/api/grocery/parse")
async def parse_grocery_request(payload: GroceryParseRequest):
    transcript = payload.text.strip()
    if not transcript:
        raise HTTPException(status_code=422, detail="Grocery text cannot be blank.")
    try:
        items = parse_grocery_text(transcript)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"items": items, "count": len(items), "language": payload.language}


@app.post("/api/voice/transcript")
async def receive_voice_transcript(payload: VoiceTranscriptRequest):
    transcript = payload.text.strip()
    if not transcript:
        raise HTTPException(status_code=422, detail="Transcript cannot be blank.")
    return {"text": transcript, "language": payload.language, "received": True}


# In local Docker, FastAPI serves the frontend. On Vercel, public/ is served
# separately as static content and is not included in the Python function bundle.
if PUBLIC_DIR.is_dir():
    app.mount("/", StaticFiles(directory=PUBLIC_DIR, html=True), name="public")
