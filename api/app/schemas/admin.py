import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --- Auth ---


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    role: str
    is_active: bool
    last_login_at: datetime | None
    created_at: datetime


# --- Gestion des admins ---


class AdminInviteRequest(BaseModel):
    email: EmailStr
    role: str = Field("viewer", description="viewer | admin | super_admin")


class AdminRoleUpdateRequest(BaseModel):
    role: str = Field(..., description="viewer | admin | super_admin")


class AdminActiveUpdateRequest(BaseModel):
    is_active: bool


class AdminManagedOut(AdminOut):
    invited_by_id: uuid.UUID | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


# --- Notifications ---


class NotificationOut(BaseModel):
    id: uuid.UUID
    category: str
    severity: str
    title: str
    message: str
    related_type: str | None
    related_id: str | None
    is_read: bool
    created_at: datetime


class UnreadCountOut(BaseModel):
    count: int


# --- Projects & API keys ---


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    slug: str = Field(..., min_length=1, max_length=120, pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    description: str | None = None
    environment: str = Field("sandbox", description="sandbox | production")


class ProjectUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = Field(None, description="active | inactive | suspended")


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    description: str | None
    status: str
    environment: str
    created_at: datetime
    updated_at: datetime


class ApiKeyCreateRequest(BaseModel):
    scopes: list[str] | None = None


class ApiKeyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    key_prefix: str
    scopes: list[str]
    status: str
    last_used_at: datetime | None
    expires_at: datetime | None
    created_at: datetime


class ApiKeyCreatedOut(ApiKeyOut):
    full_key: str = Field(..., description="Cle complete - affichee une seule fois, non recuperable ensuite")


# --- Dashboard ---


class StatusBreakdown(BaseModel):
    pending: int = 0
    processing: int = 0
    completed: int = 0
    failed: int = 0
    cancelled: int = 0
    expired: int = 0


class DashboardOverviewOut(BaseModel):
    total_transactions: int
    total_projects: int
    active_projects: int
    by_status: StatusBreakdown
    by_type: dict[str, int]


class ProjectActivityOut(BaseModel):
    project_id: uuid.UUID
    project_name: str
    project_slug: str
    total_transactions: int
    by_status: StatusBreakdown


class YellowCardAccountOut(BaseModel):
    available: Decimal
    currency: str
    currency_type: str


class YellowCardBalanceOut(BaseModel):
    environment: str
    accounts: list[YellowCardAccountOut]


# --- Webhooks ---


class WebhookEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    event_type: str
    external_event_id: str
    signature_valid: bool
    status: str
    transaction_id: uuid.UUID | None
    processing_error: str | None
    received_at: datetime
    processed_at: datetime | None


class WebhookEventDetailOut(WebhookEventOut):
    raw_payload: dict[str, Any]


# --- Monitoring ---


class ErrorLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    source: str
    level: str
    message: str
    context: dict[str, Any]
    resolved: bool
    created_at: datetime


class MonitoringHealthOut(BaseModel):
    database: str
    yellowcard_sandbox: str
    yellowcard_production: str


# --- Audit ---


class AuditLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    actor_type: str
    actor_id: str
    action: str
    resource_type: str
    resource_id: str
    before: dict[str, Any] | None
    after: dict[str, Any] | None
    ip_address: str | None
    created_at: datetime


# --- Settings ---


class SystemSettingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    value: Any
    description: str | None
    updated_at: datetime
    updated_by: str | None


class SystemSettingUpdateRequest(BaseModel):
    value: Any
    description: str | None = None


# --- Transactions (admin, cross-project) ---


class AdminTransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    type: str
    reference: str
    client_reference: str | None
    yellowcard_reference: str | None
    status: str
    amount: Decimal
    currency_code: str
    failure_reason: str | None
    initiated_at: datetime
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class TransactionStatusHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    previous_status: str | None
    new_status: str
    source: str
    created_at: datetime


class AdminTransactionDetailOut(AdminTransactionOut):
    request_payload: dict[str, Any]
    response_payload: dict[str, Any]
    customer_payload: dict[str, Any]
    status_history: list[TransactionStatusHistoryOut]
