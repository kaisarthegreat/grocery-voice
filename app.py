from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"

app = FastAPI(title="Grocery Voice", version="0.1.0")

# Static assets are served by FastAPI locally and through the Vercel Python function.
app.mount("/assets", StaticFiles(directory=PUBLIC_DIR), name="assets")


@app.get("/api/health")
async def health():
    return {"status": "ok", "app": "Grocery Voice", "version": "0.1.0"}


@app.get("/")
async def home():
    return FileResponse(PUBLIC_DIR / "index.html")
