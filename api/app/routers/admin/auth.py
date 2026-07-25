from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.deps import ADMIN_SESSION_COOKIE, get_current_admin
from app.db.session import get_db
from app.models.admin import AdminUser
from app.schemas.admin import AdminLoginRequest, AdminOut
from app.services.admin_auth_service import InvalidAdminCredentialsError, authenticate_admin, issue_admin_session_token

router = APIRouter(prefix="/auth", tags=["admin-auth"])
settings = get_settings()


@router.post("/login", response_model=AdminOut)
async def login(
    payload: AdminLoginRequest, response: Response, db: AsyncSession = Depends(get_db)
) -> AdminOut:
    try:
        admin = await authenticate_admin(db, email=payload.email, password=payload.password)
    except InvalidAdminCredentialsError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides") from exc

    token = issue_admin_session_token(admin)
    response.set_cookie(
        key=ADMIN_SESSION_COOKIE,
        value=token,
        httponly=True,
        secure=settings.is_production,
        samesite="lax",
        max_age=settings.admin_session_expire_minutes * 60,
        path="/",
    )
    return AdminOut.model_validate(admin)


@router.post("/logout")
async def logout(response: Response) -> dict:
    response.delete_cookie(key=ADMIN_SESSION_COOKIE, path="/")
    return {"logged_out": True}


@router.get("/me", response_model=AdminOut)
async def me(admin: AdminUser = Depends(get_current_admin)) -> AdminOut:
    return AdminOut.model_validate(admin)
