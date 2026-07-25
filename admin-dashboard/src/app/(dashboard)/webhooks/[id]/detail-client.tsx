"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, RotateCcw } from "lucide-react";
import { webhooksApi, ApiError } from "@/lib/api";
import { useFetch, apiErrorMessage } from "@/lib/use-fetch";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { PageSpinner, ErrorBanner } from "@/components/ui/Feedback";
import { Badge, WebhookStatusBadge } from "@/components/ui/Badge";
import { JsonViewer } from "@/components/ui/JsonViewer";
import { Button } from "@/components/ui/Button";
import { formatDateTime } from "@/lib/format";

export function WebhookDetailClient({ id }: { id: string }) {
  const { data: webhook, loading, error, reload } = useFetch(() => webhooksApi.get(id), [id]);
  const [reprocessing, setReprocessing] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  async function handleReprocess() {
    setReprocessing(true);
    setActionError(null);
    try {
      await webhooksApi.reprocess(id);
      reload();
    } catch (err) {
      setActionError(err instanceof ApiError ? apiErrorMessage(err) : "Retraitement impossible");
    } finally {
      setReprocessing(false);
    }
  }

  if (loading) return <PageSpinner />;
  if (error) return <ErrorBanner message={error} />;
  if (!webhook) return null;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <Link href="/webhooks" className="inline-flex items-center gap-1 text-sm text-muted hover:text-foreground">
          <ArrowLeft className="h-4 w-4" /> Retour aux webhooks
        </Link>
        <div className="mt-2 flex flex-wrap items-center gap-3">
          <h1 className="text-xl font-semibold text-foreground">{webhook.event_type}</h1>
          <WebhookStatusBadge status={webhook.status} />
          <Badge tone={webhook.signature_valid ? "success" : "danger"}>
            signature {webhook.signature_valid ? "valide" : "invalide"}
          </Badge>
        </div>
      </div>

      {actionError && <ErrorBanner message={actionError} />}
      {webhook.processing_error && <ErrorBanner message={webhook.processing_error} />}

      <Card>
        <CardHeader
          title="Details"
          action={
            <Button size="sm" variant="secondary" loading={reprocessing} onClick={handleReprocess}>
              <RotateCcw className="h-3.5 w-3.5" /> Retraiter
            </Button>
          }
        />
        <CardBody className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div>
            <p className="text-xs font-medium uppercase text-muted">Identifiant externe</p>
            <p className="break-all text-sm text-foreground">{webhook.external_event_id}</p>
          </div>
          <div>
            <p className="text-xs font-medium uppercase text-muted">Transaction liee</p>
            {webhook.transaction_id ? (
              <Link href={`/transactions/${webhook.transaction_id}`} className="text-sm text-accent hover:underline">
                {webhook.transaction_id}
              </Link>
            ) : (
              <p className="text-sm text-muted-foreground">—</p>
            )}
          </div>
          <div>
            <p className="text-xs font-medium uppercase text-muted">Recu le</p>
            <p className="text-sm text-foreground">{formatDateTime(webhook.received_at)}</p>
          </div>
          <div>
            <p className="text-xs font-medium uppercase text-muted">Traite le</p>
            <p className="text-sm text-foreground">{formatDateTime(webhook.processed_at)}</p>
          </div>
        </CardBody>
      </Card>

      <Card>
        <CardHeader title="Payload brut" />
        <CardBody>
          <JsonViewer data={webhook.raw_payload} />
        </CardBody>
      </Card>
    </div>
  );
}
