"use client";

import { useState } from "react";
import Link from "next/link";
import { webhooksApi } from "@/lib/api";
import { useFetch } from "@/lib/use-fetch";
import { Card, CardHeader } from "@/components/ui/Card";
import { PageSpinner, ErrorBanner, EmptyState } from "@/components/ui/Feedback";
import { WebhookStatusBadge, Badge } from "@/components/ui/Badge";
import { Table, Thead, Tbody, Tr, Th, Td } from "@/components/ui/Table";
import { Select } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { formatDateTime } from "@/lib/format";

const PAGE_SIZE = 25;

export default function WebhooksPage() {
  const [status, setStatus] = useState("");
  const [offset, setOffset] = useState(0);
  const webhooks = useFetch(
    () => webhooksApi.list({ status: status || undefined, limit: PAGE_SIZE, offset }),
    [status, offset]
  );

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-semibold text-foreground">Webhooks</h1>
        <p className="text-sm text-muted">Evenements recus depuis Yellow Card et leur statut de traitement.</p>
      </div>

      <Card>
        <CardHeader
          title="Filtrer"
          action={
            <Select
              value={status}
              onChange={(e) => {
                setStatus(e.target.value);
                setOffset(0);
              }}
              className="w-48"
            >
              <option value="">Tous les statuts</option>
              <option value="received">Recu</option>
              <option value="processed">Traite</option>
              <option value="failed">Echoue</option>
              <option value="ignored">Ignore</option>
            </Select>
          }
        />

        {webhooks.loading ? (
          <PageSpinner />
        ) : webhooks.error ? (
          <div className="p-5">
            <ErrorBanner message={webhooks.error} />
          </div>
        ) : webhooks.data && webhooks.data.length > 0 ? (
          <>
            <Table>
              <Thead>
                <Tr>
                  <Th>Evenement</Th>
                  <Th>Signature</Th>
                  <Th>Statut</Th>
                  <Th>Recu le</Th>
                </Tr>
              </Thead>
              <Tbody>
                {webhooks.data.map((wh) => (
                  <Tr key={wh.id}>
                    <Td>
                      <Link href={`/webhooks/${wh.id}`} className="font-medium text-accent hover:underline">
                        {wh.event_type}
                      </Link>
                    </Td>
                    <Td>
                      <Badge tone={wh.signature_valid ? "success" : "danger"}>
                        {wh.signature_valid ? "valide" : "invalide"}
                      </Badge>
                    </Td>
                    <Td>
                      <WebhookStatusBadge status={wh.status} />
                    </Td>
                    <Td className="text-muted">{formatDateTime(wh.received_at)}</Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
            <div className="flex items-center justify-between border-t border-border px-4 py-3 sm:px-5">
              <Button variant="secondary" size="sm" disabled={offset === 0} onClick={() => setOffset(Math.max(0, offset - PAGE_SIZE))}>
                Precedent
              </Button>
              <span className="text-xs text-muted">Page {Math.floor(offset / PAGE_SIZE) + 1}</span>
              <Button
                variant="secondary"
                size="sm"
                disabled={webhooks.data.length < PAGE_SIZE}
                onClick={() => setOffset(offset + PAGE_SIZE)}
              >
                Suivant
              </Button>
            </div>
          </>
        ) : (
          <EmptyState title="Aucun webhook" hint="Les evenements Yellow Card apparaitront ici." />
        )}
      </Card>
    </div>
  );
}
