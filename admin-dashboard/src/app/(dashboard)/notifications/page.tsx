"use client";

import { useState } from "react";
import { notificationsApi } from "@/lib/api";
import { useFetch } from "@/lib/use-fetch";
import { Card } from "@/components/ui/Card";
import { PageSpinner, ErrorBanner, EmptyState } from "@/components/ui/Feedback";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { formatDateTime } from "@/lib/format";

const SEVERITY_TONE: Record<string, "neutral" | "warning" | "danger" | "info"> = {
  info: "info",
  warning: "warning",
  critical: "danger",
};

const CATEGORY_LABELS: Record<string, string> = {
  transaction: "Transaction",
  webhook: "Webhook",
  error: "Erreur",
  admin: "Administration",
  system: "Systeme",
};

export default function NotificationsPage() {
  const [unreadOnly, setUnreadOnly] = useState(false);
  const notifications = useFetch(() => notificationsApi.list({ unread_only: unreadOnly, limit: 100 }), [
    unreadOnly,
  ]);

  async function handleMarkAllRead() {
    await notificationsApi.markAllRead();
    notifications.reload();
  }

  async function handleMarkRead(id: string) {
    await notificationsApi.markRead(id);
    notifications.reload();
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold text-foreground">Notifications</h1>
          <p className="text-sm text-muted">Mouvements et evenements de la plateforme.</p>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant={unreadOnly ? "primary" : "secondary"}
            size="sm"
            onClick={() => setUnreadOnly((v) => !v)}
          >
            {unreadOnly ? "Non lues seulement" : "Toutes"}
          </Button>
          <Button variant="secondary" size="sm" onClick={handleMarkAllRead}>
            Tout marquer comme lu
          </Button>
        </div>
      </div>

      <Card>
        {notifications.loading ? (
          <PageSpinner />
        ) : notifications.error ? (
          <div className="p-5">
            <ErrorBanner message={notifications.error} />
          </div>
        ) : notifications.data && notifications.data.length > 0 ? (
          <div className="divide-y divide-border">
            {notifications.data.map((n) => (
              <div key={n.id} className={`flex items-start gap-3 px-4 py-3.5 sm:px-5 ${n.is_read ? "" : "bg-accent/5"}`}>
                <Badge tone={SEVERITY_TONE[n.severity] ?? "neutral"}>
                  {CATEGORY_LABELS[n.category] ?? n.category}
                </Badge>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-foreground">{n.title}</p>
                  <p className="mt-0.5 text-sm text-muted-foreground">{n.message}</p>
                  <p className="mt-1 text-xs text-muted">{formatDateTime(n.created_at)}</p>
                </div>
                {!n.is_read && (
                  <Button variant="secondary" size="sm" onClick={() => handleMarkRead(n.id)}>
                    Marquer comme lu
                  </Button>
                )}
              </div>
            ))}
          </div>
        ) : (
          <EmptyState title="Aucune notification" hint={unreadOnly ? "Aucune notification non lue." : undefined} />
        )}
      </Card>
    </div>
  );
}
