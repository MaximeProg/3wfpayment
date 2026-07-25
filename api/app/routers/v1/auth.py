from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session import get_db
from app.schemas.auth import TokenRequest, TokenResponse
from app.services.auth_service import InvalidApiKeyError, issue_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


@router.post("/token", response_model=TokenResponse)
async def create_token(payload: TokenRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    try:
        access_token = await issue_access_token(db, payload.api_key)
    except InvalidApiKeyError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    return TokenResponse(
        access_token=access_token,
        expires_in=settings.jwt_access_token_expire_minutes * 60,
    )
