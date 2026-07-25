from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_admin_session_token, verify_password
from app.models.admin import AdminUser
from app.repositories import admin_repository


class InvalidAdminCredentialsError(Exception):
    pass


async def authenticate_admin(db: AsyncSession, *, email: str, password: str) -> AdminUser:
    admin = await admin_repository.get_by_email(db, email)
    if admin is None or not admin.is_active or not verify_password(password, admin.password_hash):
        raise InvalidAdminCredentialsError("Identifiants invalides")

    await admin_repository.touch_last_login(db, admin)
    return admin


def issue_admin_session_token(admin: AdminUser) -> str:
    return create_admin_session_token(admin_id=str(admin.id), role=admin.role.value)
