import enum


class ProjectStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"


class Environment(str, enum.Enum):
    sandbox = "sandbox"
    production = "production"


class ApiKeyStatus(str, enum.Enum):
    active = "active"
    revoked = "revoked"


class TransactionType(str, enum.Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    crypto_send = "crypto_send"


class TransactionStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"
    expired = "expired"


class StatusChangeSource(str, enum.Enum):
    webhook = "webhook"
    polling = "polling"
    manual = "manual"
    system = "system"


class WebhookEventStatus(str, enum.Enum):
    received = "received"
    processing = "processing"
    processed = "processed"
    failed = "failed"
    ignored = "ignored"


class AuditActorType(str, enum.Enum):
    admin = "admin"
    api_key = "api_key"
    system = "system"


class ErrorSource(str, enum.Enum):
    yellowcard_api = "yellowcard_api"
    internal = "internal"
    webhook = "webhook"
    sync = "sync"
    worker = "worker"


class ErrorLevel(str, enum.Enum):
    warning = "warning"
    error = "error"
    critical = "critical"


class AdminRole(str, enum.Enum):
    super_admin = "super_admin"
    admin = "admin"
    viewer = "viewer"


class NotificationCategory(str, enum.Enum):
    transaction = "transaction"
    webhook = "webhook"
    error = "error"
    admin = "admin"
    system = "system"


class NotificationSeverity(str, enum.Enum):
    info = "info"
    warning = "warning"
    critical = "critical"
