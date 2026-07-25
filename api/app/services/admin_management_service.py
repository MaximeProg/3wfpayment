import secrets
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.email import send_email
from app.core.security import hash_password, verify_password
from app.models.admin import AdminUser
from app.models.enums import AdminRole, NotificationCategory
from app.repositories import admin_repository
from app.services.notification_service import notify

settings = get_settings()


class AdminManagementError(Exception):
    pass


class CannotActOnSelfError(AdminManagementError):
    pass


class InvalidCurrentPasswordError(AdminManagementError):
    pass


async def list_admins(db: AsyncSession) -> list[AdminUser]:
    return await admin_repository.list_all(db)


def _invite_email_html(*, email: str, temp_password: str) -> str:
    login_url = f"{settings.admin_dashboard_origin}/login"
    return f"""
    <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto;">
      <h2>Acces au dashboard Payment Platform</h2>
      <p>Un compte administrateur a ete cree pour vous.</p>
      <p><strong>Email :</strong> {email}<br/>
      <strong>Mot de passe temporaire :</strong> {temp_password}</p>
      <p><a href="{login_url}">Se connecter</a></p>
      <p style="color:#666;font-size:12px;">Merci de changer ce mot de passe des votre premiere connexion
      (menu Profil).</p>
    </div>
    """.strip()


async def invite_admin(db: AsyncSession, *, inviter: AdminUser, email: str, role: AdminRole) -> AdminUser:
    temp_password = secrets.token_urlsafe(12)
    admin = await admin_repository.create(
        db,
        email=email,
        password_hash=hash_password(temp_password),
        role=role,
        invited_by_id=inviter.id,
    )

    send_email(
        to=admin.email,
        subject="Votre acces au dashboard Payment Platform",
        html=_invite_email_html(email=admin.email, temp_password=temp_password),
    )

    await notify(
        db,
        category=NotificationCategory.admin,
        audience_min_role=AdminRole.super_admin,
        title="Nouvel administrateur invite",
        message=f"{admin.email} ({role.value}) invite par {inviter.email}",
        related_type="admin",
        related_id=str(admin.id),
    )
    return admin


async def update_admin_role(db: AsyncSession, *, actor: AdminUser, target_id: uuid.UUID, role: AdminRole) -> AdminUser:
    if actor.id == target_id:
        raise CannotActOnSelfError("Impossible de modifier son propre role")
    target = await admin_repository.get_by_id(db, target_id)
    if target is None:
        raise LookupError("Administrateur introuvable")
    return await admin_repository.update_role(db, target, role)


async def set_admin_active(
    db: AsyncSession, *, actor: AdminUser, target_id: uuid.UUID, is_active: bool
) -> AdminUser:
    if actor.id == target_id:
        raise CannotActOnSelfError("Impossible de desactiver son propre compte")
    target = await admin_repository.get_by_id(db, target_id)
    if target is None:
        raise LookupError("Administrateur introuvable")
    return await admin_repository.set_active(db, target, is_active)


async def change_own_password(
    db: AsyncSession, *, admin: AdminUser, current_password: str, new_password: str
) -> None:
    if not verify_password(current_password, admin.password_hash):
        raise InvalidCurrentPasswordError("Mot de passe actuel incorrect")
    await admin_repository.update_password_hash(db, admin, hash_password(new_password))
