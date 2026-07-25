import uuid
from datetime import datetime

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.enums import StatusChangeSource, TransactionStatus, TransactionType
from app.models.transaction import Transaction, TransactionStatusHistory


async def get_by_id_for_project(
    db: AsyncSession, *, transaction_id: uuid.UUID, project_id: uuid.UUID
) -> Transaction | None:
    result = await db.execute(
        select(Transaction).where(Transaction.id == transaction_id, Transaction.project_id == project_id)
    )
    return result.scalar_one_or_none()


async def get_by_client_reference(
    db: AsyncSession, *, project_id: uuid.UUID, client_reference: str
) -> Transaction | None:
    result = await db.execute(
        select(Transaction).where(
            Transaction.project_id == project_id, Transaction.client_reference == client_reference
        )
    )
    return result.scalar_one_or_none()


async def get_by_yellowcard_reference(db: AsyncSession, yellowcard_reference: str) -> Transaction | None:
    """Non filtre par projet : utilise uniquement par le traitement interne des
    webhooks Yellow Card (qui ne porte pas de contexte projet)."""
    result = await db.execute(
        select(Transaction).where(Transaction.yellowcard_reference == yellowcard_reference)
    )
    return result.scalar_one_or_none()


async def list_for_project(
    db: AsyncSession,
    *,
    project_id: uuid.UUID,
    type_: TransactionType | None = None,
    status: TransactionStatus | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Transaction]:
    query = select(Transaction).where(Transaction.project_id == project_id)
    if type_ is not None:
        query = query.where(Transaction.type == type_)
    if status is not None:
        query = query.where(Transaction.status == status)
    query = query.order_by(Transaction.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, transaction_id: uuid.UUID) -> Transaction | None:
    """Non filtre par projet - reserve aux vues admin (cross-projet)."""
    result = await db.execute(
        select(Transaction)
        .where(Transaction.id == transaction_id)
        .options(selectinload(Transaction.status_history))
    )
    return result.scalar_one_or_none()


async def admin_list(
    db: AsyncSession,
    *,
    project_id: uuid.UUID | None = None,
    type_: TransactionType | None = None,
    status: TransactionStatus | None = None,
    search: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Transaction]:
    """Liste cross-projet pour le dashboard admin (FE-15/16/17)."""
    query = select(Transaction)
    if project_id is not None:
        query = query.where(Transaction.project_id == project_id)
    if type_ is not None:
        query = query.where(Transaction.type == type_)
    if status is not None:
        query = query.where(Transaction.status == status)
    if search:
        pattern = f"%{search}%"
        query = query.where(
            or_(
                Transaction.reference.ilike(pattern),
                Transaction.client_reference.ilike(pattern),
                Transaction.yellowcard_reference.ilike(pattern),
            )
        )
    query = query.order_by(Transaction.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    return list(result.scalars().all())


async def count_by_status(db: AsyncSession, *, project_id: uuid.UUID | None = None) -> dict[str, int]:
    query = select(Transaction.status, func.count(Transaction.id)).group_by(Transaction.status)
    if project_id is not None:
        query = query.where(Transaction.project_id == project_id)
    result = await db.execute(query)
    return {row[0].value: row[1] for row in result.all()}


async def count_by_type(db: AsyncSession, *, project_id: uuid.UUID | None = None) -> dict[str, int]:
    query = select(Transaction.type, func.count(Transaction.id)).group_by(Transaction.type)
    if project_id is not None:
        query = query.where(Transaction.project_id == project_id)
    result = await db.execute(query)
    return {row[0].value: row[1] for row in result.all()}


async def count_by_project_and_status(db: AsyncSession) -> list[tuple[uuid.UUID, str, int]]:
    query = select(Transaction.project_id, Transaction.status, func.count(Transaction.id)).group_by(
        Transaction.project_id, Transaction.status
    )
    result = await db.execute(query)
    return [(row[0], row[1].value, row[2]) for row in result.all()]


async def count_total(db: AsyncSession) -> int:
    result = await db.execute(select(func.count(Transaction.id)))
    return result.scalar_one()


async def create(db: AsyncSession, transaction: Transaction) -> Transaction:
    db.add(transaction)
    await db.flush()
    db.add(
        TransactionStatusHistory(
            transaction_id=transaction.id,
            previous_status=None,
            new_status=transaction.status.value,
            source=StatusChangeSource.system,
            payload=transaction.response_payload,
        )
    )
    await db.commit()
    await db.refresh(transaction)
    return transaction


async def update_status(
    db: AsyncSession,
    transaction: Transaction,
    *,
    new_status: TransactionStatus,
    response_payload: dict,
    failure_reason: str | None,
    completed_at: datetime | None,
    source: StatusChangeSource,
) -> Transaction:
    previous_status = transaction.status.value
    transaction.status = new_status
    transaction.response_payload = response_payload
    transaction.failure_reason = failure_reason
    if completed_at is not None:
        transaction.completed_at = completed_at

    if previous_status != new_status.value:
        db.add(
            TransactionStatusHistory(
                transaction_id=transaction.id,
                previous_status=previous_status,
                new_status=new_status.value,
                source=source,
                payload=response_payload,
            )
        )

    await db.commit()
    await db.refresh(transaction)
    return transaction
