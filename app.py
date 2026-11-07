from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"

app = FastAPI(
    title="Grocery Voice",
    version="0.1.0"
)


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "app": "Grocery Voice",
        "version": "0.1.0"
    }


# Serve frontend files locally.
# On Vercel, the public directory is served separately.
if PUBLIC_DIR.is_dir():
    app.mount(
        "/",
        StaticFiles(directory=PUBLIC_DIR, html=True),
        name="public"
    )