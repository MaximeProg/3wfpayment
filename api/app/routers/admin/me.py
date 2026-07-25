from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.models.admin import AdminUser
from app.schemas.admin import ChangePasswordRequest
from app.services.admin_management_service import InvalidCurrentPasswordError, change_own_password

router = APIRouter(prefix="/me", tags=["admin-me"])


@router.patch("/password")
async def change_password(
    payload: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
) -> dict:
    try:
        await change_own_password(
            db, admin=admin, current_password=payload.current_password, new_password=payload.new_password
        )
    except InvalidCurrentPasswordError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {"updated": True}
