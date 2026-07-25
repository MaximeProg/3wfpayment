export type AdminRole = "viewer" | "admin" | "super_admin";

export interface AdminUser {
  id: string;
  email: string;
  role: AdminRole;
  is_active: boolean;
  last_login_at: string | null;
  created_at: string;
}

export type ProjectStatus = "active" | "inactive" | "suspended";
export type ProjectEnvironment = "sandbox" | "production";

export interface Project {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  status: ProjectStatus;
  environment: ProjectEnvironment;
  created_at: string;
  updated_at: string;
}

export type ApiKeyStatus = "active" | "revoked";

export interface ApiKey {
  id: string;
  project_id: string;
  key_prefix: string;
  scopes: string[];
  status: ApiKeyStatus;
  last_used_at: string | null;
  expires_at: string | null;
  created_at: string;
}

export interface ApiKeyCreated extends ApiKey {
  full_key: string;
}

export interface StatusBreakdown {
  pending: number;
  processing: number;
  completed: number;
  failed: number;
  cancelled: number;
  expired: number;
}

export interface DashboardOverview {
  total_transactions: number;
  total_projects: number;
  active_projects: number;
  by_status: StatusBreakdown;
  by_type: Record<string, number>;
}

export interface ProjectActivity {
  project_id: string;
  project_name: string;
  project_slug: string;
  total_transactions: number;
  by_status: StatusBreakdown;
}

export type TransactionType = "deposit" | "withdrawal" | "crypto_send";
export type TransactionStatus =
  | "pending"
  | "processing"
  | "completed"
  | "failed"
  | "cancelled"
  | "expired";

export interface AdminTransaction {
  id: string;
  project_id: string;
  type: TransactionType;
  reference: string;
  client_reference: string | null;
  yellowcard_reference: string | null;
  status: TransactionStatus;
  amount: string;
  currency_code: string;
  failure_reason: string | null;
  initiated_at: string;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface TransactionStatusHistoryEntry {
  id: string;
  previous_status: string | null;
  new_status: string;
  source: string;
  created_at: string;
}

export interface AdminTransactionDetail extends AdminTransaction {
  request_payload: Record<string, unknown>;
  response_payload: Record<string, unknown>;
  customer_payload: Record<string, unknown>;
  status_history: TransactionStatusHistoryEntry[];
}

export type WebhookEventStatus = "received" | "processing" | "processed" | "failed" | "ignored";

export interface WebhookEvent {
  id: string;
  event_type: string;
  external_event_id: string;
  signature_valid: boolean;
  status: WebhookEventStatus;
  transaction_id: string | null;
  processing_error: string | null;
  received_at: string;
  processed_at: string | null;
}

export interface WebhookEventDetail extends WebhookEvent {
  raw_payload: Record<string, unknown>;
}

export type ErrorSource = "yellowcard_api" | "internal" | "webhook" | "sync" | "worker";
export type ErrorLevel = "warning" | "error" | "critical";

export interface ErrorLog {
  id: string;
  source: ErrorSource;
  level: ErrorLevel;
  message: string;
  context: Record<string, unknown>;
  resolved: boolean;
  created_at: string;
}

export interface MonitoringHealth {
  database: string;
  yellowcard_sandbox: string;
  yellowcard_production: string;
}

export interface AuditLog {
  id: string;
  actor_type: string;
  actor_id: string;
  action: string;
  resource_type: string;
  resource_id: string;
  before: Record<string, unknown> | null;
  after: Record<string, unknown> | null;
  ip_address: string | null;
  created_at: string;
}

export interface SystemSetting {
  key: string;
  value: unknown;
  description: string | null;
  updated_at: string;
  updated_by: string | null;
}

// --- Admin management ---

export interface AdminManaged extends AdminUser {
  invited_by_id: string | null;
}

// --- Notifications ---

export type NotificationCategory = "transaction" | "webhook" | "error" | "admin" | "system";
export type NotificationSeverity = "info" | "warning" | "critical";

export interface AppNotification {
  id: string;
  category: NotificationCategory;
  severity: NotificationSeverity;
  title: string;
  message: string;
  related_type: string | null;
  related_id: string | null;
  is_read: boolean;
  created_at: string;
}

// --- Yellow Card balance ---

export interface YellowCardAccount {
  available: string;
  currency: string;
  currency_type: string;
}

export interface YellowCardBalance {
  environment: ProjectEnvironment;
  accounts: YellowCardAccount[];
}
