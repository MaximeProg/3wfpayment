import type { ReactNode } from "react";

type Tone = "neutral" | "success" | "warning" | "danger" | "info";

const toneClasses: Record<Tone, string> = {
  neutral: "bg-border/60 text-foreground",
  success: "bg-success-bg text-success",
  warning: "bg-warning-bg text-warning",
  danger: "bg-danger-bg text-danger",
  info: "bg-info-bg text-info",
};

export function Badge({ tone = "neutral", children }: { tone?: Tone; children: ReactNode }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium whitespace-nowrap ${toneClasses[tone]}`}
    >
      {children}
    </span>
  );
}

const TRANSACTION_STATUS_TONE: Record<string, Tone> = {
  pending: "warning",
  processing: "info",
  completed: "success",
  failed: "danger",
  cancelled: "neutral",
  expired: "neutral",
};

export function StatusBadge({ status }: { status: string }) {
  return <Badge tone={TRANSACTION_STATUS_TONE[status] ?? "neutral"}>{status}</Badge>;
}

const WEBHOOK_STATUS_TONE: Record<string, Tone> = {
  received: "info",
  processing: "info",
  processed: "success",
  failed: "danger",
  ignored: "neutral",
};

export function WebhookStatusBadge({ status }: { status: string }) {
  return <Badge tone={WEBHOOK_STATUS_TONE[status] ?? "neutral"}>{status}</Badge>;
}

const ERROR_LEVEL_TONE: Record<string, Tone> = {
  warning: "warning",
  error: "danger",
  critical: "danger",
};

export function ErrorLevelBadge({ level }: { level: string }) {
  return <Badge tone={ERROR_LEVEL_TONE[level] ?? "neutral"}>{level}</Badge>;
}

const HEALTH_TONE: Record<string, Tone> = {
  ok: "success",
  not_configured: "neutral",
  error: "danger",
  unreachable: "danger",
};

export function HealthBadge({ value }: { value: string }) {
  return <Badge tone={HEALTH_TONE[value] ?? "neutral"}>{value}</Badge>;
}
