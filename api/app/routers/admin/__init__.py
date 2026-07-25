from fastapi import APIRouter

from app.routers.admin import (
    admins,
    audit,
    auth,
    dashboard,
    me,
    monitoring,
    notifications,
    projects,
    settings,
    transactions,
    webhooks,
)

router = APIRouter(prefix="/admin/v1")
router.include_router(auth.router)
router.include_router(dashboard.router)
router.include_router(projects.router)
router.include_router(transactions.router)
router.include_router(webhooks.router)
router.include_router(monitoring.router)
router.include_router(audit.router)
router.include_router(settings.router)
router.include_router(admins.router)
router.include_router(me.router)
router.include_router(notifications.router)
