import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import get_settings
from app.db.session import AsyncSessionLocal
from app.routers.admin import router as admin_router
from app.routers.v1 import router as v1_router
from app.webhooks.yellowcard import router as yellowcard_webhook_router

settings = get_settings()

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Payment Platform API",
    description="Passerelle interne unique vers Yellow Card pour tous les produits de l'entreprise.",
    version="0.1.0",
)

# CORS restreint a l'origine du dashboard admin (cookies de session -> credentials requis)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.admin_dashboard_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)
app.include_router(admin_router)
app.include_router(yellowcard_webhook_router)


@app.get("/health", tags=["monitoring"])
async def health() -> dict:
    return {"status": "ok", "environment": settings.environment}


@app.get("/health/ready", tags=["monitoring"])
async def health_ready() -> dict:
    checks = {"database": "unknown"}
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks["database"] = f"error: {exc}"

    overall = "ok" if all(v == "ok" for v in checks.values()) else "degraded"
    return {"status": overall, "checks": checks}
