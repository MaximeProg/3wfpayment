import uuid
from collections.abc import Callable

import jwt
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.admin import AdminUser
from app.models.enums import AdminRole, ProjectStatus
from app.models.project import Project
from app.repositories import admin_repository, project_repository

_bearer_scheme = HTTPBearer(auto_error=False)

ADMIN_SESSION_COOKIE = "admin_session"

# Hierarchie des roles admin : super_admin > admin > viewer.
_ROLE_RANK = {AdminRole.viewer: 0, AdminRole.admin: 1, AdminRole.super_admin: 2}


class CurrentProject:
    def __init__(self, project: Project, scopes: list[str]):
        self.project = project
        self.scopes = scopes

    def require_scope(self, scope: str) -> None:
        if scope not in self.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Scope manquant : '{scope}'"
            )


async def get_current_project(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> CurrentProject:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token manquant")

    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide") from exc

    try:
        project_id = uuid.UUID(payload["sub"])
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide") from exc

    project = await project_repository.get_by_id(db, project_id)
    if project is None or project.status != ProjectStatus.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Projet inactif ou introuvable")

    return CurrentProject(project=project, scopes=payload.get("scopes", []))


async def get_current_admin(
    admin_session: str | None = Cookie(default=None, alias=ADMIN_SESSION_COOKIE),
    db: AsyncSession = Depends(get_db),
) -> AdminUser:
    if admin_session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session admin manquante")

    try:
        payload = decode_access_token(admin_session)
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session admin invalide") from exc

    if payload.get("type") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session admin invalide")

    try:
        admin_id = uuid.UUID(payload["sub"])
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session admin invalide") from exc

    admin = await admin_repository.get_by_id(db, admin_id)
    if admin is None or not admin.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Compte admin inactif ou introuvable")

    return admin


def require_admin_role(minimum_role: AdminRole) -> Callable:
    """Dependance FastAPI verifiant que l'admin courant a au moins le role donne
    (hierarchie : super_admin > admin > viewer)."""

    async def _dependency(admin: AdminUser = Depends(get_current_admin)) -> AdminUser:
        if _ROLE_RANK[admin.role] < _ROLE_RANK[minimum_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role insuffisant : '{minimum_role.value}' requis",
            )
        return admin

    return _dependency
