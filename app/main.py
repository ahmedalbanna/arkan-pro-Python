from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.logging import configure_logging
from .api.v1.router import api_router_v1

configure_logging()

app = FastAPI(
    title="Arkan Backend API",
    version="0.1.0",
    description="FastAPI backend scaffold for Arkan migration",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(api_router_v1, prefix="/api/v1")


@app.get("/healthz")
async def health_root():
    return {"status": "ok"}
