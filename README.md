# Grocery Voice

A personal, local-first grocery-list PWA. Stage 2 adds browser speech capture in English (India) and Hindi (India), with transcript validation through FastAPI.

## Local development with Docker (recommended)

Requirements:
- Docker Desktop on Windows, or Docker Engine + Docker Compose plugin on Linux/WSL2
- Docker Compose v2 (`docker compose`)

From the project directory, run:

```bash
docker compose up --build
```

Open:
- App: http://localhost:8000
- Health check: http://localhost:8000/api/health

The project directory is bind-mounted into the container. Python source changes are picked up by Uvicorn's reload mode. If you change `requirements.txt`, rebuild:

```bash
docker compose up --build
```

Stop the development server with `Ctrl+C`, then run:

```bash
docker compose down
```

## Local development without Docker (optional)

Requires Python 3.12+.

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# WSL2 / Linux
source .venv/bin/activate

python -m pip install -r requirements.txt
uvicorn app:app --reload
```

## Production deployment on Vercel

Docker is only for local development. Vercel's Python runtime runs the FastAPI application as a serverless function, so do not deploy the app as a Docker container.

- Keep `app.py`, `requirements.txt`, and `.python-version` in the repository root. No custom `vercel.json` is needed for the working auto-detected setup.
- Push the project to GitHub.
- Import the repository into Vercel and deploy using the Python runtime configuration.
- Do not configure Vercel to build or run the local `Dockerfile`.
- Test the deployed app and `/api/health` endpoint after deployment.

The `Dockerfile`, `compose.yaml`, and `.dockerignore` are for local development only.

## Stage 2 features

- Browser speech recognition using the Web Speech API
- English (India) and Hindi (India) recognition-language choices
- Continuous listening with interim transcript display
- Start/stop controls and microphone error feedback
- Recognized transcript is sent to `POST /api/voice/transcript` and placed in the item field for review
- Typing remains available when speech recognition is unsupported or unavailable

Voice recognition support depends on the browser and device. It generally requires HTTPS (or localhost) and may use an online browser speech service. The app does not record or upload raw microphone audio; it sends only the recognized text to the app backend when listening stops.

## Stage 1 features

- Add and remove grocery items
- Edit quantities
- Mark items as purchased
- Clear completed items
- Save automatically in browser `localStorage`
- Copy or share the list using browser capabilities

## Important notes

- The list is stored in the browser on the current device. Clearing browser site data will remove it.
- No account, database, or cloud synchronization is configured.
- Natural-language item and quantity extraction, Hinglish vocabulary, and voice-based list commands are planned for Stage 3.
- The service worker file remains scaffolded; service-worker registration and install icons will be completed in the PWA stage.
- The project targets Python 3.12 for compatibility with the Vercel Python runtime.
