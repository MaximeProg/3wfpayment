from fastapi import APIRouter

from app.routers.v1 import auth, reference_data, transactions

router = APIRouter(prefix="/v1")
router.include_router(auth.router)
router.include_router(reference_data.router)
router.include_router(transactions.router)
