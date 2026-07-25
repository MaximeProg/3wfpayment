import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import CurrentProject, get_current_project
from app.db.session import get_db
from app.integrations.yellowcard.client import YellowCardAPIError
from app.models.enums import ErrorLevel, ErrorSource, TransactionStatus, TransactionType
from app.repositories import transaction_repository as repo
from app.schemas.transaction import (
    CryptoSendCreateRequest,
    DepositCreateRequest,
    TransactionOut,
    WithdrawalCreateRequest,
)
from app.services.error_log_service import log_error
from app.services.transaction_service import (
    ChannelNotFoundError,
    NetworkNotFoundError,
    create_crypto_send,
    create_deposit,
    create_withdrawal,
    refresh_transaction_status,
)

router = APIRouter(tags=["transactions"])


async def _get_owned_transaction(db: AsyncSession, current: CurrentProject, transaction_id: uuid.UUID):
    transaction = await repo.get_by_id_for_project(
        db, transaction_id=transaction_id, project_id=current.project.id
    )
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction introuvable")
    return transaction


@router.post("/deposits", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
async def create_deposit_endpoint(
    payload: DepositCreateRequest,
    db: AsyncSession = Depends(get_db),
    current: CurrentProject = Depends(get_current_project),
) -> TransactionOut:
    current.require_scope("deposits:write")
    try:
        transaction = await create_deposit(db, project=current.project, payload=payload)
    except (ChannelNotFoundError, NetworkNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except YellowCardAPIError as exc:
        await log_error(
            db,
            source=ErrorSource.yellowcard_api,
            level=ErrorLevel.error,
            message=f"Echec creation depot (projet {current.project.slug})",
            context={"status_code": exc.status_code, "payload": exc.payload, "project_id": str(current.project.id)},
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"message": "Yellow Card a rejete la requete de depot", "yellowcard_error": exc.payload},
        ) from exc
    return TransactionOut.model_validate(transaction)


@router.get("/deposits/{transaction_id}", response_model=TransactionOut)
async def get_deposit(
    transaction_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current: CurrentProject = Depends(get_current_project),
) -> TransactionOut:
    current.require_scope("transactions:read")
    transaction = await _get_owned_transaction(db, current, transaction_id)
    if transaction.type != TransactionType.deposit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction introuvable")
    transaction = await refresh_transaction_status(db, project=current.project, transaction=transaction)
    return TransactionOut.model_validate(transaction)


@router.get("/deposits", response_model=list[TransactionOut])
async def list_deposits(
    status_filter: TransactionStatus | None = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current: CurrentProject = Depends(get_current_project),
) -> list[TransactionOut]:
    current.require_scope("transactions:read")
    transactions = await repo.list_for_project(
        db,
        project_id=current.project.id,
        type_=TransactionType.deposit,
        status=status_filter,
        limit=limit,
        offset=offset,
    )
    return [TransactionOut.model_validate(t) for t in transactions]


@router.post("/withdrawals", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
async def create_withdrawal_endpoint(
    payload: WithdrawalCreateRequest,
    db: AsyncSession = Depends(get_db),
    current: CurrentProject = Depends(get_current_project),
) -> TransactionOut:
    current.require_scope("withdrawals:write")
    try:
        transaction = await create_withdrawal(db, project=current.project, payload=payload)
    except (ChannelNotFoundError, NetworkNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except YellowCardAPIError as exc:
        await log_error(
            db,
            source=ErrorSource.yellowcard_api,
            level=ErrorLevel.error,
            message=f"Echec creation retrait (projet {current.project.slug})",
            context={"status_code": exc.status_code, "payload": exc.payload, "project_id": str(current.project.id)},
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"message": "Yellow Card a rejete la requete de retrait", "yellowcard_error": exc.payload},
        ) from exc
    return TransactionOut.model_validate(transaction)


@router.get("/withdrawals/{transaction_id}", response_model=TransactionOut)
async def get_withdrawal(
    transaction_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current: CurrentProject = Depends(get_current_project),
) -> TransactionOut:
    current.require_scope("transactions:read")
    transaction = await _get_owned_transaction(db, current, transaction_id)
    if transaction.type != TransactionType.withdrawal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction introuvable")
    transaction = await refresh_transaction_status(db, project=current.project, transaction=transaction)
    return TransactionOut.model_validate(transaction)


@router.get("/withdrawals", response_model=list[TransactionOut])
async def list_withdrawals(
    status_filter: TransactionStatus | None = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current: CurrentProject = Depends(get_current_project),
) -> list[TransactionOut]:
    current.require_scope("transactions:read")
    transactions = await repo.list_for_project(
        db,
        project_id=current.project.id,
        type_=TransactionType.withdrawal,
        status=status_filter,
        limit=limit,
        offset=offset,
    )
    return [TransactionOut.model_validate(t) for t in transactions]


@router.post("/crypto-sends", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
async def create_crypto_send_endpoint(
    payload: CryptoSendCreateRequest,
    db: AsyncSession = Depends(get_db),
    current: CurrentProject = Depends(get_current_project),
) -> TransactionOut:
    current.require_scope("crypto_sends:write")
    try:
        transaction = await create_crypto_send(db, project=current.project, payload=payload)
    except YellowCardAPIError as exc:
        await log_error(
            db,
            source=ErrorSource.yellowcard_api,
            level=ErrorLevel.error,
            message=f"Echec creation crypto send (projet {current.project.slug})",
            context={"status_code": exc.status_code, "payload": exc.payload, "project_id": str(current.project.id)},
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"message": "Yellow Card a rejete la requete de crypto send", "yellowcard_error": exc.payload},
        ) from exc
    return TransactionOut.model_validate(transaction)


@router.get("/crypto-sends/{transaction_id}", response_model=TransactionOut)
async def get_crypto_send(
    transaction_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current: CurrentProject = Depends(get_current_project),
) -> TransactionOut:
    current.require_scope("transactions:read")
    transaction = await _get_owned_transaction(db, current, transaction_id)
    if transaction.type != TransactionType.crypto_send:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction introuvable")
    transaction = await refresh_transaction_status(db, project=current.project, transaction=transaction)
    return TransactionOut.model_validate(transaction)


@router.get("/crypto-sends", response_model=list[TransactionOut])
async def list_crypto_sends_endpoint(
    status_filter: TransactionStatus | None = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current: CurrentProject = Depends(get_current_project),
) -> list[TransactionOut]:
    current.require_scope("transactions:read")
    transactions = await repo.list_for_project(
        db,
        project_id=current.project.id,
        type_=TransactionType.crypto_send,
        status=status_filter,
        limit=limit,
        offset=offset,
    )
    return [TransactionOut.model_validate(t) for t in transactions]


@router.get("/transactions/{transaction_id}", response_model=TransactionOut)
async def get_transaction(
    transaction_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current: CurrentProject = Depends(get_current_project),
) -> TransactionOut:
    current.require_scope("transactions:read")
    transaction = await _get_owned_transaction(db, current, transaction_id)
    transaction = await refresh_transaction_status(db, project=current.project, transaction=transaction)
    return TransactionOut.model_validate(transaction)


@router.get("/transactions", response_model=list[TransactionOut])
async def list_transactions(
    type_filter: TransactionType | None = Query(None, alias="type"),
    status_filter: TransactionStatus | None = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current: CurrentProject = Depends(get_current_project),
) -> list[TransactionOut]:
    current.require_scope("transactions:read")
    transactions = await repo.list_for_project(
        db,
        project_id=current.project.id,
        type_=type_filter,
        status=status_filter,
        limit=limit,
        offset=offset,
    )
    return [TransactionOut.model_validate(t) for t in transactions]
