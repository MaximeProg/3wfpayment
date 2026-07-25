import type {
  AdminManaged,
  AdminTransaction,
  AdminTransactionDetail,
  AdminUser,
  ApiKey,
  ApiKeyCreated,
  AppNotification,
  AuditLog,
  DashboardOverview,
  ErrorLog,
  MonitoringHealth,
  Project,
  ProjectActivity,
  SystemSetting,
  WebhookEvent,
  WebhookEventDetail,
  YellowCardBalance,
} from "./types";

const API_BASE = `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/admin/v1`;

export class ApiError extends Error {
  status: number;
  detail: unknown;

  constructor(status: number, detail: unknown) {
    super(typeof detail === "string" ? detail : `Erreur API (${status})`);
    this.status = status;
    this.detail = detail;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    credentials: "include",
    headers: {
      ...(init?.body ? { "Content-Type": "application/json" } : {}),
      ...init?.headers,
    },
  });

  if (!res.ok) {
    let detail: unknown;
    try {
      const body = await res.json();
      detail = body.detail ?? body;
    } catch {
      detail = res.statusText;
    }
    throw new ApiError(res.status, detail);
  }

  if (res.status === 204 || res.headers.get("content-length") === "0") {
    return undefined as T;
  }
  return (await res.json()) as T;
}

function qs(params: Record<string, string | number | boolean | undefined | null>): string {
  const entries = Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== "");
  if (entries.length === 0) return "";
  const search = new URLSearchParams(entries.map(([k, v]) => [k, String(v)]));
  return `?${search.toString()}`;
}

// --- Auth ---

export const authApi = {
  login: (email: string, password: string) =>
    request<AdminUser>("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),
  logout: () => request<{ logged_out: boolean }>("/auth/logout", { method: "POST" }),
  me: () => request<AdminUser>("/auth/me"),
};

// --- Dashboard ---

export const dashboardApi = {
  overview: () => request<DashboardOverview>("/stats/overview"),
  byProject: () => request<ProjectActivity[]>("/stats/by-project"),
  yellowCardBalance: () => request<YellowCardBalance[]>("/stats/yellowcard-balance"),
};

// --- Projects & API keys ---

export const projectsApi = {
  list: () => request<Project[]>("/projects"),
  get: (id: string) => request<Project>(`/projects/${id}`),
  create: (payload: { name: string; slug: string; description?: string; environment: string }) =>
    request<Project>("/projects", { method: "POST", body: JSON.stringify(payload) }),
  update: (id: string, payload: { name?: string; description?: string; status?: string }) =>
    request<Project>(`/projects/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  listApiKeys: (projectId: string) => request<ApiKey[]>(`/projects/${projectId}/api-keys`),
  createApiKey: (projectId: string, scopes?: string[]) =>
    request<ApiKeyCreated>(`/projects/${projectId}/api-keys`, {
      method: "POST",
      body: JSON.stringify({ scopes: scopes ?? null }),
    }),
  rotateApiKey: (apiKeyId: string) =>
    request<ApiKeyCreated>(`/projects/api-keys/${apiKeyId}/rotate`, { method: "POST" }),
  revokeApiKey: (apiKeyId: string) =>
    request<ApiKey>(`/projects/api-keys/${apiKeyId}/revoke`, { method: "POST" }),
};

// --- Transactions ---

export const transactionsApi = {
  list: (params: {
    project_id?: string;
    type?: string;
    status?: string;
    search?: string;
    limit?: number;
    offset?: number;
  }) => request<AdminTransaction[]>(`/transactions${qs(params)}`),
  get: (id: string) => request<AdminTransactionDetail>(`/transactions/${id}`),
};

// --- Webhooks ---

export const webhooksApi = {
  list: (params: { status?: string; limit?: number; offset?: number }) =>
    request<WebhookEvent[]>(`/webhooks${qs(params)}`),
  get: (id: string) => request<WebhookEventDetail>(`/webhooks/${id}`),
  reprocess: (id: string) => request<WebhookEventDetail>(`/webhooks/${id}/reprocess`, { method: "POST" }),
};

// --- Monitoring ---

export const monitoringApi = {
  health: () => request<MonitoringHealth>("/monitoring/health"),
  errors: (params: { source?: string; resolved?: boolean; limit?: number; offset?: number }) =>
    request<ErrorLog[]>(`/monitoring/errors${qs(params)}`),
};

// --- Audit ---

export const auditApi = {
  list: (params: { limit?: number; offset?: number }) => request<AuditLog[]>(`/audit-logs${qs(params)}`),
};

// --- Settings ---

export const settingsApi = {
  list: () => request<SystemSetting[]>("/settings"),
  update: (key: string, payload: { value: unknown; description?: string }) =>
    request<SystemSetting>(`/settings/${key}`, { method: "PATCH", body: JSON.stringify(payload) }),
};

// --- Admin management ---

export const adminsApi = {
  list: () => request<AdminManaged[]>("/admins"),
  invite: (payload: { email: string; role: string }) =>
    request<AdminManaged>("/admins", { method: "POST", body: JSON.stringify(payload) }),
  updateRole: (id: string, role: string) =>
    request<AdminManaged>(`/admins/${id}/role`, { method: "PATCH", body: JSON.stringify({ role }) }),
  setActive: (id: string, is_active: boolean) =>
    request<AdminManaged>(`/admins/${id}/active`, { method: "PATCH", body: JSON.stringify({ is_active }) }),
};

// --- Compte courant ---

export const meApi = {
  changePassword: (payload: { current_password: string; new_password: string }) =>
    request<{ updated: boolean }>("/me/password", { method: "PATCH", body: JSON.stringify(payload) }),
};

// --- Notifications ---

export const notificationsApi = {
  list: (params: { unread_only?: boolean; limit?: number; offset?: number }) =>
    request<AppNotification[]>(`/notifications${qs(params)}`),
  unreadCount: () => request<{ count: number }>("/notifications/unread-count"),
  markRead: (id: string) => request<{ read: boolean }>(`/notifications/${id}/read`, { method: "POST" }),
  markAllRead: () => request<{ read: boolean }>("/notifications/read-all", { method: "POST" }),
};
