import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin_role
from app.db.session import get_db
from app.models.admin import AdminUser
from app.models.enums import AdminRole, TransactionStatus, TransactionType
from app.repositories import transaction_repository as repo
from app.schemas.admin import AdminTransactionDetailOut, AdminTransactionOut

router = APIRouter(prefix="/transactions", tags=["admin-transactions"])


@router.get("", response_model=list[AdminTransactionOut])
async def list_transactions(
    project_id: uuid.UUID | None = Query(None),
    type_filter: TransactionType | None = Query(None, alias="type"),
    status_filter: TransactionStatus | None = Query(None, alias="status"),
    search: str | None = Query(None, description="Recherche sur reference/client_reference/yellowcard_reference"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> list[AdminTransactionOut]:
    transactions = await repo.admin_list(
        db,
        project_id=project_id,
        type_=type_filter,
        status=status_filter,
        search=search,
        limit=limit,
        offset=offset,
    )
    return [AdminTransactionOut.model_validate(t) for t in transactions]


@router.get("/{transaction_id}", response_model=AdminTransactionDetailOut)
async def get_transaction(
    transaction_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> AdminTransactionDetailOut:
    transaction = await repo.get_by_id(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction introuvable")
    return AdminTransactionDetailOut.model_validate(transaction)
