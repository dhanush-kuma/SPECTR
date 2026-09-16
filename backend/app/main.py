import logging
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from .config import CORS_ORIGINS, IS_PRODUCTION
from .core.csrf import CSRFMiddleware
from .core.rate_limit import limiter
from .core.security_headers import SecurityHeadersMiddleware
from .routers import setup, admin, organizers, organizer, investigator

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Study Randomizer API",
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None if IS_PRODUCTION else "/redoc",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(CSRFMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(setup.router)
app.include_router(admin.router)
app.include_router(organizers.router)
app.include_router(organizer.router)
app.include_router(investigator.router)


def _mount_frontend(app: FastAPI) -> None:
    """Serve the built React app from the same origin (Docker / single-domain deploy)."""
    dist = Path(os.environ.get("FRONTEND_DIST", ""))
    if not dist.is_dir():
        return

    index_html = dist / "index.html"
    if not index_html.is_file():
        logging.warning("FRONTEND_DIST set but index.html missing: %s", dist)
        return

    dist_resolved = dist.resolve()

    def _safe_dist_file(relative_path: str) -> Path | None:
        if not relative_path:
            return None
        candidate = (dist_resolved / relative_path).resolve()
        try:
            candidate.relative_to(dist_resolved)
        except ValueError:
            return None
        if candidate.is_file():
            return candidate
        return None

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        safe_file = _safe_dist_file(full_path)
        if safe_file is not None:
            return FileResponse(safe_file)
        return FileResponse(index_html)


_mount_frontend(app)
