"use client";

import { useState } from "react";
import { auditApi } from "@/lib/api";
import { useFetch } from "@/lib/use-fetch";
import { Card } from "@/components/ui/Card";
import { PageSpinner, ErrorBanner, EmptyState } from "@/components/ui/Feedback";
import { Table, Thead, Tbody, Tr, Th, Td } from "@/components/ui/Table";
import { Button } from "@/components/ui/Button";
import { formatDateTime } from "@/lib/format";

const PAGE_SIZE = 50;

export default function AuditPage() {
  const [offset, setOffset] = useState(0);
  const logs = useFetch(() => auditApi.list({ limit: PAGE_SIZE, offset }), [offset]);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-semibold text-foreground">Journal d&apos;audit</h1>
        <p className="text-sm text-muted">Actions administratives sensibles (projets, cles API, parametres).</p>
      </div>

      <Card>
        {logs.loading ? (
          <PageSpinner />
        ) : logs.error ? (
          <div className="p-5">
            <ErrorBanner message={logs.error} />
          </div>
        ) : logs.data && logs.data.length > 0 ? (
          <>
            <Table>
              <Thead>
                <Tr>
                  <Th>Action</Th>
                  <Th>Ressource</Th>
                  <Th>Acteur</Th>
                  <Th>IP</Th>
                  <Th>Date</Th>
                </Tr>
              </Thead>
              <Tbody>
                {logs.data.map((log) => (
                  <Tr key={log.id}>
                    <Td className="font-medium text-foreground">{log.action}</Td>
                    <Td>
                      {log.resource_type} <span className="text-xs text-muted-foreground">{log.resource_id}</span>
                    </Td>
                    <Td className="whitespace-nowrap">{log.actor_type} / {log.actor_id.slice(0, 8)}…</Td>
                    <Td className="text-muted">{log.ip_address ?? "—"}</Td>
                    <Td className="text-muted whitespace-nowrap">{formatDateTime(log.created_at)}</Td>
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
                disabled={logs.data.length < PAGE_SIZE}
                onClick={() => setOffset(offset + PAGE_SIZE)}
              >
                Suivant
              </Button>
            </div>
          </>
        ) : (
          <EmptyState title="Aucune entree" hint="Les actions administratives apparaitront ici." />
        )}
      </Card>
    </div>
  );
}
